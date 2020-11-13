import asyncio
import logging
from urllib.parse import urlparse

from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup
from typing import List, Dict

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

DEFAULT_FETCH_TIMEOUT = ClientTimeout(sock_connect=10, sock_read=20)

DEFAULT_REQUESTS = 30

INVALID_PAGE_EXTENSIONS = (".csv", ".xml", ".pdf", ".txt", ".xls", ".xlsx")


class CrawlerService:
    def __init__(self, depth=1, headers=DEFAULT_HEADERS, timeout=DEFAULT_FETCH_TIMEOUT, requests=DEFAULT_REQUESTS):
        self.depth = depth
        self.headers = headers
        self.timeout = timeout
        self.requests = requests
        self._tasks = []

    @property
    def depth(self) -> int:
        return self._depth

    @depth.setter
    def depth(self, depth: int):
        if depth < 1:
            raise ValueError(f"Depth mast be greater than 0, got {depth}")
        self._depth = depth

    @property
    def requests(self) -> int:
        return self._requests

    @requests.setter
    def requests(self, requests):
        if requests < 1:
            raise ValueError(f"Requests value mast be greater than 0, got {requests}")
        self._requests = requests

    async def fetch_one(
        self, url: str, session: ClientSession, depth=1, checked_urls=None, result=None
    ) -> Dict[int, List[BeautifulSoup]]:
        result = {depth: []} if result is None or result.get(depth, None) is None else result
        checked_urls = [] if checked_urls is None else checked_urls

        if depth > self.depth or url.endswith(INVALID_PAGE_EXTENSIONS):
            return result

        try:
            logging.info(f"Fetching url {url} current depth {depth}...")
            async with session.get(url) as response:
                page_bytes = await response.read()
                logging.info(f"Fetched page bytes for url {url}, depth {depth}")
        except Exception as e:
            logging.error(f"Fetch error: {e}(url={url}, depth={depth})")
            return result

        page_content: BeautifulSoup = BeautifulSoup(page_bytes, "html.parser")
        result[depth].append(page_content)

        checked_urls.append(url)

        parsed_url = urlparse(url)
        tasks = []
        for page_link in page_content.find_all("a"):
            if (
                page_link is None
                or not page_link.get("href", "").startswith("/")
                or not parsed_url.scheme.startswith("http")
            ):
                continue

            href_attr = f"{parsed_url.scheme}://{parsed_url.netloc}{page_link['href']}"
            if href_attr in checked_urls:
                continue

            task = asyncio.ensure_future(self.fetch_one(href_attr, session, depth + 1, checked_urls, result))
            tasks.append(task)

            if len(tasks) >= self.requests:
                await asyncio.gather(*tasks)
                tasks.clear()

        if len(tasks) > 0:
            await asyncio.gather(*tasks)
            tasks.clear()

        return result

    async def fetch_all(self, urls: list):
        async with ClientSession(headers=self.headers, timeout=self.timeout) as session:
            return await asyncio.gather(*[self.fetch_one(url, session) for url in urls])
