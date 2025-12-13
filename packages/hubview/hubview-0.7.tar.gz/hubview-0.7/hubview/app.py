#!/usr/bin/env python3
"""
LocalHub — a GitHub like file viewer for local folders (Flask)
Features
- Clean, responsive UI with dark/light support
- Directory browsing with breadcrumbs
- Markdown rendering (GitHub ish) incl. tables, task lists, admonitions
- Mermaid diagrams in fenced blocks ```mermaid
- Syntax highlighting (highlight.js) for code (server serves plain text, client highlights)
- Renders photos/images directly, plus audio/video and PDFs
- README.md auto renders at the bottom of directory listings (like GitHub)
- Safe path handling (jailed to a configured ROOT)
"""
from __future__ import annotations

import os, re, csv, json, mimetypes, posixpath, uuid, threading, signal
import mimetypes
import posixpath
from datetime import datetime
from pathlib import Path
from typing import List, Tuple
import argparse
import pandas as pd
from typing import List, Tuple, Optional, Dict, Any
import yaml
from dataclasses import dataclass
from typing import Optional, Dict
import sys


# New
from flask import (
    Flask,
    render_template,
    abort,
    send_from_directory,
    request,
    url_for,
    redirect,
    jsonify,
    Response,
)
from markupsafe import Markup
from werkzeug.utils import safe_join
import csv
import markdown
from bs4 import BeautifulSoup  # for rewriting relative links in rendered markdown
from pymdownx.superfences import fence_div_format
from .scripting.script_server import ScriptRunner, ScriptManager

# --------------------------- Configuration ----------------------------------


def detect_root() -> str:
    env = os.environ.get("FFV_ROOT")
    if env:
        return os.path.abspath(env)
    # Default to current working directory
    return os.path.abspath(os.getcwd())


ROOT_DIR = detect_root()

APP_TITLE = "HubView"
APP_SUBTITLE = ""

# Execution feature is opt-in
ALLOW_EXEC = False

# Jobs log file (JSON Lines)
JOBS_LOG = os.path.join(os.path.expanduser("~"), ".localhub_jobs.jsonl")

# Filetype groups
MARKDOWN_EXTS = {".md", ".markdown", ".mdown"}
IMAGE_EXTS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".webp",
    ".bmp",
    ".ico",
    ".tif",
    ".tiff",
}
VIDEO_EXTS = {".mp4", ".webm", ".ogg", ".mov", ".m4v"}
AUDIO_EXTS = {".mp3", ".wav", ".ogg", ".m4a", ".flac", ".aac"}
PDF_EXTS = {".pdf"}
CSV_EXTS = {".csv", ".tsv"}
EXCEL_EXTS = {".xlsx", ".xls"}
TEXT_EXTS = {
    ".txt",
    ".csv",
    ".tsv",
    ".py",
    ".js",
    ".ts",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".env",
    ".html",
    ".css",
    ".scss",
    ".less",
    ".xml",
    ".sh",
    ".bat",
    ".ps1",
    ".go",
    ".rs",
    ".rb",
    ".java",
    ".kt",
    ".swift",
    ".m",
    ".mm",
    ".cs",
    ".sql",
    ".dockerfile",
    ".makefile",
    ".gradle",
    ".tex",
    ".rst",
    ".log",
}

LANG_BY_EXT = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "c",
    ".hpp": "cpp",
    ".json": "json",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".toml": "toml",
    ".ini": "ini",
    ".cfg": "ini",
    ".html": "xml",
    ".xml": "xml",
    ".css": "css",
    ".scss": "scss",
    ".less": "less",
    ".sh": "bash",
    ".bat": "dos",
    ".ps1": "powershell",
    ".go": "go",
    ".rs": "rust",
    ".rb": "ruby",
    ".java": "java",
    ".kt": "kotlin",
    ".swift": "swift",
    ".m": "objectivec",
    ".mm": "objectivec",
    ".cs": "csharp",
    ".sql": "sql",
    ".tex": "latex",
    ".rst": "rst",
}

IGNORE_NAMES = {
    "__pycache__",
    ".git",
    ".hg",
    ".svn",
    ".DS_Store",
    "Thumbs.db",
}


