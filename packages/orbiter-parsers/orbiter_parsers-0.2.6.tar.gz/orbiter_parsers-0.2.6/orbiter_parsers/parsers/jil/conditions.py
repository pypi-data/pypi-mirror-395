from datetime import timedelta
from importlib.util import find_spec
from pathlib import Path

from orbiter_parsers.parsers.jil.condition_types import TaskStatus, Condition, ExitCode, Variable

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from lark import Transformer, Lark

from orbiter_parsers.parsers import discard_fn, identity_fn


def combine_leaves(_, tokens: list) -> list:
    def _get_all_types(_ts) -> set:
        _all_types = set()
        if isinstance(_ts, list):
            for t in _ts:
                _all_types.update(_get_all_types(t))
        else:
            _all_types.add(type(_ts))
        return _all_types

    def _flatten(_ts) -> list:
        _r = []
        if isinstance(_ts, list):
            for t in _ts:
                _r.extend(_flatten(t))
        return _r

    all_types = _get_all_types(tokens)
    r = []
    if (Condition not in all_types) or (len(all_types) == 1 and Condition in all_types):
        for t in tokens:
            if isinstance(t, list):
                r.extend(t)
            else:
                r.append(t)
        return r
    else:
        return tokens


class JilConditionsParser(Transformer):
    """Turn JIL `conditions` into python via Lark Grammar

    Functions that relate to `conditions.cfgr`
    grammar Rules or Terminals are used to transform parse tree to python object
    """

    @staticmethod
    def loads(s: str) -> list[dict] | dict:
        """Load JIL and run through parser via .cfgr grammar,

        Functions below that relate to grammar Rules
        or Terminals are used to transform parse tree to python dict"""
        cfgr = (Path(find_spec("orbiter_parsers.parsers.jil.grammar").origin).parent / "conditions.cfgr").read_text()
        parser = Lark(cfgr, start="start")
        return JilConditionsParser().transform(parser.parse(s if s.endswith("\n") else s + "\n"))

    def start(self, conditions: list[dict]) -> list[dict] | dict | None:
        if not conditions:
            return None
        return conditions

    cond = identity_fn
    any_status = identity_fn

    status_cond = lambda _, tokens: TaskStatus(status=tokens[0], task_id=tokens[1])
    status_cond_lookback = lambda _, tokens: TaskStatus(status=tokens[0], task_id=tokens[1], lookback=tokens[2])
    status = identity_fn

    STATUS_DONE = lambda _, __: "done"
    STATUS_FAILURE = lambda _, __: "failure"
    STATUS_NOTRUNNING = lambda _, __: "notrunning"
    STATUS_SUCCESS = lambda _, __: "success"
    STATUS_TERMINATED = lambda _, __: "terminated"

    and_cond = lambda _, tokens: (Condition(condition="and", children=combine_leaves(_, tokens)))
    ungrouped_and = combine_leaves
    grouped_and = combine_leaves

    or_cond = lambda _, tokens: (Condition(condition="or", children=combine_leaves(_, tokens)))
    grouped_or = combine_leaves
    ungrouped_or = combine_leaves

    lookback = identity_fn
    lookback_hhhh = lambda _, tokens: timedelta(hours=int(tokens[0]))
    lookback_period_hhhh_mm = lambda _, tokens: timedelta(hours=int(tokens[0]), minutes=int(tokens[1]))
    lookback_colon_hhhh_mm = lambda _, tokens: timedelta(hours=int(tokens[0]), minutes=int(tokens[1]))

    exitcode_cond = lambda _, tokens: ExitCode(
        task_id=tokens[0],
        operator=tokens[1],
        value=int(val) if (val := tokens[2]).isdigit() else val,
    )
    exitcode_cond_lookback = lambda _, tokens: ExitCode(
        task_id=tokens[0],
        lookback = tokens[1],
        operator=tokens[2],
        value=int(val) if (val := tokens[3]).isdigit() else val,
    )

    value_cond = lambda _, tokens: Variable(
        name=tokens[0],
        operator=tokens[1],
        value=int(val) if (val := tokens[2]).isdigit() else val,
    )

    object_name = identity_fn

    NEWLINE: None = discard_fn  # throw away empty newlines

    __default__ = identity_fn
    """if there isn't a rule otherwise for something, just have it return its value"""
    __default_token__ = identity_fn
