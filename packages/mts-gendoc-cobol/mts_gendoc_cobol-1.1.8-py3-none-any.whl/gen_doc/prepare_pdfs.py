import os
import argparse
import shutil
import tempfile
import hashlib
from pathlib import Path
import subprocess
import io
import re

def _find_mermaid_blocks(md_text: str):
    """Find fenced ```mermaid blocks and replace them with placeholders.

    Returns (processed_md, entries) where entries is list of dicts with keys:
      - filename: suggested svg filename
      - code: mermaid diagram source
    """
    print("ENTERED _find_mermaid_blocks")
    pattern = re.compile(r"```mermaid\s*\n(.*?)\n```", re.DOTALL | re.IGNORECASE)
    entries = []
    def _make_filename(code: str, idx: int):
        h = hashlib.sha1(code.encode('utf-8')).hexdigest()[:8]
        return f"mermaid_{idx:03d}_{h}.png"

    def repl(m):
        code = m.group(1).strip()
        idx = len(entries) + 1
        filename = _make_filename(code, idx)
        entries.append({"filename": filename, "code": code})
        # Return a visible placeholder token so the converter preserves it in the storage XHTML
        return f"MERMAID_PLACEHOLDER:{filename}"

    processed = pattern.sub(repl, md_text)
    return processed, entries


def clean_markdown(md_text: str, remove_leading_markdown_tag: bool = True) -> str:
    """Normalize and balance markdown fences for the whole document.

    - If the document starts with a fence (``` or more) optionally followed
      by a language (e.g. markdown), the leading fence is removed.
    - A matching trailing fence of the same length is removed if present.
    - All remaining fences are balanced: unmatched opening fences get a
      closing fence appended; stray closing fences (when no opener) are
      skipped.
    """
    if not md_text:
        return md_text

    # Strip UTF-8 BOM
    if md_text.startswith('\ufeff'):
        md_text = md_text.lstrip('\ufeff')

    # Remove a single leading fence with optional language tag
    if remove_leading_markdown_tag:
        m = re.match(r"^\s*(`{3,})\s*(?:markdown|md)?\s*\n", md_text, re.IGNORECASE)
        if m:
            leading_ticks = m.group(1)
            md_text = md_text[m.end():]
            # Remove a matching trailing fence if present
            closing_re = re.compile(r"\n?^\s*" + re.escape(leading_ticks) + r"\s*$", re.MULTILINE)
            closings = list(closing_re.finditer(md_text))
            if closings:
                last = closings[-1]
                md_text = md_text[:last.start()] + md_text[last.end():]

    # Balance fences: treat any fence line starting with ticks as a fence,
    # using the exact tick count to match open/close.
    out_lines = []
    stack = []
    fence_line_re = re.compile(r"^\s*(`{3,})\s*.*$")
    for line in md_text.splitlines(keepends=True):
        m = fence_line_re.match(line)
        if m:
            ticks = m.group(1)
            if stack and stack[-1] == ticks:
                # matching closer
                stack.pop()
                out_lines.append(line)
            else:
                # opener
                stack.append(ticks)
                out_lines.append(line)
        else:
            out_lines.append(line)

    # Append closing fences for any unmatched openers
    while stack:
        last_ticks = stack.pop()
        if not out_lines or not out_lines[-1].endswith('\n'):
            out_lines.append('\n')
        out_lines.append(last_ticks + '\n')

    return ''.join(out_lines)

