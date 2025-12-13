from typing import Optional
from curl_cffi import requests
from misato.config import HEADERS, RETRY, DELAY, TIMEOUT
from misato.logger import logger
from misato.chrome import page

import time

class HttpClient:
    def get(self, url: str, cookies: Optional[dict] = None, retries: int = RETRY, delay: int = DELAY, timeout: int = TIMEOUT) -> Optional[bytes]:
        for attempt in range(retries):
            try:
                response = requests.get(url=url, headers=HEADERS, cookies=cookies, timeout=timeout, verify=False)
                return response.content
            except Exception as e:
                logger.error(f"Failed to fetch data (attempt {attempt + 1}/{retries}): {e} url is: {url}")
                time.sleep(delay)
        logger.error(f"Max retries reached. Failed to fetch data. url is: {url}")
        return None

    def post(self, url: str, data: dict, cookies: Optional[dict] = None, retries: int = RETRY, delay: int = DELAY, timeout: int = TIMEOUT) -> Optional[requests.Response]:
        for attempt in range(retries):
            try:
                response = requests.post(url=url, data=data, headers=HEADERS, cookies=cookies, timeout=timeout, verify=False)
                return response
            except Exception as e:
                logger.error(f"Failed to post data (attempt {attempt + 1}/{retries}): {e} url is: {url}")
                time.sleep(delay)
        logger.error(f"Max retries reached. Failed to post data. url is: {url}")
        return None

    def get_page_html(self, url: str, cookies: Optional[str]) -> Optional[str]:
        try:
            page.goto(url, wait_until="domcontentloaded")
            content = page.content()
            page.goto("chrome://settings/help")
            return content
        except Exception as e:
            logger.error("An error occurred: %s", str(e))
