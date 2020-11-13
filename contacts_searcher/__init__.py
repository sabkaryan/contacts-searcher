import asyncio
import logging
from builtins import print
from pprint import pprint
from time import perf_counter


from contacts_searcher.application import search_service
from contacts_searcher.application.crawler_service import CrawlerService
from contacts_searcher.application.search_service import SearchService, SearchEngine
from contacts_searcher.domain.contacts_service import ContactsService
from contacts_searcher.domain.inn_repository import InnRepository
from contacts_searcher.domain.sanitizer_service import SanitizerService
from contacts_searcher.infrastructure.csv_data_source import CSVDataSource

MAX_PAGES = 3
MAX_DUPLICATES = 1

logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", datefmt="%d/%m/%Y %H:%M:%S", level=logging.INFO)


if __name__ == "__main__":
    start = perf_counter()

    loop = asyncio.get_event_loop()

    res = []
    csv_data_source = CSVDataSource("../inn_example_small.csv")
    inn_repository = InnRepository(csv_data_source)
    inn_list_gen = inn_repository.find_all()

    search_service = SearchService(pages=MAX_PAGES)
    crawler_service = CrawlerService()
    contacts_service = ContactsService()
    sanitizer_service = SanitizerService()

    for inn in inn_list_gen:
        links = search_service.search(f"{inn}")
        print(f"Found {len(links)} links for inn={inn}")

        crawler_results = loop.run_until_complete(crawler_service.fetch_all(links))
        company_contacts = contacts_service.parse_contacts(inn, crawler_results)
        res.append(company_contacts)

    sanitizer_service.clear_duplicates(res)
    stop = perf_counter()

    pprint(res)
    print(f"Done in {stop - start} seconds")
