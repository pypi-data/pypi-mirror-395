from __future__ import annotations

from typing import Any

from lark import Token, Tree
from lark.visitors import Discard


# noinspection D
def identity_fn(
    _, tokens: list[Tree | Token | Any] | Token, *args
) -> list[Token | Any] | Any:
    """Identity Function - return what was given

    ```pycon
    >>> identity_fn('', Token('FOO', []))
    lark.visitors.Discard

    >>> identity_fn('', Token('FOO', [1,2,3]))
    [1, 2, 3]

    ```
    """
    # If it's a Token/TERMINATOR get the .value of the token rather than just returning the token itself
    _ = args # noqa
    if isinstance(tokens, Token):
        if isinstance(value := tokens.value, list):
            if not len(value):
                return Discard
            elif len(value) == 1:
                return value[0]
            else:
                return value
        else:
            return value
    elif isinstance(tokens, list):
        if not len(tokens):
            return Discard
        elif len(tokens) == 1:
            return tokens[0]
        else:
            return tokens
    else:
        return tokens

def identity_kv(_, tokens: list[Token | Any]):
    res = identity_fn(_, tokens)
    if isinstance(res, list):
        # if it's [<rule_name>, <match 1>, <match 2>, ...]
        if len(res) == 2:
            return res[0], res[1]
        elif len(res) > 2:
            return res[0], res[1:]
    return res

def discard_fn(self, _) -> Discard:  # noqa
    """Discard Function - throw away token"""
    return Discard

def as_kv(_, tokens: list[Token]) -> tuple[Token, Token]:
    """Return a tuple of (key, value) from a list of tokens"""
    return (
        tokens[0],
        tokens[1],
    )


def reduce_to_dict(_, tokens: list[tuple[str, Any]]) -> dict:
    """Reduce a list of tuples into a dict"""
    r = {}
    for k, v in tokens:
        if k in r:
            if isinstance(r[k], list):
                r[k].append(v)
            else:
                r[k] = [r[k], v]
        else:
            r[k] = v
    return r
