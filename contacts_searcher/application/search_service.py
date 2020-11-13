import logging
from enum import Enum

from search_engine_parser.core.engines.bing import Search as BingSearch
from search_engine_parser.core.engines.duckduckgo import Search as DuckDuckGoSearch
from search_engine_parser.core.engines.google import Search as GoogleSearch
from search_engine_parser.core.engines.yandex import Search as YandexSearch
from search_engine_parser.core.exceptions import NoResultsOrTrafficError


class SearchEngine(Enum):
    DUCK_DUCK_GO = DuckDuckGoSearch
    GOOGLE = GoogleSearch
    YANDEX = YandexSearch
    BING = BingSearch


class SearchService:
    def __init__(
        self,
        main_engine: SearchEngine = SearchEngine.DUCK_DUCK_GO,
        fallback_engine: SearchEngine = SearchEngine.GOOGLE,
        pages: int = 1,
    ):
        self.__main_engine = main_engine.value()
        self.__fallback_engine = fallback_engine.value()
        self.pages = pages

    @property
    def pages(self):
        return self._pages

    @pages.setter
    def pages(self, value: int):
        if value < 1:
            raise ValueError(f"Pages value should be greater than 0, got {value}")
        self._pages = value

    def search(self, query):
        return self.__do_search(query, self.__main_engine)

    def __do_search(self, query, engine):
        found_links = []

        for page in range(1, self._pages):
            try:
                result = engine.search(query, page)
            except NoResultsOrTrafficError as e:
                if engine.name == self.__main_engine.name and page == 1:
                    logging.info(
                        f"{self.__main_engine.name} search failed. Trying fallback engine: {self.__fallback_engine.name}..."
                    )
                    found_links += self.__do_search(query, self.__fallback_engine)
                else:
                    logging.error(e)
                continue
            found_links += [r["links"] for r in result if r["links"] is not None]

        return found_links
