import typing as t
import collections
import dataclasses
import re


class _Token(collections.namedtuple("Token", "type value")):
    pass


class _TGenerator:

    def __init__(self, *t_types):
        self._t_types = t_types
        self._master_pat = re.compile(r"|".join(*t_types))

    def __call__(self, text):
        scanner = self._master_pat.scanner(text)
        for m in iter(scanner.match, None):
            tok = _Token(m.lastgroup, m.group())
            yield tok


@dataclasses.dataclass
class _Tokens:
    tokens: t.Iterator
    token: _Token | None = None
    next_token: _Token | None = None

    def advance(self):
        self.token, self.next_token = self.next_token, next(self.tokens, None)

    def accept(self, token_type: str):
        if self.next_token and self.next_token.type == token_type:
            self.advance()
            return True
        return False

    def expect(self, token_type):
        if not self.accept(token_type):
            raise SyntaxError(f"Expected {token_type}")
