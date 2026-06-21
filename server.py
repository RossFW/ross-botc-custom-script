#!/usr/bin/env python3
"""Tiny dev server for the custom-script editor.
Serves static files AND accepts POST /save to persist edits to data.json on disk,
so edits are visible outside the browser (and survive cache clears)."""
import http.server, os

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data.json")
PORT = 8770

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=DIR, **kw)

    def do_POST(self):
        if self.path == "/save":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            with open(DATA, "wb") as f:
                f.write(body)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
        else:
            self.send_error(404)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

print(f"Editor server running at http://localhost:{PORT}/v1.html")
print(f"Edits persist to {DATA}")
http.server.HTTPServer(("", PORT), Handler).serve_forever()
