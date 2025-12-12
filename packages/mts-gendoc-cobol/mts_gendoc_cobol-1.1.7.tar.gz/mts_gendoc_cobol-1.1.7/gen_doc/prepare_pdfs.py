from fpdf import FPDF
import os
import logging
import sys
import argparse as ap
import re
import shutil
import tempfile
import subprocess
from pathlib import Path


def convert_md_to_pdf_fpdf(md_path: str, pdf_path: str, image_dir: str, logger, font_path: str = None):
    """Minimal markdown -> PDF converter using fpdf2.

    - Renders headings (#, ##, ###) as larger bold text
    - Renders code fences as monospaced blocks
    - Replaces image markdown `![](name.png)` by embedding the image (searches image_dir)
    - Wraps plain paragraphs
    This is intentionally small and not a full markdown renderer.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    # If a font_path (TTF) is provided, register it for Unicode support.
    use_custom_font = False
    if font_path:
        try:
            pdf.add_font('Custom', '', font_path, uni=True)
            pdf.set_font('Custom', size=12)
            use_custom_font = True
        except Exception as e:
            logger.warning('Failed to load custom font %s: %s. Falling back to builtin fonts.', font_path, e)
            pdf.set_font('Helvetica', size=12)
    else:
        pdf.set_font('Helvetica', size=12)

    def safe_text(s: str) -> str:
        # If custom Unicode font is available, return original text.
        if use_custom_font:
            return s
        # Otherwise replace characters outside Latin-1 with '?'
        return ''.join(ch if ord(ch) < 256 else '?' for ch in s)

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove leading outer fenced block like ``` or ```markdown to avoid code fence at top
    try:
        content = normalize_outer_markdown_wrapper(content)
    except Exception:
        pass

    lines = content.splitlines()
    in_code = False
    code_buf = []
    current_fence = None

    def ensure_x():
        # Ensure current X position leaves at least one character width available
        avail = pdf.w - pdf.r_margin - pdf.x
        if avail <= 1:
            pdf.ln(4)
            pdf.set_x(pdf.l_margin)
        return
    did_first_heading = False

    def wrapped_lines_count(pdf_obj, text, line_height):
        # Ensure x at left margin for consistent width calculation
        pdf_obj.set_x(pdf_obj.l_margin)
        usable_width = pdf_obj.w - pdf_obj.l_margin - pdf_obj.r_margin
        if usable_width <= 0:
            return 1
        # Use get_string_width which depends on current font
        width = pdf_obj.get_string_width(text)
        # Prevent zero division; estimate at least one line
        import math
        return max(1, math.ceil(width / usable_width))

    for idx in range(len(lines)):
        line = lines[idx]
        # If we're inside a code block but a markdown heading appears, assume the code block
        # was not intended to contain the heading (malformed fences) — close code block.
        if in_code and re.match(r'^(?P<hashes>#{1,6})\s*(?P<text>.*)', line):
            # flush code buf
            pdf.set_font('Courier', size=10)
            pdf.set_text_color(0, 0, 0)
            for cl in code_buf:
                ensure_x()
                pdf.multi_cell(0, 5, safe_text(cl))
            pdf.ln(2)
            pdf.set_font('Helvetica', size=12)
            in_code = False
            current_fence = None
            code_buf = []
        # detect fenced code blocks using exact fence string (``` or longer)
        fence_match = re.match(r'^(?P<fence>`{3,})(?:\s*(?P<lang>[^\s`]+)\s*)?$', line.lstrip())
        if fence_match:
            fence = fence_match.group('fence')
            if not in_code:
                in_code = True
                current_fence = fence
                code_buf = []
                continue
            else:
                # only close if the fence string matches the opener (exact match)
                if fence == current_fence:
                    # flush code buf
                    pdf.set_font('Courier', size=10)
                    pdf.set_text_color(0, 0, 0)
                    for cl in code_buf:
                        ensure_x()
                        pdf.multi_cell(0, 5, safe_text(cl))
                    pdf.ln(2)
                    pdf.set_font('Helvetica', size=12)
                    in_code = False
                    current_fence = None
                    continue
                else:
                    # a fence with different tick count inside a code block: treat as literal
                    code_buf.append(line)
                    continue

        if in_code:
            code_buf.append(line)
            continue

        # image replacement
        m = re.match(r'!\[.*?\]\((?P<img>[^)]+)\)', line.strip())
        if m:
            imgname = m.group('img')
            # look in image_dir then absolute
            imgpath = os.path.join(image_dir, imgname)
            if not os.path.exists(imgpath):
                if os.path.isabs(imgname) and os.path.exists(imgname):
                    imgpath = imgname
                else:
                    logger.warning('Image not found: %s', imgname)
                    continue
            # add image full width with aspect kept
            try:
                w = pdf.w - 2 * pdf.l_margin
                pdf.image(imgpath, x=None, y=None, w=w)
                pdf.ln(2)
                # reset X to left margin after placing a full-width image
                pdf.set_x(pdf.l_margin)
            except Exception as e:
                logger.error('Failed to add image %s: %s', imgpath, e)
            continue

        # headings
        h = re.match(r'^(?P<hashes>#{1,6})\s*(?P<text>.*)', line)
        if h:
            # Determine whether we need to keep the heading with the following content.
            level = len(h.group('hashes'))
            text = h.group('text')
            size = max(16 - level * 2, 10)

            # Look ahead for the next non-empty line to determine content type
            next_idx = idx + 1
            next_type = None
            next_text = ''
            # skip blank lines
            while next_idx < len(lines) and lines[next_idx].strip() == '':
                next_idx += 1
            if next_idx < len(lines):
                nxt = lines[next_idx]
                if nxt.strip().startswith('```'):
                    next_type = 'code'
                    # gather code block lines
                    j = next_idx + 1
                    code_lines = []
                    while j < len(lines) and not lines[j].strip().startswith('```'):
                        code_lines.append(lines[j])
                        j += 1
                    next_text = '\n'.join(code_lines) if code_lines else ''
                elif re.match(r'!\[.*?\]\((?P<img>[^)]+)\)', nxt.strip()):
                    next_type = 'image'
                    next_text = nxt.strip()
                elif re.match(r'^(?P<hashes>#{1,6})\s*(?P<text>.*)', nxt):
                    next_type = 'heading'
                    next_text = ''
                else:
                    next_type = 'paragraph'
                    next_text = nxt
            else:
                next_type = None

            # If next is heading or there is no next content, we don't need to keep-with-next
            need_keep_with_next = next_type in ('paragraph', 'code', 'image')

            if need_keep_with_next and did_first_heading:
                # measure required space: heading + at least one line of next content
                # set heading font for measurement
                pdf.set_font('Helvetica', 'B', size=size)
                ensure_x()
                heading_lines = wrapped_lines_count(pdf, safe_text(text), 7)

                # measure next content at its font
                if next_type == 'code':
                    pdf.set_font('Courier', size=10)
                    # approximate by summing wrapped lines for each code line
                    if next_text:
                        next_lines_count = 0
                        for cl in next_text.splitlines():
                            next_lines_count += wrapped_lines_count(pdf, safe_text(cl), 5)
                        next_lines = next_lines_count
                    else:
                        next_lines = 1
                    next_line_height = 5
                elif next_type == 'image':
                    # Try to compute the actual rendered image height for the PDF page
                    # so we can avoid orphaning the image. If Pillow is available,
                    # open the image and compute height preserving aspect ratio for
                    # the full-width rendering used later. Otherwise fall back to
                    # a conservative estimate.
                    img_match = re.match(r'!\[.*?\]\((?P<img>[^)]+)\)', next_text)
                    img_name = img_match.group('img') if img_match else None
                    display_h_mm = None
                    if img_name:
                        # resolve path relative to image_dir or absolute
                        img_path = os.path.join(image_dir, img_name)
                        if not os.path.exists(img_path) and os.path.isabs(img_name) and os.path.exists(img_name):
                            img_path = img_name
                        if os.path.exists(img_path):
                            try:
                                from PIL import Image
                                with Image.open(img_path) as im:
                                    iw, ih = im.size
                                    # PDF unit is mm here; approximate display width in mm
                                    display_w = pdf.w - 2 * pdf.l_margin
                                    # compute display height preserving aspect ratio
                                    display_h_mm = display_w * (ih / iw)
                            except Exception:
                                display_h_mm = None

                    if display_h_mm is None:
                        # conservative guess: 30 units (same unit scale as used earlier)
                        display_h_mm = 30

                    # Convert display height in mm to an approximate number of paragraph lines
                    # using paragraph line height (6 mm). Use at least 1 line.
                    import math
                    next_lines = max(1, math.ceil(display_h_mm / 6))
                    next_line_height = 6
                else:
                    pdf.set_font('Helvetica', size=12)
                    next_lines = wrapped_lines_count(pdf, safe_text(next_text), 6)
                    next_line_height = 6

                # compute required vertical space
                required = heading_lines * 7 + next_lines * next_line_height
                # remaining space on page
                remaining = pdf.h - pdf.b_margin - pdf.y
                if remaining < required:
                    pdf.add_page()
                    # reset base font on new page
                    if use_custom_font:
                        pdf.set_font('Custom', size=12)
                    else:
                        pdf.set_font('Helvetica', size=12)

            did_first_heading = True

            pdf.set_font('Helvetica', 'B', size=size)
            ensure_x()
            pdf.multi_cell(0, 7, safe_text(text))
            pdf.ln(1)
            pdf.set_font('Helvetica', size=12)
            continue

        # plain paragraph
        if line.strip() == '':
            pdf.ln(4)
        else:
            ensure_x()
            pdf.multi_cell(0, 6, safe_text(line))

    # final save
    # Write to a temporary file in the same directory then atomically replace.
    out_dir = os.path.dirname(pdf_path) or os.getcwd()
    try:
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False, dir=out_dir) as tf:
            tmp_pdf = tf.name
        # fpdf.output can accept a filename; let it write to tmp_pdf
        pdf.output(tmp_pdf)
        try:
            os.replace(tmp_pdf, pdf_path)
        except PermissionError:
            # attempt to remove the existing target and retry
            try:
                if os.path.exists(pdf_path):
                    os.remove(pdf_path)
                    os.replace(tmp_pdf, pdf_path)
                    return
            except Exception:
                # Couldn't remove or replace; fall back to a unique filename
                try:
                    fallback = pdf_path + f".new-{os.getpid()}-{int(tempfile.mkstemp()[1])}.pdf"
                except Exception:
                    fallback = pdf_path + ".new.pdf"
                try:
                    os.replace(tmp_pdf, fallback)
                    logger.error("Permission denied when writing '%s'. Output written to fallback path: %s", pdf_path, fallback)
                    return
                except Exception:
                    # give up and clean up
                    try:
                        os.remove(tmp_pdf)
                    except Exception:
                        pass
                    logger.error("Permission denied when writing '%s' and fallback path failed. Is the file open in another program?", pdf_path)
                    raise
    except PermissionError:
        # bubble up so caller can decide; log already written
        raise
    except Exception:
        # cleanup temp file if any other error occurred
        try:
            if 'tmp_pdf' in locals() and os.path.exists(tmp_pdf):
                os.remove(tmp_pdf)
        except Exception:
            pass
        raise


def normalize_outer_markdown_wrapper(content: str) -> str:
    """Remove an outer code-fence wrapper if it's an unlabeled fence or labeled 'markdown'."""
    def find_leading_markdown_fence(line: str):
        if line is None:
            return None
        l = line.lstrip('\ufeff').lstrip()
        m = re.match(r'^(?P<fence>`{3,})(?:\s*(?P<lang>[A-Za-z0-9_+-]+)\b)?', l, re.IGNORECASE)
        if not m:
            return None
        lang = m.groupdict().get('lang')
        if lang is None or lang.lower() == 'markdown':
            return m.group('fence')
        return None

    lines_list = content.splitlines()
    nonempty = [i for i, L in enumerate(lines_list) if L.strip() != '']
    if not nonempty:
        return content
    first_candidates = nonempty[:3]
    leading_idx = None
    leading_fence = None
    for idx in first_candidates:
        fence = find_leading_markdown_fence(lines_list[idx])
        if fence:
            leading_idx = idx
            leading_fence = fence
            break

    if leading_fence is not None:
        trailing_idx = None
        for idx in range(leading_idx + 1, len(lines_list)):
            if lines_list[idx].lstrip('\ufeff').lstrip().startswith(leading_fence):
                trailing_idx = idx
                break
        if trailing_idx is not None and trailing_idx > leading_idx:
            del lines_list[trailing_idx]
            del lines_list[leading_idx]
            return "\n".join(lines_list)
    return content

