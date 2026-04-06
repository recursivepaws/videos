# Source - https://stackoverflow.com/a/1884277
def find_nth(haystack: str, needle: str, n: int) -> int:
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start


def unswara(s):
    return s.replace("\\'", "").replace("\\_", "")