def list_directory(abs_dir: str):
    try:
        entries = []
        with os.scandir(abs_dir) as it:
            for e in it:
                name = e.name
                # skip if name is ignored (applies to both files AND folders)
                if name in IGNORE_NAMES:
                    continue

                is_dir = e.is_dir(follow_symlinks=False)
                try:
                    st = e.stat(follow_symlinks=False)
                except (FileNotFoundError, PermissionError):
                    st = None

                entries.append(
                    {
                        "name": name,
                        "is_dir": is_dir,
                        "size": None if is_dir or not st else st.st_size,
                        "mtime": (
                            None if not st else datetime.fromtimestamp(st.st_mtime)
                        ),
                        "ext": "" if is_dir else Path(name).suffix.lower(),
                        "hidden": name.startswith("."),
                    }
                )
        entries.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
        return entries
    except FileNotFoundError:
        abort(404)


def is_within_root(path: str) -> bool:
    try:
        Path(path).resolve().relative_to(Path(ROOT_DIR).resolve())
        return True
    except Exception:
        return False


def to_abs(rel_path: str | None) -> str:
    if not rel_path:
        rel_path = ""
    # Always use POSIX paths in URLs, convert to FS paths here
    safe_path = safe_join(ROOT_DIR, rel_path)
    if safe_path is None:
        abort(404)
    safe_path = os.path.abspath(safe_path)
    if not is_within_root(safe_path):
        abort(404)
    return safe_path


def make_breadcrumbs(rel_path: str) -> List[Tuple[str, str]]:
    parts = [p for p in rel_path.split("/") if p]
    crumbs = [("root", url_for("browse", path=""))]
    acc = []
    for p in parts:
        acc.append(p)
        crumbs.append((p, url_for("browse", path="/".join(acc))))
    return crumbs


def human_size(num_bytes: int) -> str:
    step = 1024.0
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num_bytes < step:
            return (
                f"{num_bytes:,.0f} {unit}"
                if unit == "B"
                else f"{num_bytes/step:.1f} {unit}"
            )
        num_bytes /= step
    return f"{num_bytes:.1f} PB"


def list_directory(abs_dir: str):
    try:
        entries = []
        with os.scandir(abs_dir) as it:
            for e in it:
                name = e.name
                if name in IGNORE_NAMES:  # skip only explicit names
                    continue

                is_dir = e.is_dir(follow_symlinks=False)
                try:
                    st = e.stat(follow_symlinks=False)
                except (FileNotFoundError, PermissionError):
                    # Entry vanished or not accessible; show as 0 size
                    st = None

                entries.append(
                    {
                        "name": name,
                        "is_dir": is_dir,
                        "size": None if is_dir or not st else st.st_size,
                        "mtime": (
                            None if not st else datetime.fromtimestamp(st.st_mtime)
                        ),
                        "ext": "" if is_dir else Path(name).suffix.lower(),
                        "hidden": name.startswith("."),  # kept, so you can style it
                        "path": name,  # add if you need links
                    }
                )
        entries.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
        return entries
    except FileNotFoundError:
        abort(404)


def build_markdown_renderer():
    return markdown.Markdown(
        extensions=[
            "extra",  # includes abbr, attr_list, def_list, fenced_code, tables
            "admonition",
            "sane_lists",
            "toc",
            "pymdownx.details",
            "pymdownx.tasklist",
            "pymdownx.emoji",
            "pymdownx.superfences",
            "pymdownx.highlight",
        ],
        extension_configs={
            "pymdownx.highlight": {
                "use_pygments": False,  # let highlight.js handle it
                "anchor_linenums": False,
            },
            "pymdownx.superfences": {
                "custom_fences": [
                    # Allow ```mermaid fenced blocks to render as <div class="mermaid">…</div>
                    {"name": "mermaid", "class": "mermaid", "format": fence_div_format},
                ]
            },
            "pymdownx.emoji": {
                "emoji_generator": "github",  # GitHub‑style emoji shortcodes
            },
        },
        output_format="html5",
        tab_length=4,
    )


def is_url_like(href: str) -> bool:
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", href))


