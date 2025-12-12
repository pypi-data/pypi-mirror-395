from collections.abc import Generator
from typing import IO, Protocol, runtime_checkable

try:
    from typing import Self  # type: ignore[attr-defined]
except ImportError:
    from typing_extensions import Self


@runtime_checkable
class PathLike(Protocol):
    """Utility protocol used for the type of the `path` attribute of
    file-like datasets. Example types that adhere to this protocol are
    `pathlib.Path` and `cloudpathlib.CloudPath`:

    ```python
    >>> from ordeq.types import PathLike
    >>> from cloudpathlib import CloudPath
    >>> isinstance(CloudPath, PathLike)
    True
    >>> from pathlib import Path
    >>> isinstance(Path, PathLike)
    True

    ```

    `pathlib.Path` provides a consistent file addressing mechanism across
    different operating systems. Moreover, `cloudpathlib.CloudPath` allows
    users to interact with files on cloud storage through (most of the)
    `pathlib.Path` API.  The `PathLike` protocol allows users to use
    either one interchangebly in the dataset definition.

    Note that datasets that rely on the IO implementation of an external
    library may expect a type different from `PathLike` for
    its `path` (e.g., `spark.read_csv`).
    """

    def open(
        self, mode="r", buffering=-1, encoding=None, errors=None, newline=None
    ) -> IO: ...

    def __fspath__(self): ...


class GlobPath(PathLike, Protocol):
    """Protocol for accepting any PathLike object that has a `glob` method"""

    def glob(
        self, pattern, *, case_sensitive=None
    ) -> Generator[Self, None, None]: ...
