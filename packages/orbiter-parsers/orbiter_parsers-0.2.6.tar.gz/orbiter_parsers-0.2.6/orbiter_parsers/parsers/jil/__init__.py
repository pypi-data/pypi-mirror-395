from __future__ import annotations

from importlib.util import find_spec
from pathlib import Path

from lark import Transformer, Lark, Tree

from orbiter_parsers.parsers import identity_fn, discard_fn, as_kv, identity_kv, reduce_to_dict


def clean_str(s: str) -> str:
    r"""Clean string:
     - remove non-breaking space char (GIGO)
     - remove leading or training whitespace (if a later rule was dropped but the space remained)
     - remove leading and trailing quotes if both are present
         - BUT NOT if there are quotes in the middle of the string
         - UNLESS they are escaped

    ```pycon
    >>> clean_str('"foo" ')
    'foo'
    >>> clean_str(r'"foo" "bar" "baz" ')
    '"foo" "bar" "baz"'
    >>> clean_str(r'" \"foo\" \"bar\" \"baz\" "')
    '\\"foo\\" \\"bar\\" \\"baz\\"'

    ```
    """
    remove_nbsp = s.replace("\xa0", " ")
    strip_ws = remove_nbsp.strip()

    without_outer_quotes = strip_ws[1:-1]
    has_start_and_end_quotes = strip_ws.startswith('"') and strip_ws.endswith('"')
    has_inner_quotes = bool(without_outer_quotes.count('"'))
    has_only_inner_escaped_quotes = bool(without_outer_quotes.count('"') == without_outer_quotes.count(r'\"'))

    match (has_start_and_end_quotes, has_inner_quotes, has_only_inner_escaped_quotes):
        # a) has inner quotes that are escaped, strip
        case (True, True, True):
            return without_outer_quotes.strip()
        # b) has inner quotes that are unescaped, skip
        case (True, True, False):
            return strip_ws
        # c) only has start/end quotes, strip
        case (True, False, _):
            return without_outer_quotes.strip()
        # d) no further quotes, skip
        case (False, _, _) | _:
            return strip_ws


class JilParser(Transformer):
    """Turn JIL into python dict via Lark Grammar

    Functions that relate to `jil.cfgr` grammar Rules or Terminals are used to transform parse tree to python dict
    """

    @staticmethod
    def loads(s: str) -> list[dict] | dict:
        """Load JIL and run through parser via .cfgr grammar,

        Functions below that relate to grammar Rules
        or Terminals are used to transform parse tree to python dict"""
        # Add a newline, if not present
        clean_input = (
            s
            if s.endswith("\n") else
            s + "\n"
        # clean utf-8 BOM from input
        ).lstrip(b'\xef\xbb\xbf'.decode('utf-8'))
        cfgr = (Path(find_spec("orbiter_parsers.parsers.jil.grammar").origin).parent / "jil.cfgr").read_text()
        parser = Lark(cfgr, start="start")
        return JilParser().transform(parser.parse(clean_input))

    def start(self, list_of_sub_command: list[Tree | dict]) -> list[dict] | dict | None:
        """Return all the 'sub_command' children as a list, or just a single dict if there's only one"""
        if not list_of_sub_command:
            return None
        elif len(list_of_sub_command) == 1:
            return list_of_sub_command[0]
        else:
            return list_of_sub_command

    NEWLINE: None = discard_fn  # throw away empty newlines

    sub_command: dict = reduce_to_dict
    """sub_command is like `insert_job: foo job_type: bar`, 
    it can have attribute_statements (e.g. `job_type`) 
    after the definition"""
    sub_command_def: tuple = as_kv

    attribute_statement: tuple = as_kv
    """attribute_statement is like `job_type: bar`"""

    attribute_statement_def = identity_kv

    date_statement = lambda _, tokens: ("date", tokens[0])
    date = identity_fn
    time = identity_fn

    def attribute_statement_value(self, tokens):
        if not tokens:
            return None
        res = identity_fn(self, tokens)
        return clean_str("".join(res) if isinstance(res, list) else res)

    auto_blob = lambda _, token: identity_fn(_, token).removeprefix("<auto_blobt>").removesuffix("</auto_blobt>")

    string = identity_fn
    unquoted_string = identity_fn
    quoted_string = lambda _, token: f'"{"".join(identity_fn(_, token) if token else [])}"'
    quoted_inner = identity_fn
    quoted_string_ending_slash = identity_fn

    __default__ = identity_fn
    """if there isn't a rule otherwise for something, just have it return its value"""
    __default_token__ = identity_fn