def rewrite_relative_links(html: str, current_dir_rel: str) -> str:
    """
    For rendered Markdown: adjust relative links to route through our Flask views.
    - <img src="pic.png">  => /raw/{current_dir}/pic.png
    - <a href="file.md">   => /view/{current_dir}/file.md
    - <a href="#section">  => unchanged (in‑page anchors)
    - Absolute URLs (http:, mailto:, etc.) unchanged
    """
    soup = BeautifulSoup(html, "html.parser")

    def _join(rel):
        # normalize POSIX path
        joined = posixpath.normpath(posixpath.join(current_dir_rel, rel)).lstrip("/")
        return joined

    # images and media
    for tag in soup.find_all(["img", "source", "video", "audio"]):
        attr = "src"
        if tag.has_attr(attr):
            src = tag.get(attr, "")
            if (
                src
                and not src.startswith("/")
                and not is_url_like(src)
                and not src.startswith("#")
            ):
                tag[attr] = url_for("raw_file", path=_join(src))

    # links
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if (
            not href
            or href.startswith("#")
            or href.startswith("/")
            or is_url_like(href)
        ):
            continue
        # decide view vs raw based on extension
        ext = Path(href).suffix.lower()
        if (
            ext in IMAGE_EXTS
            or ext in PDF_EXTS
            or ext in VIDEO_EXTS
            or ext in AUDIO_EXTS
        ):
            a["href"] = url_for("raw_file", path=_join(href))
        else:
            a["href"] = url_for("view_file", path=_join(href))

    return str(soup)