def find_mermaid_blocks(md_file_path, logger):
    """ Find mermaid code blocks in a markdown file and return (normalized_content, blocks).

    Returns:
      (content, blocks) where blocks is list of dicts with keys: full, code, start, end
    """
    logger.debug("Searching for mermaid blocks in file: %s", md_file_path)
    mermaid_blocks = []
    # Accept optional language suffix on the opening fence and CRLF variants
    pattern = re.compile(r"```mermaid\b[^\r\n]*\r?\n(.*?)\r?\n```", re.DOTALL | re.IGNORECASE)
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Normalize leading/trailing outer fences: remove an outer ``` or ```markdown wrapper
    def _find_leading_wrapper(lines):
        def find_leading_markdown_fence(line: str):
            if line is None:
                return None
            l = line.lstrip('\ufeff').lstrip()
            m = re.match(r'^(?P<fence>`{3,})(?:\s*(?P<lang>[A-Za-z0-9_+-]+)\b)?', l, re.IGNORECASE)
            if not m:
                return None
            lang = m.groupdict().get('lang')
            if lang is None or lang.lower() == 'markdown':
                return m.group('fence')
            return None

        lines_list = lines.splitlines()
        nonempty = [i for i, L in enumerate(lines_list) if L.strip() != '']
        if not nonempty:
            return lines
        first_candidates = nonempty[:3]
        leading_idx = None
        leading_fence = None
        for idx in first_candidates:
            fence = find_leading_markdown_fence(lines_list[idx])
            if fence:
                leading_idx = idx
                leading_fence = fence
                break

        if leading_fence is not None:
            # find the next occurrence of the same fence after the leading fence
            trailing_idx = None
            for idx in range(leading_idx + 1, len(lines_list)):
                if lines_list[idx].lstrip('\ufeff').lstrip().startswith(leading_fence):
                    trailing_idx = idx
                    break
            if trailing_idx is not None and trailing_idx > leading_idx:
                # delete trailing first, then leading
                del lines_list[trailing_idx]
                del lines_list[leading_idx]
                return "\n".join(lines_list)
        return lines

    content = _find_leading_wrapper(content)
    # return list of (match_text, start, end, code)
    for m in pattern.finditer(content):
        mermaid_blocks.append({
            'full': m.group(0),
            'code': m.group(1),
            'start': m.start(),
            'end': m.end(),
        })
    logger.debug("Found %d mermaid blocks in file: %s", len(mermaid_blocks), md_file_path)
    return content, mermaid_blocks


