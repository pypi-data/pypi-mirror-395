import os
from pathlib import Path
import base64
import json
import time
import requests
import markdown
import argparse as ap
from typing import Optional, List
import sys
import re
import tempfile
import subprocess
import hashlib
# ====== USER SETTINGS ======
CONFLUENCE_BASE = "https://wiki.aciworldwide.com"  # no trailing slash
USERNAME = ""
PASSWORD = ""         # Prefer ENV var in practice
SPACE_KEY = "RTPS"                  # your target space
PARENT_PAGE_ID = "775340390"        
ROOT_DIR = Path("OUTPUT/entry_subs")
DRY_RUN = False                     # True = don't call API, just print plan
# ===========================

SESSION = requests.Session()
AUTH = (USERNAME, PASSWORD)
HEADERS_JSON = {"Accept": "application/json", "Content-Type": "application/json"}

def log(msg: str):
    print(msg, flush=True)

def expand_block(title: str, storage_body: str) -> str:
    return f"""
<ac:structured-macro ac:name="expand" ac:schema-version="1">
  <ac:parameter ac:name="title">{title}</ac:parameter>
  <ac:rich-text-body>
    {storage_body}
  </ac:rich-text-body>
</ac:structured-macro>
""".strip()

def compose_page_body(subdir_title: str, expand_blocks: List[str]) -> str:
    heading = f"<h2>{subdir_title}</h2>"
    return heading + "\n" + "\n".join(expand_blocks)

def convert_editor_html_to_storage(html: str) -> str:
    """
    Uses Confluence DC/Server REST: POST /rest/api/contentbody/convert/storage
    Body: { "value": html, "representation": "editor" }
    Returns 'value' (storage XHTML).
    """
    url = f"{CONFLUENCE_BASE}/rest/api/contentbody/convert/storage"
    payload = {"value": html, "representation": "editor","minorEdit":True}
    r = SESSION.post(url, auth=AUTH, headers=HEADERS_JSON, data=json.dumps(payload))
    if not r.ok:
        raise RuntimeError(f"Convert API failed: {r.status_code} {r.text}")
    return r.json()["value"]  # storage XHTML
    # Ref: Confluence Data Center REST content-body convert supports editor->storage.  cite: turn1search22

def get_page_by_title(space_key: str, title: str):
    url = f"{CONFLUENCE_BASE}/rest/api/content"
    params = {"spaceKey": space_key, "title": title, "expand": "version"}
    r = SESSION.get(url, auth=AUTH, headers={"Accept": "application/json"}, params=params)
    if not r.ok:
        raise RuntimeError(f"get_page_by_title failed: {r.status_code} {r.text}")
    data = r.json()
    if data.get("size", 0) > 0:
        return data["results"][0]
    return None


def _find_mermaid_blocks(md_text: str):
    """Find fenced ```mermaid blocks and replace them with placeholders.

    Returns (processed_md, entries) where entries is list of dicts with keys:
      - filename: suggested svg filename
      - code: mermaid diagram source
    """
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