# --- CSV/Excel renderers ---
def render_csv(abs_path, limit_rows=1000):
    with open(abs_path, newline="", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        rows = list(reader)[:limit_rows]
    html = "<table class='csv-table'>"
    for i, row in enumerate(rows):
        tag = "th" if i == 0 else "td"
        html += "<tr>" + "".join(f"<{tag}>{cell}</{tag}>" for cell in row) + "</tr>"
    html += "</table>"
    return Markup(html)


def render_excel(abs_path, limit_rows=1000, limit_cols=50):
    try:
        df = pd.read_excel(abs_path, sheet_name=0)
        df = df.iloc[:limit_rows, :limit_cols]
        return Markup(df.to_html(classes="csv-table", border=0, escape=False))
    except Exception as e:
        return Markup(f"<p class='muted'>Error rendering Excel: {e}</p>")


# ------------------------------ Flask app -----------------------------------

app = Flask(__name__)


@app.context_processor
def inject_globals():
    return {
        "APP_TITLE": APP_TITLE,
        "APP_SUBTITLE": APP_SUBTITLE,
        "ROOT_DIR": ROOT_DIR,
    }


@app.route("/")
def home():
    return redirect(url_for("browse", path=""))


def list_children(rel_path: str):
    abs_dir = to_abs(rel_path)
    if not os.path.isdir(abs_dir):
        abort(400)

    items = []
    with os.scandir(abs_dir) as it:
        for e in it:
            if e.name in IGNORE_NAMES or e.name.startswith("."):
                continue  # 👈 skip ignored / hidden
            items.append(
                {
                    "name": e.name,
                    "is_dir": e.is_dir(),
                    "path": (rel_path + "/" if rel_path else "") + e.name,
                }
            )
    items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
    return items


@app.route("/api/list")
def api_list():
    rel_path = request.args.get("path", "")
    abs_path = to_abs(rel_path)

    # ✅ If it's a file, don't coerce — just say "not a directory"
    if os.path.isfile(abs_path):
        return jsonify({"error": "---> Selected"}), 400

    if not os.path.isdir(abs_path):
        return jsonify({"error": "not a directory"}), 400

    items = []
    with os.scandir(abs_path) as it:
        for e in it:
            if e.name in IGNORE_NAMES:
                continue
            items.append(
                {
                    "name": e.name,
                    "is_dir": e.is_dir(),
                    "path": (rel_path + "/" if rel_path else "") + e.name,
                }
            )
    items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
    return jsonify({"path": rel_path, "items": items})


@app.route("/browse/")
@app.route("/browse/<path:path>")
def browse(path: str | None = None):
    rel_path = "" if path is None else path
    abs_path = to_abs(rel_path)
    if not os.path.isdir(abs_path):
        return redirect(url_for("view_file", path=rel_path))

    entries = list_directory(abs_path)
    breadcrumbs = make_breadcrumbs(rel_path)

    # Render README.md (or index.md) if present
    fallback_used = False
    readme_html = None

    # Preferred README names
    candidates = ["README.md", "readme.md", "index.md"]
    found = False
    for readme_name in candidates:
        candidate = os.path.join(abs_path, readme_name)
        if os.path.isfile(candidate):
            with open(candidate, "r", encoding="utf-8", errors="ignore") as f:
                md = build_markdown_renderer()
                html = md.convert(f.read())
                readme_html = Markup(rewrite_relative_links(html, rel_path))
            found = True
            break

    # Fallback: first markdown file in directory
    if not found:
        for entry in sorted(os.listdir(abs_path)):
            if Path(entry).suffix.lower() in MARKDOWN_EXTS:
                candidate = os.path.join(abs_path, entry)
                with open(candidate, "r", encoding="utf-8", errors="ignore") as f:
                    md = build_markdown_renderer()
                    html = md.convert(f.read())
                    readme_html = Markup(rewrite_relative_links(html, rel_path))
                fallback_used = candidate.split("/")[-1]
                break

    return render_template(
        "browse.html",
        rel_path=rel_path,
        abs_path=abs_path,
        entries=entries,
        breadcrumbs=breadcrumbs,
        readme_html=readme_html,
        fallback_used=fallback_used,
    )


@app.route("/view/<path:path>")
def view_file(path: str):
    rel_path = path
    abs_path = to_abs(rel_path)
    if not os.path.exists(abs_path) or not os.path.isfile(abs_path):
        abort(404)

    ext = Path(abs_path).suffix.lower()
    breadcrumbs = make_breadcrumbs(posixpath.dirname(rel_path))

    # Markdown
    if ext in MARKDOWN_EXTS:
        with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
            md = build_markdown_renderer()
            html = md.convert(f.read())
            html = rewrite_relative_links(html, posixpath.dirname(rel_path))
        return render_template(
            "view_file.html",
            rel_path=rel_path,
            abs_path=abs_path,
            breadcrumbs=breadcrumbs,
            kind="markdown",
            html=Markup(html),
            language=None,
            raw_url=url_for("raw_file", path=rel_path),
        )

    if ext in CSV_EXTS:
        return render_template(
            "view_file.html",
            kind="csv",
            html=render_csv(abs_path),
            rel_path=rel_path,
            breadcrumbs=breadcrumbs,
            raw_url=url_for("raw_file", path=rel_path),
        )

    if ext in EXCEL_EXTS:
        return render_template(
            "view_file.html",
            kind="excel",
            html=render_excel(abs_path),
            rel_path=rel_path,
            breadcrumbs=breadcrumbs,
            raw_url=url_for("raw_file", path=rel_path),
        )

    # Image
    if ext in IMAGE_EXTS:
        return render_template(
            "view_file.html",
            rel_path=rel_path,
            abs_path=abs_path,
            breadcrumbs=breadcrumbs,
            kind="image",
            src=url_for("raw_file", path=rel_path),
            raw_url=url_for("raw_file", path=rel_path),
            language=None,
        )

    # PDF
    if ext in PDF_EXTS:
        return render_template(
            "view_file.html",
            rel_path=rel_path,
            abs_path=abs_path,
            breadcrumbs=breadcrumbs,
            kind="pdf",
            src=url_for("raw_file", path=rel_path),
            raw_url=url_for("raw_file", path=rel_path),
            language=None,
        )

    # Video
    if ext in VIDEO_EXTS:
        return render_template(
            "view_file.html",
            rel_path=rel_path,
            abs_path=abs_path,
            breadcrumbs=breadcrumbs,
            kind="video",
            src=url_for("raw_file", path=rel_path),
            raw_url=url_for("raw_file", path=rel_path),
            language=None,
        )

    # Audio
    if ext in AUDIO_EXTS:
        return render_template(
            "view_file.html",
            rel_path=rel_path,
            abs_path=abs_path,
            breadcrumbs=breadcrumbs,
            kind="audio",
            src=url_for("raw_file", path=rel_path),
            raw_url=url_for("raw_file", path=rel_path),
            language=None,
        )

    # Text / code files -> show with client-side highlighting
    if ext in TEXT_EXTS or ext == "":
        # Avoid reading very large files into the page
        max_preview_bytes = 2 * 1024 * 1024  # 2 MB
        size = os.path.getsize(abs_path)
        too_big = size > max_preview_bytes
        content = ""
        if not too_big:
            with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        language = LANG_BY_EXT.get(ext, "")
        return render_template(
            "view_file.html",
            rel_path=rel_path,
            abs_path=abs_path,
            breadcrumbs=breadcrumbs,
            kind="text",
            content=content,
            language=language,
            too_big=too_big,
            size=size,
            raw_url=url_for("raw_file", path=rel_path),
        )

    # Fallback: offer download / raw view
    return render_template(
        "view_file.html",
        rel_path=rel_path,
        abs_path=abs_path,
        breadcrumbs=breadcrumbs,
        kind="binary",
        raw_url=url_for("raw_file", path=rel_path),
        language=None,
    )


@app.route("/raw/<path:path>")
def raw_file(path: str):
    rel_path = path
    abs_path = to_abs(rel_path)
    if not os.path.exists(abs_path) or not os.path.isfile(abs_path):
        abort(404)
    directory = os.path.dirname(abs_path)
    filename = os.path.basename(abs_path)
    return send_from_directory(directory=directory, path=filename, as_attachment=False)


@app.route("/scripts_home")
def scripts_home():
    mgr: ScriptManager = app.config["SCRIPTS"]
    items = []
    for name in mgr.names():
        r = mgr.get(name)
        s = mgr.spec(name)
        items.append({
            "name": name,
            "running": r.process is not None and r.process.poll() is None,
            "path": s.path,
            "log": s.log,
        })
    return render_template("scripts_home.html", scripts=items)

@app.route("/script/<name>")
def script_page(name: str):
    mgr: ScriptManager = app.config["SCRIPTS"]
    runner = mgr.get(name)
    spec = mgr.spec(name)
    return render_template(
        "script.html",
        name=name,
        script=spec,
        running=runner.process is not None,
    )

@app.route("/start/<name>", methods=["GET"])
def start(name: str):
    mgr: ScriptManager = app.config["SCRIPTS"]
    return mgr.get(name).start()

@app.route("/stop/<name>", methods=["GET"])
def stop(name: str):
    mgr: ScriptManager = app.config["SCRIPTS"]
    return mgr.get(name).stop()

@app.route("/status/<name>")
def status(name: str):
    mgr: ScriptManager = app.config["SCRIPTS"]
    r = mgr.get(name)
    return "Running" if r.process else "Stopped"

@app.route("/log/<name>", methods=["GET"])
def log(name: str):
    mgr: ScriptManager = app.config["SCRIPTS"]
    r = mgr.get(name)
    return Response(r.get_output(), mimetype="text/plain")

# --------------------------- CLI + Entrypoint -------------------------------


def print_banner(port):
    print(f"\n{APP_TITLE} — {APP_SUBTITLE}")
    print(f"Root directory: {ROOT_DIR}")
    print(f"Serving on http://127.0.0.1:{port}\n")


def run_server(root=None, port=5000, debug=False, host="127.0.0.1"):
    global ROOT_DIR
    if root:
        ROOT_DIR = os.path.abspath(root)
    print(f"Serving {ROOT_DIR} at http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)


# ==============================================================================#
# run as import
def create_hub(
    root=None,
    host="127.0.0.1",
    port=5000,
    debug=False,
    scripts=None
):
    global ROOT_DIR
    if root:
        ROOT_DIR = os.path.abspath(root)

    if scripts:
        app.config["SCRIPTS"] = ScriptManager(scripts)
    app.run(host=host, port=port, debug=debug)


def main():
    parser = argparse.ArgumentParser(
        description="Local GitHub-like file viewer (Flask)"
    )
    parser.add_argument("--root", type=str, default=None, help="Root folder to serve")
    parser.add_argument("--host", type=str, default=None, help="Host server. 0.0.0.0")
    parser.add_argument(
        "--port", type=int, default=5000, help="Port to run the server on"
    )
    parser.add_argument("--debug", action="store_true", help="Enable Flask debug mode")
    args = parser.parse_args()

    run_server(root=args.root, port=args.port, debug=args.debug, host=args.host)


# if __name__ == "__main__":
#     import argparse
#     dd = 'active/flask_file_viewer/demo'
#     dd = "active/flask_file_viewer/show/d19_microspot"
#     dd = "Wiki-Doc/pages"
#     parser = argparse.ArgumentParser(description="Local GitHub-like file viewer (Flask)")
#     parser.add_argument("--root", type=str, default=dd, help="Root folder to serve (defaults to CWD or $FFV_ROOT)")
#     parser.add_argument("--port", type=int, default=5000, help="Port to run the server on")
#     parser.add_argument("--debug", action="store_true", help="Enable Flask debug mode")
#     args = parser.parse_args()


#     if args.root:
#         ROOT_DIR = os.path.abspath(args.root)

#     port = int(args.port or 5000)
#     print_banner(port)
#     app.run(host="127.0.0.1", port=port, debug=bool(args.debug))
