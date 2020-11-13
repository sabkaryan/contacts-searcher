from collections import Counter
from typing import List

from contacts_searcher.domain.contact import Contact


class SanitizerService:
    def __init__(self, blacklist=None, threshold=1):
        self.blacklist = blacklist
        self.threshold = threshold

    def clear_duplicates(self, naive_results: List[Contact]) -> List[Contact]:
        """
        clear duplicates for different inns

        :param naive_results: list of results with duplicates
        :return: results cleared from duplicates
        """
        emails = []
        phones = []
        company_names = []
        for contacts in naive_results:
            emails += contacts.emails
            phones += contacts.phones
            company_names += contacts.company_names

        email_duplicates = self._find_duplicates(emails, self.threshold)
        phone_duplicates = self._find_duplicates(phones, self.threshold)
        company_name_duplicates = self._find_duplicates(company_names, self.threshold)

        return [
            Contact(
                contacts.inn,
                phones=contacts.phones - phone_duplicates,
                emails=contacts.emails - email_duplicates,
                company_names=company_name_duplicates,
            )
            for contacts in naive_results
        ]

    def _find_duplicates(self, sequence, threshold=1):
        counter = Counter(sequence)
        return {key for key, value in counter.items() if value > threshold}

    def find_common_contacts(self, search_results: List[Contact]) -> List[Contact]:
        # TODO: implement
        # inn_result["emails"] = emails
        # inn_result["phones"] = {key for key, value in Counter(phones).most_common(5) if value > 1}
        # inn_result["companyName"] = Counter(company_names).most_common(1)[0][0] if len(company_names) > 0 else None
        #
        raise NotImplemented
