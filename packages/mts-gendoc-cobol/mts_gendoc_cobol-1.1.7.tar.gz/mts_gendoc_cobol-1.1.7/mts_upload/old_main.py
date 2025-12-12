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
        for md_path in md_files:
            md_text = md_path.read_text(encoding="utf-8")
            # 1) Markdown -> HTML
            html = markdown.markdown(md_text, extensions=["tables", "fenced_code"])  # add more extensions as needed
            # 2) HTML (editor repr) -> STORAGE via Confluence convert API
            storage_xhtml = convert_editor_html_to_storage(html)
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
