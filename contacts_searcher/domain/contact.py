from contacts_searcher.domain.inn import validate
from contacts_searcher.infrastructure.unique_str_set import UniqueStrSet


class Contact:
    def __init__(self, inn: str, phones=None, emails=None, company_names=None):
        self.inn = inn
        self.phones = phones or set()
        self.emails = emails or set()
        self.company_names = company_names or UniqueStrSet(similarity_threshold=0.5)

    @property
    def inn(self) -> str:
        return self._inn

    @inn.setter
    def inn(self, inn: str):
        if not validate(inn):
            raise ValueError(f"Invalid INN was provided: {inn}")
        self._inn = inn

    def __repr__(self):
        return repr(
            f"{self.__class__.__name__}(inn={self.inn}, phones={self.phones}, emails={self.emails}, company_names={self.company_names})"
        )