def render_mermaid_to_svg_cli(code: str, out_path: str) -> None:
    """Render mermaid source to an image (PNG) using the `mmdc` (mermaid-cli) tool.

    Requires: npm install -g @mermaid-js/mermaid-cli
    Writes output to out_path. Raises RuntimeError on failure.
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as tf:
        tf.write(code)
        input_path = tf.name

    # Try to find a usable mmdc executable/script on PATH. On Windows npm global
    # installs may provide one of: mmdc.ps1, mmdc.cmd, or mmdc
    path = shutil.which("mmdc.ps1") or shutil.which("mmdc.cmd") or shutil.which("mmdc")
    if not path:
        raise RuntimeError("Could not find 'mmdc' (mermaid-cli) on PATH. Install with: npm install -g @mermaid-js/mermaid-cli")

    # If we found a PowerShell script (.ps1), invoke via powershell.exe -File.
    if path.lower().endswith('.ps1'):
        cmd = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", path, "-i", input_path, "-o", out_path]
    else:
        # For .cmd/.exe or plain 'mmdc' command, invoke directly
        cmd = [path, "-i", input_path, "-o", out_path]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except FileNotFoundError as e:
        # powershell.exe or the script wasn't found
        raise RuntimeError(f"Could not execute PowerShell/mmdc script: {e}")

    if proc.returncode != 0:
        raise RuntimeError(f"mmdc invocation failed: returncode={proc.returncode}\nstdout:{proc.stdout}\nstderr:{proc.stderr}")

    return



def is_likely_text(data: bytes) -> bool:
    """Rudimentary check whether bytes look like text (not binary)."""
    if b"\x00" in data:
        return False
    try:
        data.decode("utf-8")
        return True
    except Exception:
        text_chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)))
        nontext = sum(1 for b in data if b not in text_chars)
        return (nontext / max(1, len(data))) < 0.30


def read_text_file_with_fallback(path: str) -> tuple[str, str]:
    """Read file trying UTF-8, then cp1252/latin-1. Returns (content, used_encoding)."""
    with open(path, "rb") as bf:
        head = bf.read(4096)
        if not is_likely_text(head):
            raise UnicodeDecodeError("binary", b"", 0, 1, "file appears binary")
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            with io.open(path, "r", encoding=enc, errors="strict") as f:
                return f.read(), enc
        except UnicodeDecodeError:
            continue
    with io.open(path, "r", encoding="latin-1", errors="replace") as f:
        return f.read(), "latin-1-replaced"


def fix_merm(input_dir: str) -> None:
    """Find mermaid code fences and ensure top-level bracket contents are wrapped in double quotes.

    This is the implementation copied from the project's `fix_merm.py` script but
    adapted to be called as a function with `input_dir` argument.
    """
    if not os.path.isdir(input_dir):
        print(f"Input directory does not exist: {input_dir}")
        return

    merm_block = re.compile(r"```mermaid\s*\n(.*?)\n```", re.DOTALL | re.IGNORECASE)

    for root, dirs, files in os.walk(input_dir):
        print("Walking through directory:", root)
        for target_file in files:
            file_path = os.path.join(root, target_file)
            print(" Processing file:", file_path)
            try:
                content, used_enc = read_text_file_with_fallback(file_path)
            except UnicodeDecodeError:
                print(f"  Skipping binary or unreadable file: {file_path}")
                continue
            except Exception as e:
                print(f"  Error reading {file_path}: {e}")
                continue

            matches = merm_block.findall(content)
            if not matches:
                continue

            new_content = content
            for match in matches:
                print("  Found MERM block (first 120 chars):", match[:120].replace('\n', '\\n'))
                fixed_lines = []
                for line in match.splitlines():
                    if any(char in line for char in '()[]{}'):
                        def quote_top_level_pairs(s: str) -> str:
                            opens = {'(': ')', '[': ']', '{': '}'}
                            if not any(ch in s for ch in '()[]{}'):
                                return s
                            out = []
                            i = 0
                            L = len(s)
                            while i < L:
                                ch = s[i]
                                if ch in opens:
                                    open_ch = ch
                                    close_ch = opens[ch]
                                    depth = 1
                                    j = i + 1
                                    while j < L and depth > 0:
                                        if s[j] == open_ch:
                                            depth += 1
                                        elif s[j] == close_ch:
                                            depth -= 1
                                            if depth == 0:
                                                break
                                        j += 1
                                    if j >= L or depth != 0:
                                        out.append(ch)
                                        i += 1
                                        continue
                                    inner = s[i+1:j]
                                    inner_stripped = inner.replace('"', '')
                                    out.append(open_ch)
                                    out.append('"')
                                    out.append(inner_stripped)
                                    out.append('"')
                                    out.append(close_ch)
                                    i = j + 1
                                else:
                                    out.append(ch)
                                    i += 1
                            return ''.join(out)

                        fixed_line = quote_top_level_pairs(line).rstrip()
                        fixed_lines.append(fixed_line)
                    else:
                        fixed_lines.append(line)
                fixed_block = "\n".join(fixed_lines)
                new_content = new_content.replace(match, fixed_block)

            if new_content != content:
                try:
                    with io.open(file_path, "w", encoding=used_enc, errors="replace") as wf:
                        wf.write(new_content)
                    print(f"  Updated file (encoding={used_enc})")
                except Exception as e:
                    print(f"  Failed to write {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generate PDFs from Markdown files recursively.")
    parser.add_argument(
        "-i", "--input-dir", help="Path to the input directory containing Markdown files", required=True)
    parser.add_argument(
        "-o", "--output-dir", help="Path to the output directory for generated PDFs", required=True)
    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    if not os.path.isdir(input_dir):
        print(f"Input directory does not exist: {input_dir}")
        return
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Build the command
    command = shutil.which("md-to-pdf")
    if command is None:
        print("md-to-pdf command not found. Please install it first.")
        return
    
    arglist = []
    if command.lower().endswith(".ps1"):
        arglist = ["powershell", "-File", command]
    else:
        arglist = [command]
    
    # Flow of this program 
    # 1. Fix all mermaid that we can 
    # 2. generate pdfs 
    # 3. add unique handling for pdfs that contain mermaid code
    fix_merm(input_dir)
    for root, dirs, files in os.walk(input_dir):
        for target_file in files:
            if target_file.lower().endswith(".md"):
                input_path = os.path.join(root, target_file)
                with open(input_path, "r", encoding="utf-8", errors="replace") as f:
                    md_text = f.read()
                # Always clean markdown fences for each file before further processing
                cleaned = clean_markdown(md_text, remove_leading_markdown_tag=True)
                processed_md, mermaid_entries = _find_mermaid_blocks(cleaned)

                temp_workdir = None
                try:
                    if mermaid_entries:
                        print(f"Generating PDF with mermaid diagrams for: {input_path}")
                        # Create one temporary work directory; images and tmp md will live here
                        temp_workdir = tempfile.mkdtemp()
                        print(f"[DEBUG] Created temp_workdir: {temp_workdir}")
                        # Render each mermaid entry to a PNG file inside temp_workdir and replace placeholder
                        for entry in mermaid_entries:
                            filename = entry['filename']
                            code = entry['code']
                            out_path = os.path.join(temp_workdir, filename)
                            try:
                                print(f"[DEBUG] Rendering mermaid to: {out_path}")
                                render_mermaid_to_svg_cli(code, out_path)
                                print(f"[DEBUG] Rendered {filename}: exists={os.path.exists(out_path)}, size={os.path.getsize(out_path) if os.path.exists(out_path) else 'n/a'}")
                            except Exception as e:
                                print(f"  Error rendering mermaid diagram {filename}: {e}")
                                # leave placeholder in place and continue
                                continue
                            # Use relative filename so markdown references image next to the md file
                            processed_md = processed_md.replace(f"MERMAID_PLACEHOLDER:{filename}", f"![{filename}]({filename})")

                        # Ensure headings stay with following images: wrap heading+image in a keep-together div
                        def _wrap_heading_with_image(md: str) -> str:
                            style = '<style> .keep-together { page-break-inside: avoid; break-inside: avoid; display: block; }</style>\n\n'
                            # Find markdown heading followed immediately by a markdown image and
                            # replace with HTML: a div with an <hN> and an <img> so the heading
                            # renders correctly even inside the HTML block.
                            pattern = re.compile(r'(?m)^(?P<head>#{1,6}\s*[^\n]+)\s*\n\s*(?P<img>!\[[^\]]*\]\([^\)]+\))')
                            def repl(m):
                                head = m.group('head').strip()
                                img = m.group('img').strip()
                                # parse heading level and text
                                hm = re.match(r'^(?P<hashes>#{1,6})\s*(?P<text>.*)$', head)
                                if hm:
                                    level = min(6, len(hm.group('hashes')))
                                    htext = hm.group('text').strip()
                                else:
                                    level = 2
                                    htext = head
                                # parse image markdown
                                im = re.match(r'^!\[(?P<alt>[^\]]*)\]\((?P<src>[^\)]+)\)$', img)
                                if im:
                                    alt = im.group('alt')
                                    src = im.group('src')
                                else:
                                    alt = ''
                                    src = ''
                                # Return HTML block with heading and image tag
                                return f'<div class="keep-together">\n<h{level}>{htext}</h{level}>\n\n<img src="{src}" alt="{alt}" />\n</div>'

                            new_md = pattern.sub(repl, md)
                            if new_md is md:
                                return style + md
                            return style + new_md

                        # Write processed markdown to a temporary file inside the same workdir for conversion
                        tmpmd_path = os.path.join(temp_workdir, "document.md")
                        with open(tmpmd_path, mode='w', encoding='utf-8') as tmpmd:
                            tmpmd.write(_wrap_heading_with_image(processed_md))
                        print(f"[DEBUG] Wrote temp markdown: {tmpmd_path}")
                        print(f"[DEBUG] Temp workdir listing: {os.listdir(temp_workdir)}")
                        run_target = tmpmd_path
                    else:
                        print(f"Generating PDF for: {input_path}")
                        run_target = input_path

                    # Build a flat argument list for subprocess.run: command args + input path
                    if temp_workdir:
                        run_args = arglist + [os.path.basename(run_target)]
                        print(f"[DEBUG] Running md-to-pdf: {run_args}  (cwd={temp_workdir})")
                        proc = subprocess.run(run_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=temp_workdir)
                    else:
                        run_args = arglist + [run_target]
                        print(f"[DEBUG] Running md-to-pdf: {run_args}  (cwd={os.getcwd()})")
                        proc = subprocess.run(run_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    if proc.returncode != 0:
                        print(f"Error generating PDF for {input_path}: {proc.stderr}")
                        continue
                    # On success, try to find the produced PDF and move it to output_dir
                    # Preserve input directory structure under the output dir
                    # Possible locations: next to run_target, next to original input_path, or cwd
                    candidates = []
                    candidates.append(os.path.splitext(run_target)[0] + ".pdf")
                    candidates.append(os.path.splitext(input_path)[0] + ".pdf")
                    candidates.append(os.path.join(os.getcwd(), os.path.basename(os.path.splitext(run_target)[0] + ".pdf")))
                    moved = False
                    print(f"[DEBUG] PDF candidates: {candidates}")
                    for cand in candidates:
                        print(f"[DEBUG] Checking candidate: {cand} exists={os.path.exists(cand)}")
                        if os.path.exists(cand):
                            # compute destination path preserving relative path from input_dir
                            try:
                                rel = os.path.relpath(input_path, input_dir)
                            except Exception:
                                rel = os.path.basename(input_path)
                            rel_pdf = os.path.splitext(rel)[0] + ".pdf"
                            dest = os.path.join(output_dir, rel_pdf)
                            dest_dir = os.path.dirname(dest)
                            if not os.path.exists(dest_dir):
                                os.makedirs(dest_dir, exist_ok=True)
                            try:
                                shutil.move(cand, dest)
                                print(f"Moved generated PDF to: {dest}")
                                moved = True
                                break
                            except Exception as e:
                                print(f"Failed to move PDF {cand} -> {dest}: {e}")
                                # try next candidate
                    if not moved:
                        print(f"Warning: could not locate generated PDF for {input_path}; looked at: {candidates}")
                finally:
                    # Clean up temporary working directory (contains images and tmp md)
                    if temp_workdir and os.path.exists(temp_workdir):
                        try:
                            shutil.rmtree(temp_workdir)
                        except Exception:
                            pass
    


if __name__ == "__main__":
    main()



