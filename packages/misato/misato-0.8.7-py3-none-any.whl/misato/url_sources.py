from abc import ABC, abstractmethod
import re
from typing import Optional
from misato.http_client import HttpClient
from misato.config import HREF_REGEX_PUBLIC_PLAYLIST, HREF_REGEX_NEXT_PAGE, MATCH_UUID_PATTERN
from misato.logger import logger
from misato.utils import ThreadSafeCounter
from enum import Enum

class UrlType(Enum):
    SINGLE = 1
    PLAYLIST = 2

class UrlSource(ABC):
    @abstractmethod
    def get_urls(self) -> list[str]:
        pass

    @staticmethod
    def movie_count_log(movie_counter: ThreadSafeCounter, movie_url: str):
        logger.info(f"Movie {movie_counter.increment_and_get()} url: {movie_url}")

    @staticmethod
    def get_urls_from_list(movie_counter: ThreadSafeCounter, play_list_url: str, limit: Optional[str], cookie=None, http_client: HttpClient = None) -> list[str]:
        movie_url_list = []
        url = play_list_url
        while url and (limit is None or movie_counter.get() < int(limit)):
            html_source = http_client.get_page_html(url, cookies=cookie)
            if html_source is None:
                break
            movie_url_matches = re.findall(HREF_REGEX_PUBLIC_PLAYLIST, html_source)
            temp_url_list = list(set(movie_url_matches))
            for movie_url in temp_url_list:
                movie_url_list.append(movie_url)
                UrlSource.movie_count_log(movie_counter, movie_url)
                if limit and movie_counter.get() == limit:
                    return movie_url_list
            next_page_matches = re.findall(HREF_REGEX_NEXT_PAGE, html_source)
            url = next_page_matches[0].replace('&amp;', '&') if next_page_matches else None
        return movie_url_list

class SingleUrlSource(UrlSource):
    def __init__(self, movie_counter: ThreadSafeCounter, url: str, limit: Optional[str]):
        self.movie_counter = movie_counter
        self.url = url
        self.limit = int(limit) if limit else None

    def get_urls(self) -> list[str]:
        if self.limit and self.movie_counter.get() == self.limit:
            return []
        else:
            UrlSource.movie_count_log(self.movie_counter, self.url)
            return [self.url]

class PlaylistSource(UrlSource):
    def __init__(self, movie_counter: ThreadSafeCounter, playlist_url: str, limit: Optional[str]):
        self.movie_counter = movie_counter
        self.playlist_url = playlist_url
        self.limit = int(limit) if limit else None
        self.http_client = HttpClient()

    def get_urls(self) -> list[str]:
        url = self.playlist_url
        return UrlSource.get_urls_from_list(movie_counter=self.movie_counter, play_list_url=url, limit=self.limit, cookie=None, http_client=self.http_client)

class AutoUrlSource(UrlSource):
    def __init__(self, movie_counter: ThreadSafeCounter, auto_urls: list[str], limit: Optional[str]):
        self.movie_counter = movie_counter
        self.auto_urls = auto_urls
        self.limit = int(limit) if limit else None
        self.http_client = HttpClient()

    def get_urls(self) -> list[str]:
        movie_url_list = []

        for url in self.auto_urls:

            url_type : UrlType = self._determine_url_type(url)
            if url_type == UrlType.SINGLE:
                single_url_source = SingleUrlSource(movie_counter=self.movie_counter, url=url, limit=self.limit)
                movie_url_list.extend(single_url_source.get_urls())
            else:
                playlist_source = PlaylistSource(movie_counter=self.movie_counter, playlist_url=url, limit=self.limit)
                movie_url_list.extend(playlist_source.get_urls())

        return movie_url_list

    def _determine_url_type(self, url: str) -> Optional[UrlType]:
        if self._is_movie_url(url):
            return UrlType.SINGLE
        else:
            return UrlType.PLAYLIST

    def _is_movie_url(self, url: str) -> bool:
        html = self.http_client.get_page_html(url, None)
        if not html:
            return False
        match = re.search(MATCH_UUID_PATTERN, html)
        if not match:
            return False
        return True

class AuthSource(UrlSource):
    def __init__(self, movie_counter: ThreadSafeCounter, username: str, password: str, limit: Optional[str]):
        self.movie_counter = movie_counter
        self.http_client = HttpClient()
        self.cookie = self._login(username, password)
        self.limit = int(limit) if limit else None

    def _login(self, username: str, password: str) -> dict:
        response = self.http_client.post('https://missav.ai/api/login', data={'email': username, 'password': password})
        if response and response.status_code == 200:
            cookie_info = response.cookies.get_dict()
            if "user_uuid" in cookie_info:
                logger.info(f"User uuid: {cookie_info['user_uuid']}")
                return cookie_info
        logger.error("Login failed, check your network connection or account information.")
        exit(114514)

    def get_urls(self) -> list[str]:
        url = 'https://missav.ai/saved'
        return UrlSource.get_urls_from_list(movie_counter=self.movie_counter, play_list_url=url, limit=self.limit, cookie=self.cookie, http_client=self.http_client)

class SearchSource(UrlSource):
    def __init__(self, movie_counter: ThreadSafeCounter, key: str):
        self.movie_counter = movie_counter
        self.key = key
        self.http_client = HttpClient()

    def get_urls(self) -> list[str]:
        search_url = f"https://missav.ai/search/{self.key}"
        search_regex = r'<a href="([^"]+)" alt="' + self.key + '">'
        html_source = self.http_client.get_page_html(search_url, None)
        if html_source is None:
            logger.error(f"Search failed, key: {self.key}")
            return []
        movie_url_matches = re.findall(search_regex, html_source)
        temp_url_list = list(set(movie_url_matches))
        if temp_url_list:
            logger.info(f"Search {self.key} successfully: {temp_url_list[0]}")
            UrlSource.movie_count_log(self.movie_counter, temp_url_list[0])
            return [temp_url_list[0]]
        logger.error(f"Search failed, key: {self.key}")
        return []

class FileSource(UrlSource):
    def __init__(self, movie_counter: ThreadSafeCounter, file_path: str, limit: Optional[str]):
        self.movie_counter = movie_counter
        self.file_path = file_path
        self.limit = int(limit) if limit else None

    def get_urls(self) -> list[str]:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]
        auto_url_source = AutoUrlSource(movie_counter=self.movie_counter, auto_urls=urls, limit=self.limit)
        return auto_url_source.get_urls()