from __future__ import annotations

from functools import partial
from importlib.util import find_spec
from pathlib import Path
from typing import TypedDict, Any

from lark import Transformer, Token, Tree, Lark
from lark.visitors import Discard


class Node(TypedDict):
    type: str
    key: None | str  # optional, e.g. for things like comments or references
    # TODO - Should it be Node.value: str | list["Node"] ? or just list["Node"]?
    value: str | list["Node"]


class EspToDict(Transformer):
    """Turn ESP text into python dict via Lark Grammar

    Functions that relate to `esp.cfgr` grammar Rules or Terminals are used to transform parse tree to python dict
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = Lark(
            (
                Path(find_spec("orbiter_parsers.parsers.esp.grammar").origin).parent
                / "esp.cfgr"
            ).read_text(),
            start="start",
        )

    def loads(self, s: str) -> list[Node | Any]:
        """Load ESP string.
        :return
        """
        if not s.endswith("\n"):
            s += "\n"
        return self.transform(self.parser.parse(s))

    @staticmethod
    def _node_of_type(_type, tokens: list[Node | Any], no_key=False) -> Node:
        if len(tokens) == 0:
            raise ValueError("No tokens provided")
        elif len(tokens) == 1:
            return Node(type=_type, value=tokens[0])  # noqa
        elif len(tokens) > 1 and no_key:
            return Node(type=_type, value=tokens)  # noqa
        elif len(tokens) == 2:
            # TODO - Should it be Node.value: str | list["Node"] ? or just list["Node"]?
            return Node(type=_type, key=tokens[0], value=tokens[1])
        else:
            return Node(type=_type, key=tokens[0], value=tokens[1:])

    def line_end(self, tokens: list[Token]) -> list | Discard:  # noqa
        """If only one thing on the line, return it directly, else return a list, else Discard if line is empty"""
        if tokens:
            if len(tokens) == 1:
                return tokens[0]
            else:
                return tokens
        else:
            return Discard

    def paren_unquoted(self, tokens: list[Token | Any]) -> list:  # noqa
        return [
            t
            for t in tokens
            if t and (not isinstance(t, str) or (isinstance(t, str) and t.strip()))
        ]

    def identity_fn(
        self, tree_or_tokens: list[Tree | Token | Any] | Token, or_discard: bool = False
    ) -> list[Token | Any] | Any:  # noqa
        """Identity Function - return what was given
        :param tree_or_tokens: A tree if it's the start rule, or a list of tokens if it's a rule, or a single token if it's a terminal
        :param or_discard: - if True, discard if empty rather than passing through (e.g. [])
        """
        # If it's a Token/TERMINATOR get the .value of the token rather than just returning the token itself
        if isinstance(tree_or_tokens, Token):
            return tree_or_tokens.value
        if or_discard:
            return tree_or_tokens or Discard
        return tree_or_tokens

    def discard_fn(self, _) -> Discard:  # noqa
        """Discards - throw away"""
        return Discard

    # Nodes
    job = lambda self, tokens: self._node_of_type("job", tokens)  # noqa E731
    jobname = lambda self, tokens: self._node_of_type("jobname", tokens)  # noqa E731
    stmt = lambda self, tokens: self._node_of_type("stmt", tokens)  # noqa E731
    if_ = lambda self, tokens: self._node_of_type(  # noqa E731
        "if", tokens, no_key=True
    )
    then = lambda self, tokens: self._node_of_type(  # noqa E731
        "then", tokens, no_key=True
    )
    else_ = lambda self, tokens: self._node_of_type(  # noqa E731
        "else", tokens, no_key=True
    )
    if_stmt = lambda self, tokens: self._node_of_type(  # noqa E731
        "if_stmt", tokens, no_key=True
    )
    do_stmt = lambda self, tokens: self._node_of_type(  # noqa E731
        "do_stmt", tokens, no_key=True
    )
    var = lambda self, tokens: self._node_of_type("var", tokens)  # noqa E731
    REFERENCE = lambda self, token: (  # noqa E731
        self._node_of_type("ref", [token.value])
    )
    COMMENT = lambda self, token: (  # noqa E731
        self._node_of_type("comment", [token.value.strip()])
    )

    # Identity
    start = identity_fn
    prop = identity_fn
    line = partial(
        identity_fn, or_discard=True
    )  # discard if empty line or pass line through
    string = identity_fn
    unquoted_inner = identity_fn
    double_quoted_string = identity_fn
    single_quoted_string = identity_fn
    paren_quoted = identity_fn

    STRING = identity_fn
    NAME = identity_fn
    JOB = identity_fn
    APPLEND = identity_fn
    SOMEJOB = identity_fn
    FILEWATCHER = identity_fn
    NUMBER = identity_fn
    STR_IN_SINGLE_QUOTE = identity_fn
    STR_IN_DOUBLE_QUOTE = identity_fn
    COLON = identity_fn
    ENV_VAR = identity_fn
    ESCAPED_STRING = identity_fn

    # Discard
    NEWLINE = discard_fn
    WS = discard_fn
