import typing as t
import pydantic

from lestra.io import parse


class lestra(str):

    parsed: t.Any = None

    def __getattr__(self, item):
        if self.parsed is None:
            self.parsed = parse(self)
        return self.parsed[item]

    def __getitem__(self, item):
        return self.__getattr__(item)


def is_struct(struct: type[pydantic.BaseModel] , st: str | lestra):
    try:
        struct(**parse(st))
        return True
    except (TypeError, ValueError):
        return False
