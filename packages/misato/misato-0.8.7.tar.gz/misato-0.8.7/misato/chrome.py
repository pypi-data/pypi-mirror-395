import os
import sys
import time
import subprocess
from typing import Optional

from playwright.sync_api import sync_playwright, Browser, Page, Playwright

from misato.logger import logger
from misato.config import CHROME_EXE, USER_DATA_DIR, DEBUG_PORT, MAX_CONNECT_ATTEMPTS

# Global singletons (created once, reused forever)
_playwright: Optional[Playwright] = None
_browser: Optional[Browser] = None
_page: Optional[Page] = None


def _launch_chrome() -> None:
    """Launch Chrome with remote debugging port if not already running."""
    os.makedirs(USER_DATA_DIR, exist_ok=True)

    subprocess.Popen(
        [
            CHROME_EXE,
            f"--remote-debugging-port={DEBUG_PORT}",
            f"--user-data-dir={USER_DATA_DIR}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-popup-blocking"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
    )
    logger.info(f"Chrome launched (or already running) with remote debugging port {DEBUG_PORT}")


def _connect_once() -> None:
    """Connect to the existing Chrome instance with automatic retry."""
    global _playwright, _browser, _page

    # Fast alive-check
    if _page is not None:
        try:
            _page.title()
            return
        except:
            pass  # connection lost → reconnect

    logger.info("Connecting to your Chrome instance")

    for attempt in range(1, MAX_CONNECT_ATTEMPTS + 1):
        try:
            _playwright = sync_playwright().start()
            _browser = _playwright.chromium.connect_over_cdp(f"http://localhost:{DEBUG_PORT}")
            context = _browser.contexts[0]

            # Reuse existing tab if any, otherwise create one
            _page = context.pages[0] if context.pages else context.new_page()

            # Block useless resources → blazing fast + minimal bandwidth
            _page.route(
                "**/*",
                lambda route, request: route.abort()
                if request.resource_type in {"image", "stylesheet", "script", "font", "media"}
                else route.continue_()
            )

            logger.info(f"Successfully connected!")
            return

        except Exception:
            logger.info(f"Connection failed. Retrying...")
            time.sleep(1)

    logger.error(f"Failed to connect to Chrome on port {DEBUG_PORT} after {MAX_CONNECT_ATTEMPTS}s")
    logger.error("   → Start Chrome with --remote-debugging-port=9222 first")
    sys.exit(1)


# ========================== PUBLIC API ==========================
def _ensure_ready() -> None:
    """Called on import – guarantees browser & page are ready."""
    if _page is None:
        _launch_chrome()     # make sure Chrome is running
        _connect_once()      # wait until CDP is available


# Auto-initialize when module on import
_ensure_ready()

# Public singletons (these are the only things you will ever use)
browser: Browser = _browser          # rarely needed, kept for advanced cases
page: Page = _page                   # your one and only tab – goto anywhere!