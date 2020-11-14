from typing import List

from contacts_searcher.domain.contact import Contact


class ContactRepository:
    def __init__(self, datasource):
        self.collection = datasource.get_collection('contacts')

    def write_all(self, contacts: List[Contact]):
        contacts_dict = [vars(contact) for contact in contacts]
        self.collection.insert_many(contacts_dict)
