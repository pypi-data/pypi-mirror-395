from typing import ClassVar, Set, Callable

from ast2json import str2json
from orbiter.file_types import FileType

from orbiter_parsers.file_types import unimplemented_dump


class FileTypePython(FileType):
    """Python File Type

    :param extension: PY
    :type extension: Set[str]
    :param load_fn: Python AST loading function (via `ast2json`)
    :type load_fn: Callable[[str], dict]
    :param dump_fn: Python dumping function not yet implemented, raises an error
    :type dump_fn: Callable[[dict], str]
    """

    extension: ClassVar[Set[str]] = {"PY"}
    load_fn: ClassVar[Callable[[str], dict]] = str2json
    dump_fn: ClassVar[Callable[[dict], str]] = unimplemented_dump
