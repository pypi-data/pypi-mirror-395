import re
from dataclasses import dataclass
from typing import Callable, Match, Pattern, Tuple, cast

REGEX_NUMERIC = re.compile(r"^\d+$")

REGEX_NUMBERS_ONLY = re.compile(r"^[\d\.]+$")

REGEX_CAMEL_CASE = re.compile(
    r"((?<=[a-z0-9])(?=[A-Z])|(?<!^)(?<=[A-Z])(?=[A-Z][a-z]))"
)

RE_DOMAIN_NAMES = re.compile(
    r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$"
)

RE_UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")

# r"^[\w.-]+@[\w.-]+\.\w+$",
RE_EMAIL = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

RE_HTML = re.compile(r"<[^<]+?>")

RE_URL = re.compile(
    r"^https?:\/\/(?:(?:www\.)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z0-9]{2,}|(?:[a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+(?:\/[^\s/]+)+)(?:\/[^?\s]*)?(?:\?[^\s]*)?$"
)


# r"^(\+?\d{1,3})?\s?\d{3}[\s.-]\d{3}[\s.-]\d{4}$"
RE_PHONE_NUMBER = re.compile(r"^(\+?\d{1,3})?\s?\d{3}[\s.-]\d{3}[\s.-]\d{4}$")

# r"^\s*function\s+\w+\s*\("
RE_JAVASCRIPT = re.compile(r"^\s*function\s+\w+\s*\(")


MatchFunc = Callable[[str | Pattern[str], str], Match[str] | None]


@dataclass
class RegExMatcher:
    string: str
    _match_func: MatchFunc
    match: Match[str] | None = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (str, re.Pattern, tuple)):
            return NotImplemented
        pattern = other
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        elif isinstance(pattern, tuple):
            pattern = re.compile(*pattern)
        self.match = self._match_func(pattern, self.string)
        return self.match is not None

    def __getitem__(
        self, group: int | str | tuple[int, ...] | tuple[str, ...]
    ) -> str | tuple[str, ...] | None:
        if self.match is None:
            return None
        if isinstance(group, (int, str)):
            return self.match[group]
        # For tuple groups, need to handle differently
        return cast(Tuple[str, ...], tuple(self.match[g] for g in group))


def _search(pattern: str | Pattern[str], string: str) -> Match[str] | None:
    return re.search(pattern, string)


def _match(pattern: str | Pattern[str], string: str) -> Match[str] | None:
    return re.match(pattern, string)


def _fullmatch(pattern: str | Pattern[str], string: str) -> Match[str] | None:
    return re.fullmatch(pattern, string)


def search_in(string: str) -> RegExMatcher:
    return RegExMatcher(string, _match_func=_search)


def match_in(string: str) -> RegExMatcher:
    return RegExMatcher(string, _match_func=_match)


def fullmatch_in(string: str) -> RegExMatcher:
    return RegExMatcher(string, _match_func=_fullmatch)