def sanitize_fences(content: str, logger) -> str:
    """Sanitize code fence issues in markdown content.

    - If content starts with a leading ```markdown (or unlabeled ```), remove that leading fence.
    - Ensure every opening fence has a closing fence. If an opening fence is missing a closer,
      append a closing fence at the end of the content.
    - Remove stray closing fences that don't have a matching opener.

    This aims to normalize inconsistent output coming from the LLM in prompt2 files.
    """
    lines = content.splitlines()
    # Remove a leading outer fence if present (unlabeled or labeled 'markdown')
    if lines:
        first = lines[0].lstrip('\ufeff').lstrip()
        m = re.match(r'^(?P<fence>`{3,})(?:\s*(?P<lang>[A-Za-z0-9_+-]+)\b)?', first, re.IGNORECASE)
        if m:
            lang = m.groupdict().get('lang')
            if lang is None or lang.lower() == 'markdown':
                logger.debug('Stripping leading outer fence from content')
                # remove the first line
                lines = lines[1:]

    # Now balance fences: track opening fences with their language (or None)
    fence_stack = []
    out_lines = []
    fence_re = re.compile(r'^(?P<fence>`{3,})(?:\s*(?P<lang>[^\s`]+)\s*)?$')
    for ln in lines:
        m = fence_re.match(ln.lstrip())
        if m:
            fence = m.group('fence')
            lang = m.group('lang')
            if fence_stack and fence_stack[-1] == fence:
                # closing fence for top of stack
                fence_stack.pop()
                out_lines.append(ln)
            else:
                # if this looks like an opening fence, push it
                # we treat any fence when stack empty or lang present as opener
                fence_stack.append(fence)
                out_lines.append(ln)
        else:
            out_lines.append(ln)

    # If any fences remain open, append closing fences to balance
    if fence_stack:
        logger.debug('Appending %d missing closing fence(s)', len(fence_stack))
        # close in LIFO order, but closing marker is just the fence chars
        for _ in range(len(fence_stack)):
            out_lines.append('```')

    # Remove leading stray closing fences at the very top (cases like starting with ``` then content)
    # Already handled earlier; this ensures no extra top closers
    # Also remove duplicated closers beyond those we just added: collapse sequences of closers
    return "\n".join(out_lines)

