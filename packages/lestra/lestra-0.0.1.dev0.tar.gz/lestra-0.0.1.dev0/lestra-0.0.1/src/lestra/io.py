import json
import typing as t
import typing_extensions as te

from lestra._parser import _TGenerator, _Tokens


_SCALAR_TYPES = str, int, float,


def _dump(o: t.Any, parent: None | str = None) -> str:

    if isinstance(o, list):
        ret = ", ".join(_dump(i) for i in o)
        ret = f"[{ret}]"
        if parent:
            return f"{parent}={ret}"
        return ret

    if isinstance(o, dict):
        ret = []
        for k, v in o.items():
            if parent is None:
                p = k
            else:
                p = f"{parent}.{k}"
            r = _dump(v, p)
            ret.append(r)

        return " ".join(ret)

    if isinstance(o, _SCALAR_TYPES):
        if parent:
            return f"{parent}={json.dumps(o)}"
        return json.dumps(o)

    raise TypeError(f"Unexpected type={type(o)}")


_T_NUM = r"(?P<NUM>\d+)"
_T_LB = r"(?P<LB>\[)"
_T_RB = r"(?P<RB>\])"
_T_SPACES = r"(?P<SPACES>\s)"
_T_EQ = r"(?P<EQ>=)"
_T_DOT = r"(?P<DOT>\.)"
_T_WORD = r"(?P<WORD>\w+)"
_T_QUOTES = r"(?P<QUOTES>\")"
_T_SEP = r"(?P<SEP>,)"


_generate_tokens = _TGenerator(ts := list(v for n, v in locals().items() if n.startswith("_T_")))


def dump(
    o: t.Annotated[
        t.Any,
        te.Doc("Объект для сериализации. Поддерживаются: str, int, float, list и dict (keys - строки)."),
    ]
) ->  t.Annotated[
    str,
    te.Doc("Строковое представление объекта в компактной форме (поддерживает разбор функцией parse)."),
]:
    """
     Сериализация объекта в компактную строковую форму.

    Описание:
    - Для словарей создаётся набор присваиваний с точечной нотацией для вложенных ключей.
    - Для списков создаётся JSON-подобное представление в квадратных скобках.
    - Строки экранируются и берутся в двойные кавычки (используется json.dumps).
    - Числа остаются в числовом виде (int или float).

    Примеры:
    >>> dump({"a": 1, "b": [2, 3]})
    'a=1 b=[2, 3]'

    >>> dump("hello")
    '"hello"'

    """
    return _dump(o)


def parse(s: t.Annotated[str, te.Doc("Разбор строки, созданной dump в Python структуру")]) -> t.Any:
    """
    Поддерживаемый синтаксис:
    - Присваивания: key=value, где key может быть вложенным через точки (a.b.c=1)
    - Числа: целые (123) или дробные (12.34)
    - Строки: в двойных кавычках "text" (поддерживается экранирование через стандарт JSON-правила)
    - Списки: [v1, v2, ...]
    - Между токенами могут быть пробелы

    Возвращаемое значение:
    - В большинстве случаев возвращается dict с разобранными присваиваниями.
      Однако функция поддерживает также разбор отдельных значений (например, при парсинге списка/скаляра).

    Исключения:
    - SyntaxError при ошибках синтаксиса (неожиданные токены, незакрытые строки и т.п.)

    examples:

    >>> parse("123")
    123

    >>> parse("a.b=20")
    {"a": {"b": 20}}
    """
    toks = _Tokens(tokens=_generate_tokens(s))
    toks.advance()

    def skip_spaces():
        while toks.accept("SPACES"):
            pass

    def merge_into(target: dict, src: dict):
        for k, v in src.items():
            if k in target and isinstance(target[k], dict) and isinstance(v, dict):
                merge_into(target[k], v)
            else:
                target[k] = v

    def parse_value():
        skip_spaces()
        if not toks.next_token:
            raise SyntaxError("Unexpected end of input while parsing value")

        nt = toks.next_token.type

        if nt == "LB":
            return parse_list()

        if nt == "QUOTES":
            # consume opening "
            toks.expect("QUOTES")
            pieces = ['"']  # start with opening quote
            # collect everything until closing QUOTES
            while True:
                if toks.next_token is None:
                    raise SyntaxError("Unterminated string")
                if toks.next_token.type == "QUOTES":
                    toks.advance()  # consume closing quote
                    pieces.append(toks.token.value)
                    break
                toks.advance()
                pieces.append(toks.token.value)
            full = "".join(pieces)
            return json.loads(full)

        if nt == "NUM":
            toks.expect("NUM")
            num_str = toks.token.value
            # possible float: NUM DOT NUM
            if toks.next_token and toks.next_token.type == "DOT":
                toks.advance()  # consume DOT
                # after this expect NUM
                toks.expect("NUM")
                num_str = num_str + "." + toks.token.value
                return float(num_str)
            return int(num_str)

        if nt == "WORD":
            # An identifier at a value position means an inline dict fragment (a=23 or a.b=3)
            return parse_assignment_as_dict()

        raise SyntaxError(f"Unexpected token while parsing value: {nt}")

    def parse_assignment_as_dict():
        # parse key path: WORD(.WORD)*
        skip_spaces()
        keys = []
        toks.expect("WORD")
        keys.append(toks.token.value)
        while True:
            skip_spaces()
            if toks.accept("DOT"):
                skip_spaces()
                toks.expect("WORD")
                keys.append(toks.token.value)
                continue
            break
        skip_spaces()
        toks.expect("EQ")
        # parse the value for this assignment
        val = parse_value()
        # build nested dict for this assignment
        d = cur = dict()
        *keys, last = keys

        for k in keys:
            cur[k] = dict()
            cur = cur[k]
        cur[last] = val
        return d

    def parse_list():
        skip_spaces()
        toks.expect("LB")
        skip_spaces()
        items = []

        # empty list
        if toks.next_token and toks.next_token.type == "RB":
            toks.expect("RB")
            return items

        while True:
            skip_spaces()
            if toks.next_token is None:
                raise SyntaxError("Unterminated list")
            if toks.next_token.type == "WORD":
                item = parse_assignment_as_dict()
            else:
                item = parse_value()
            items.append(item)
            skip_spaces()
            if toks.accept("SEP"):
                continue
            if toks.next_token and toks.next_token.type == "RB":
                toks.expect("RB")
                break
            raise SyntaxError("Expected ',' or ']' in list")
        return items

    # start parsing
    skip_spaces()
    if toks.next_token is None:
        return None

    # If string starts with '[' => whole thing is a list
    if toks.next_token.type == "LB":
        res = parse_list()
        skip_spaces()
        if toks.next_token is not None:
            raise SyntaxError("Extra data after top-level list")
        return res

    # If starts with NUM or QUOTES => single scalar value
    if toks.next_token.type in ("NUM", "QUOTES"):
        res = parse_value()
        skip_spaces()
        if toks.next_token is not None:
            raise SyntaxError("Extra data after scalar")
        return res

    # Otherwise parse as sequence of assignments -> dict
    result = dict()
    while toks.next_token:
        skip_spaces()
        if toks.next_token is None:
            break
        d = parse_assignment_as_dict()
        merge_into(result, d)
        skip_spaces()
    return result
