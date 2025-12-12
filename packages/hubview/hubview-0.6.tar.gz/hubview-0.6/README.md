# HubView — GitHub‑like file viewer (Flask)

A clean, fast, local file viewer with a GitHub‑style UI. Browse folders, preview code with syntax highlighting, render Markdown (tables, task lists, admonitions), show images/video/audio/PDF, and even draw Mermaid diagrams via fenced blocks.

https://github.com/ (UI inspiration only)

### TODO

1. Instructions on running: hubview
   1. 251204


## Example Run Code

```python
from hubview import app
app.create_hub(
    root='./',
    host='0.0.0.0',
    port=3000,
    script_ex='.venv/bin/python',
    script_path='./',
    script_log='log.log'
)
```

Or:

in terminal, type:
hubview

## Quick start

1. pip install hubview
2. hubview --root 'your directory'
3. open **http://127.0.0.1:5000** in your browser.

## Features

- 🗂️ Directory browsing with breadcrumbs
- 📝 Markdown rendering with **pymdown-extensions** (tables, details, tasklists, emoji, etc.)
- 🧠 Mermaid diagrams via fenced blocks:  
  <code>```mermaid</code> … <code>```</code>
- 🎨 Client-side syntax highlighting using highlight.js
- 🖼️ Photo/image preview, plus audio/video and PDF embeds
- 📖 Auto-render `README.md` (or `index.md`) at the bottom of each directory
- 🛡️ Path safety (jailed to a root folder)
- 🌗 Looks good in light and dark


