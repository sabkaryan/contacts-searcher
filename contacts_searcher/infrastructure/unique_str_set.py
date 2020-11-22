from contacts_searcher.infrastructure.string_utils import calc_jaccard_similarity, sanitize_str


class UniqueStrSet:
    def __init__(self, similarity_threshold=0, items=None, similarity_func=calc_jaccard_similarity):
        self.items = items or set()
        self.similarity_threshold = similarity_threshold
        self.similarity_func = similarity_func

    def add(self, candidate_item: str) -> bool:
        for item in self.items:
            similarity = self.similarity_func(sanitize_str(item), sanitize_str(candidate_item))
            if similarity >= self.similarity_threshold:
                return False
        self.items.add(candidate_item)
        return True

    def __iter__(self):
        return self.items.__iter__()

    def __sub__(self, other):
        return self.items.__sub__(other)
