from typing import ClassVar, Set, Callable

from orbiter_parsers.file_types import unimplemented_dump
from orbiter.file_types import FileType

from orbiter_parsers.parsers.jil import JilParser


def old_parse_jil(s: str) -> dict[str, list[dict]]:
    """Parses JIL string into a dictionary.

    ```pycon
    >>> old_parse_jil(r'''insert_job: TEST.ECHO  job_type: CMD  /* INLINE COMMENT */
    ... owner: foo
    ... /* MULTILINE
    ...     COMMENT */
    ... machine: bar
    ... command: echo "Hello World"''')
    {'jobs': [{'insert_job': 'TEST.ECHO', 'job_type': 'CMD', 'owner': 'foo', 'machine': 'bar', 'command': 'echo "Hello World"'}]}

    ```
    """
    from jilutil import JilParser as OldJilParser

    return {k: [dict(job) for job in v] for k, v in OldJilParser(None).parse_jobs_from_str(s).items()}

class FileTypeJILv1(FileType):
    """JIL File Type

    :param extension: JIL
    :type extension: Set[str]
    :param load_fn: custom JIL loading function
    :type load_fn: Callable[[str], dict]
    :param dump_fn: JIL dumping function not yet implemented, raises an error
    :type dump_fn: Callable[[dict], str]
    """

    extension: ClassVar[Set[str]] = {"TXT", "JIL"}
    load_fn: ClassVar[Callable[[str], dict]] = JilParser.loads
    dump_fn: ClassVar[Callable[[dict], str]] = unimplemented_dump

class FileTypeJIL(FileType):
    """JIL File Type

    :param extension: JIL
    :type extension: Set[str]
    :param load_fn: custom JIL loading function
    :type load_fn: Callable[[str], dict]
    :param dump_fn: JIL dumping function not yet implemented, raises an error
    :type dump_fn: Callable[[dict], str]
    """

    extension: ClassVar[Set[str]] = {"TXT", "JIL"}
    load_fn: ClassVar[Callable[[str], dict]] = JilParser.loads
    dump_fn: ClassVar[Callable[[dict], str]] = unimplemented_dump
