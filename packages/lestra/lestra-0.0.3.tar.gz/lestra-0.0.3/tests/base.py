import pytest
from collections import namedtuple

from lestra import parse, dump


class _TestPair(namedtuple("TestPair", "struct dumped")):
    pass


_PAIRS = [
    _TestPair(
        struct=1,
        dumped="1",
    ),
    _TestPair(
        struct="x",
        dumped="\"x\"",
    ),
    _TestPair(
        struct=[1, 2],
        dumped="[1, 2]",
    ),
    _TestPair(
        struct=[2, "3"],
        dumped="[2, \"3\"]",
    ),
    _TestPair(
        struct=dict(a=10, b=20),
        dumped="a=10 b=20",
    ),
    _TestPair(
        struct=dict(a="10", b=[2, "3"], c=dict(d=40, e=dict(f="500"), g=[6, dict(s=70)])),
        dumped="a=\"10\" b=[2, \"3\"] c.d=40 c.e.f=\"500\" c.g=[6, s=70]"
    ),
]


@pytest.mark.parametrize(
    "o, expected", _PAIRS
)
def test_dump_basic(o, expected):
    assert dump(o) == expected

@pytest.mark.parametrize(
    "expected, s", _PAIRS
)
def test_parse_basic(expected, s):
    assert expected == parse(s)



@pytest.mark.parametrize("bad", ["a=", "a", "a=1 b", "[1 2]", "[1,]", "2 3"])
def test_parse_raises_on_invalid(bad):
    with pytest.raises(SyntaxError):
        parse(bad)


def test_dump_unsupported_type_raises():
    class Foo:
        pass

    with pytest.raises(TypeError):
        dump(Foo())
