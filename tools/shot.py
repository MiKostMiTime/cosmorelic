# AI-assisted code (agentic AI + LLM). Disclosure: see README.md.
"""Capture a real screenshot of the running app via the Chrome DevTools Protocol.

Chrome's own --screenshot flag fires on the load event, which is too early for a
Gradio app: its first paint arrives from a server round-trip. This script opens
the page, waits in real time for that round-trip to land, then captures.

Usage:
    python tools/shot.py URL OUT.png [wait_seconds]
"""

import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import websocket

CHROME = (
    Path.home()
    / "Library/Caches/ms-playwright/chromium-1254/chrome-mac-arm64"
    / "Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
)
PORT = 9333


def _get(path):
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}{path}", timeout=10) as r:
        return json.load(r)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    url, out = sys.argv[1], sys.argv[2]
    wait = float(sys.argv[3]) if len(sys.argv) > 3 else 12.0

    chrome = subprocess.Popen(
        [
            str(CHROME),
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            f"--remote-debugging-port={PORT}",
            "--window-size=1440,1750",
            "about:blank",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(40):
            try:
                _get("/json/version")
                break
            except Exception:
                time.sleep(0.25)
        else:
            print("Chrome did not expose a debugging port")
            return 1

        tabs = _get("/json/list")
        page = next(t for t in tabs if t.get("type") == "page")
        ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=30)
        msg_id = 0

        def send(method, params=None):
            nonlocal msg_id
            msg_id += 1
            ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
            while True:
                reply = json.loads(ws.recv())
                if reply.get("id") == msg_id:
                    return reply

        send("Page.enable")
        send("Page.navigate", {"url": url})
        time.sleep(wait)

        shot = send("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True})
        data = shot["result"]["data"]
        import base64

        Path(out).write_bytes(base64.b64decode(data))
        print(f"wrote {out}")
        ws.close()
        return 0
    finally:
        chrome.terminate()
        chrome.wait(timeout=10)


if __name__ == "__main__":
    sys.exit(main())