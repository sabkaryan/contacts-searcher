import re


def calc_jaccard_similarity(str1: str, str2: str) -> float:
    if str1 is None and str2 is None:
        return 1

    if str1 is None or str2 is None:
        return 0

    def lower(s):
        return s.lower()

    a = set(map(lower, str1.split()))
    b = set(map(lower, str2.split()))
    c = a.intersection(b)
    return float(len(c) / (len(a) + len(b) - len(c)))


def sanitize_str(string):
    if not string:
        return string

    return re.sub(r'[^0-9a-zA-Zа-яА-Я ]+', '', string)