def main():
    """ Parse Arguments and invoke the planned flow """
    parser = ap.ArgumentParser(
        description="Generate PDFs from Markdown files."
    )
    parser.add_argument(
        "-i", "--input-dir",
        required=True,
        help="Directory containing Markdown files."
    )
    parser.add_argument(
        "-o", "--output-dir",
        required=True,
        help="Directory to save generated PDF files."
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging."
    )
    parser.add_argument(
        "--normalize-inplace",
        action="store_true",
        help="If set, normalize outer ```markdown wrappers in source .md files in-place before processing."
    )
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    verbose = args.verbose
    normalize_inplace = args.normalize_inplace

    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    logger = logging.getLogger(__name__)
    logger.info("Starting PDF generation process.")

    logger.info("Validating input directory : %s", input_dir)
    if not os.path.isdir(input_dir):
        logger.error("Input directory does not exist: %s", input_dir)
        sys.exit(1)
    
    logger.info("Ensuring output directory exists: %s", output_dir)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
        logger.info("Created output directory: %s", output_dir)
    
    logger.info("Path Validation Complete. Beginning PDF generation.")

    # navigate through each subdirectory in the parent
    for root, dirs, files in os.walk(input_dir):
        logger.info("Processing directory: %s", root)
        # only consider markdown files
        md_files = [f for f in sorted(files) if f.lower().endswith('.md')]
        for index, file in enumerate(md_files):
            logger.debug("Processing file: %s", file)
            md_file_path = os.path.join(root, file)
            # Optionally normalize the source file in-place to remove outer wrappers
            if normalize_inplace:
                with open(md_file_path, 'r', encoding='utf-8') as f:
                    original = f.read()
                normalized = normalize_outer_markdown_wrapper(original)
                if normalized != original:
                    logger.debug('Normalizing outer wrapper in %s', md_file_path)
                    with open(md_file_path, 'w', encoding='utf-8') as f:
                        f.write(normalized)
            # Next check the index of this file in the subdirectory
            if index == 0:
                # Deal with first file differetly
                logger.debug("First file in directory, applying special formatting.")
                # find mermaid code blocks and convert them to pngs, replacing the blocks inline
                content, blocks = find_mermaid_blocks(md_file_path, logger)

                if blocks:
                        # locate mmdc
                        path = shutil.which("mmdc.ps1") or shutil.which("mmdc.cmd") or shutil.which("mmdc")
                        if not path:
                            logger.error("Could not find 'mmdc' (mermaid-cli) on PATH. Skipping mermaid rendering for this file.")
                            path = None

                        # content already returned by find_mermaid_blocks (normalized)

                        # We will replace blocks in order from last to first to preserve indices
                        logger.debug("Converting %d mermaid blocks to images.", len(blocks))
                        images = []
                        for i, b in enumerate(reversed(blocks)):
                            code = b['code']
                            # generate output image name
                            png_name = f"{Path(file).stem}_mermaid_{i+1}.png"
                            png_path = os.path.join(output_dir, png_name)

                            # write temp mermaid file
                            with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as tf:
                                tf.write(code)
                                input_temp = tf.name

                            # build command
                            if path.lower().endswith('.ps1'):
                                cmd = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", path, "-i", input_temp, "-o", png_path]
                            else:
                                cmd = [path, "-i", input_temp, "-o", png_path]

                            proc = subprocess.run(cmd, capture_output=True, text=True)
                            if proc.returncode != 0:
                                logger.error("Mermaid CLI error for %s: %s", file, proc.stderr)
                                # remove temp input file and continue
                                try:
                                    os.remove(input_temp)
                                except Exception:
                                    pass
                                continue

                            images.append(png_path)
                            # replace the block in content (we are iterating reversed order)
                            content = content[:b['start']] + f"![]({png_name})" + content[b['end']:]
                            try:
                                os.remove(input_temp)
                            except Exception:
                                pass

                        # write a temporary markdown file with images in place
                        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tfmd:
                            tfmd.write(content)
                            temp_md = tfmd.name

                        # convert temp markdown to pdf using fpdf2
                        pdf_output_path = os.path.join(output_dir, f"{os.path.splitext(file)[0]}.pdf")
                        try:
                            logger.info("Converting File with Mermaid diagrams.")
                            convert_md_to_pdf_fpdf(temp_md, pdf_output_path, output_dir, logger)
                        finally:
                            try:
                                os.remove(temp_md)
                            except Exception:
                                pass
            elif index == 1:
                # sanitize second prompt outputs for inconsistent fences
                logger.debug('Sanitizing fences for second file: %s', md_file_path)
                with open(md_file_path, 'r', encoding='utf-8') as f:
                    original = f.read()
                sanitized = sanitize_fences(original, logger)
                # write sanitized content to a temp file and convert
                with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tfmd:
                    tfmd.write(sanitized)
                    temp_md = tfmd.name
                # Ensure we write prompt2 to its own PDF file
                pdf_output_path = os.path.join(output_dir, f"{os.path.splitext(file)[0]}.pdf")
                logger.debug('Temporary sanitized md saved to %s; converting to %s', temp_md, pdf_output_path)
                try:
                    convert_md_to_pdf_fpdf(temp_md, pdf_output_path, os.path.dirname(md_file_path), logger)
                finally:
                    try:
                        os.remove(temp_md)
                    except Exception:
                        pass
            else:
                logger.info("Converting File")
                # No mermaid blocks: convert original file directly
                pdf_output_path = os.path.join(output_dir, f"{os.path.splitext(file)[0]}.pdf")
                convert_md_to_pdf_fpdf(md_file_path, pdf_output_path, os.path.dirname(md_file_path), logger)


if __name__ == "__main__":
    main()

    

    # 2 method flow 
    # 1. Read all markdown files from input_dir
    # 2. Convert in certain ways depending on what file index they are
