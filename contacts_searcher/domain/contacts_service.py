import logging
import re

import phonenumbers
from bs4 import BeautifulSoup
from phonenumbers import NumberParseException

from contacts_searcher.domain.contact import Contact


class ContactsService:
    def parse_contacts(self, inn: str, crawler_results):
        company_contacts = Contact(inn)

        results = (
            self.parse_page_contacts(page, depth)
            for depth_dict in crawler_results
            for depth, pages in depth_dict.items()
            for page in pages
        )

        for phones, emails, company_name in results:
            company_contacts.phones |= phones
            company_contacts.emails |= emails
            company_contacts.company_names.add(company_name)

        return company_contacts

    def parse_page_contacts(self, page_content: BeautifulSoup, depth: int) -> (set, set, str):
        phones = self._scrap_phones(page_content)
        emails = self._scrap_emails(page_content)
        company_name = self._scrap_company_name(page_content) if depth == 1 else None

        return phones, emails, company_name

    def _scrap_emails(self, page_content: BeautifulSoup):
        hrefs = set()

        for mailto in page_content.select("a[href^=mailto]"):
            regexp_result = re.search(r"mailto:([^?]+)", mailto["href"])

            if regexp_result is not None:
                hrefs.add(regexp_result.group(1))

        return hrefs

    def _scrap_phones(self, page_content: BeautifulSoup):
        phones = set()
        phones_iter = re.finditer(
            r"(\+7|8)[\s\-]\(?[0-9]{3,4}\)?[\s\-]?[0-9]{2,3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}",
            page_content.text,
            re.MULTILINE,
        )

        for phone_match in phones_iter:
            phone_candidate = phone_match.group()
            try:
                parsed_phone = phonenumbers.parse(phone_candidate, "RU")
            except NumberParseException as e:
                logging.info(f"Error occurred while parsing the phone {phone_candidate}")
                logging.error(e)
                continue

            if phonenumbers.is_valid_number(parsed_phone):
                phones.add(phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.NATIONAL))

        return phones

    def _scrap_company_name(self, page_content: BeautifulSoup):
        page_header_element = page_content.find("h1")
        return page_header_element.text.strip() if page_header_element is not None else None