def render_mermaid_to_svg_cli(code: str, out_path: str) -> None:
    """Render mermaid source to an image (PNG) using the `mmdc` (mermaid-cli) tool.

    Requires: npm install -g @mermaid-js/mermaid-cli
    Writes output to out_path. Raises RuntimeError on failure.
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as tf:
        tf.write(code)
        input_path = tf.name

    # Invoke the mmdc PowerShell script explicitly (user requested PowerShell attempt).
    cmd = [
        "powershell.exe",
        "-File",
        r"C:\Users\bastianellib\AppData\Roaming\npm\mmdc.ps1",
        "-i",
        input_path,
        "-o",
        out_path,
    ]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except FileNotFoundError as e:
        # powershell.exe or the script wasn't found
        raise RuntimeError(f"Could not execute PowerShell/mmdc script: {e}")

    if proc.returncode != 0:
        raise RuntimeError(f"mmdc invocation failed: returncode={proc.returncode}\nstdout:{proc.stdout}\nstderr:{proc.stderr}")

    return


def upload_attachment(page_id: str, filename: str, data: bytes):
    """Upload an attachment to a Confluence page. Returns the API response JSON."""
    url = f"{CONFLUENCE_BASE}/rest/api/content/{page_id}/child/attachment"
    headers = {"X-Atlassian-Token": "no-check"}
    files = {'file': (filename, data, 'image/png')}
    r = SESSION.post(url, auth=AUTH, headers=headers, files=files)
    if not r.ok:
        raise RuntimeError(f"upload_attachment failed: {r.status_code} {r.text}")
    return r.json()


def _make_attachment_image_macro(filename: str) -> str:
    # storage format macro referencing an attachment by filename on the same page
    return f'<ac:image><ri:attachment ri:filename="{filename}" /></ac:image>'

def create_page(space_key: str, title: str, parent_id: Optional[str], storage_body: str):
    url = f"{CONFLUENCE_BASE}/rest/api/content"
    body = {
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "body": {"storage": {"value": storage_body, "representation": "storage"}},
    }
    if parent_id:
        body["ancestors"] = [{"id": int(parent_id)}]

    r = SESSION.post(url, auth=AUTH, headers=HEADERS_JSON, data=json.dumps(body))
    if not r.ok:
        raise RuntimeError(f"create_page failed: {r.status_code} {r.text}")
    return r.json()["id"]

def update_page(page_id: str, title: str, space_key: str, parent_id: Optional[str], storage_body: str, current_version: int):
    url = f"{CONFLUENCE_BASE}/rest/api/content/{page_id}"
    body = {
        "id": page_id,
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "version": {"number": current_version + 1},
        "body": {"storage": {"value": storage_body, "representation": "storage"}},
    }
    if parent_id:
        body["ancestors"] = [{"id": int(parent_id)}]

    r = SESSION.put(url, auth=AUTH, headers=HEADERS_JSON, data=json.dumps(body))
    if not r.ok:
        raise RuntimeError(f"update_page failed: {r.status_code} {r.text}")
    return r.json()["id"]


def main():
    global DRY_RUN, ROOT_DIR, PARENT_PAGE_ID, USERNAME, PASSWORD
    parser = ap.ArgumentParser(description="Publish Markdown files as Confluence pages with expands.")
    parser.add_argument("--dry-run", action="store_true", help="If set, do not call Confluence API, just print plan.")
    parser.add_argument("--root-dir", type=str, default=str(ROOT_DIR), help="Root directory containing subdirectories with .md files.")
    parser.add_argument("--parent-page-id", type=str, default=PARENT_PAGE_ID, help="Parent page ID in Confluence.")
    parser.add_argument("--username", type=str, default=USERNAME, help="Confluence username.")
    parser.add_argument("--password", type=str, default=PASSWORD, help="Confluence password.")
    parser.add_argument("-l", "--log", action="store_true", help="Enable logging to see payloads and information used to send API requests")
    args = parser.parse_args()
    
    DRY_RUN = args.dry_run
    ROOT_DIR = Path(args.root_dir)
    PARENT_PAGE_ID = args.parent_page_id
    USERNAME = args.username
    PASSWORD = args.password

    # Update AUTH and session auth after parsing credentials
    global AUTH
    AUTH = (USERNAME, PASSWORD)
    SESSION.auth = AUTH

    # Require credentials unless doing a dry-run
    if not DRY_RUN and (not USERNAME or not PASSWORD):
        parser.error("USERNAME and PASSWORD are required unless --dry-run is set")

    if(args.log):
        import http.client as http_client
        http_client.HTTPConnection.debuglevel = 1

        import logging
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
    
    log(f"Starting publish_md_expands.py with root_dir={ROOT_DIR}, parent_page_id={PARENT_PAGE_ID}, dry_run={DRY_RUN}")
    for subdir in sorted(p for p in ROOT_DIR.iterdir() if p.is_dir()):
        subdir_title = subdir.name
        log(f"\nProcessing: {subdir_title}")

        md_files = sorted(subdir.glob("*.md"))
        if not md_files:
            log("  (no .md files found)")
            continue

        expand_blocks = []

        # If not a dry run, ensure the target page exists (create placeholder if necessary)
        page_pid = None
        page_current_version = None
        if not DRY_RUN:
            existing_page = get_page_by_title(SPACE_KEY, subdir_title)
            if existing_page:
                page_pid = existing_page["id"]
                page_current_version = existing_page["version"]["number"]
                log(f"  Found existing page for uploads: id={page_pid}, version={page_current_version}")
            else:
                # Create a minimal placeholder page so we can attach files to it
                placeholder_body = f"<h2>{subdir_title}</h2><p>Preparing content...</p>"
                page_pid = create_page(SPACE_KEY, subdir_title, PARENT_PAGE_ID, placeholder_body)
                page_current_version = 1
                log(f"  Created placeholder page for uploads: id={page_pid}")

        for md_path in md_files:
            md_text = md_path.read_text(encoding="utf-8")
            
            # Normalize fences for every markdown file: remove an outer wrapper fence (3+ backticks, optional 'markdown')
            # that appears near the start and a matching closing fence near the end. This avoids leaving
            # leading ```markdown and trailing ``` markers in the processed content.
            lines = md_text.splitlines()

            def find_leading_markdown_fence(line: str) -> Optional[str]:
                if line is None:
                    return None
                l = line.lstrip('\ufeff').lstrip()
                m = re.match(r'^(?P<fence>`{3,})(?:\s*markdown\b)?', l, re.IGNORECASE)
                if m:
                    return m.group('fence')
                return None

            def is_code_fence_of_any(line: str) -> bool:
                if line is None:
                    return False
                l = line.lstrip('\ufeff').lstrip()
                return bool(re.match(r'^`{3,}', l))

            # Look for an outer fence within the first/last 3 non-empty lines
            nonempty = [i for i, L in enumerate(lines) if L.strip() != '']
            first_candidates = nonempty[:3]
            last_candidates = nonempty[-3:]
            leading_idx = None
            leading_fence = None
            for idx in first_candidates:
                fence = find_leading_markdown_fence(lines[idx])
                if fence:
                    leading_idx = idx
                    leading_fence = fence
                    break

            if leading_fence is not None:
                # find a matching trailing fence in the last candidates
                trailing_idx = None
                for idx in reversed(last_candidates):
                    if lines[idx].lstrip('\ufeff').lstrip().startswith(leading_fence):
                        trailing_idx = idx
                        break
                if trailing_idx is not None and trailing_idx > leading_idx:
                    # delete trailing first, then leading
                    del lines[trailing_idx]
                    del lines[leading_idx]
            else:
                # fallback: remove trailing code-fence lines of any 3+ backticks
                while lines and is_code_fence_of_any(lines[-1]):
                    lines.pop()

            md_text = "\n".join(lines)
            
            # Preprocess mermaid blocks: detect, render to SVG, upload as attachments, replace with image macros
            processed_md, mermaid_entries = _find_mermaid_blocks(md_text)

            # For each mermaid entry, render and (if not dry-run) upload to a temporary page placeholder
            attachment_macros = {}
            for entry in mermaid_entries:
                filename = entry['filename']
                code = entry['code']
                if DRY_RUN:
                    log(f"    [DRY-RUN] Would render mermaid diagram and upload as {filename}")
                    attachment_macros[filename] = _make_attachment_image_macro(filename)
                    continue

                # Render to temp file then upload
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmpf:
                    out_path = tmpf.name
                try:
                    render_mermaid_to_svg_cli(code, out_path)
                    data = Path(out_path).read_bytes()
                except Exception as e:
                    log(f"    Error rendering mermaid diagram {filename}: {e}")
                    continue

                # Upload to the actual page so the attachment is found by the image macro
                try:
                    if page_pid is None:
                        # Fallback: upload to parent if we somehow don't have a page id
                        target_upload_pid = PARENT_PAGE_ID
                    else:
                        target_upload_pid = page_pid
                    upload_resp = upload_attachment(target_upload_pid, filename, data)
                    attachment_macros[filename] = _make_attachment_image_macro(filename)
                    log(f"    Uploaded mermaid PNG as attachment: {filename} (page id={target_upload_pid})")
                except Exception as e:
                    log(f"    Failed to upload attachment {filename}: {e}")

            # 1) Markdown -> HTML (processed still contains visible placeholders)
            html = markdown.markdown(processed_md, extensions=["tables", "fenced_code"])  # add more extensions as needed
            # 2) HTML (editor repr) -> STORAGE via Confluence convert API
            storage_xhtml = convert_editor_html_to_storage(html)

            # Replace placeholder tokens in the storage XHTML with storage-format image macros
            for fname, macro in attachment_macros.items():
                storage_xhtml = storage_xhtml.replace(f"MERMAID_PLACEHOLDER:{fname}", macro)
            # 3) Wrap in Expand
            expand_blocks.append(expand_block(md_path.stem, storage_xhtml))
            log(f"  Prepared expand for: {md_path.name}")

        page_body = compose_page_body(subdir_title, expand_blocks)

        if DRY_RUN:
            log(f"  [DRY-RUN] Would upsert page '{subdir_title}' under parent {PARENT_PAGE_ID} "
                f"in space '{SPACE_KEY}' with {len(expand_blocks)} expands")
            continue

        # Upsert
        existing = get_page_by_title(SPACE_KEY, subdir_title)
        if existing:
            pid = existing["id"]
            ver = existing["version"]["number"]
            update_page(pid, subdir_title, SPACE_KEY, PARENT_PAGE_ID, page_body, ver)
            log(f"  Page updated: {subdir_title} (id={pid})")
        else:
            pid = create_page(SPACE_KEY, subdir_title, PARENT_PAGE_ID, page_body)
            log(f"  Page created: {subdir_title} (id={pid})")

if __name__ == "__main__":
    main()
