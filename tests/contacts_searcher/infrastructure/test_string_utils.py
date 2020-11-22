import unittest

from pytest import approx

from contacts_searcher.infrastructure.string_utils import calc_jaccard_similarity, sanitize_str


class StringUtils(unittest.TestCase):
    def test_calc_jaccard_similarity(self):
        similarity = calc_jaccard_similarity('ООО ""КОМБИКОРМОВЫЙ ЗАВОД ""ЛЕТО""', 'Комбикормовый Завод ""Лето"", ООО')
        assert approx(similarity) == 0.333333, "similar strings test"

    def test_sanitize_str(self):
        assert (
            sanitize_str('ООО ""КОМБИКОРМОВЫЙ ЗАВОД ""ЛЕТО""') == "ООО КОМБИКОРМОВЫЙ ЗАВОД ЛЕТО"
        ), "sanitize string test"
