"""
Path and file helpers: find directories and files, archivate, etc.
"""
from __future__ import annotations

import logging
import os
import sys
from datetime import datetime
from io import IOBase
from pathlib import Path
from shutil import copy2
from typing import IO, TYPE_CHECKING, Generator, Iterable, overload

if TYPE_CHECKING:
    from typing import Literal

_logger = logging.getLogger(__name__)


#region Find application-specific data directories and files

SYSTEM_DATA_ROOT = Path(os.environ.get('PROGRAMDATA') or (r'C:\ProgramData' if sys.platform == 'win32' else '/usr/local/share'))

USER_DATA_ROOT = Path(os.environ.get('APPDATA') or (r'~\AppData\Roaming' if sys.platform == 'win32' else '~/.local/share')).expanduser()


def get_app_data_dir(app: str, *, repository: str|os.PathLike|None = None) -> Path:
    r"""
    Determine the primary application directory to use depending on the name of the application.
    
    For an application named `my-app`:
    - `$PWD/data/my-app` where `$PWD` is the current working directory, if it exists
    - `$repository/data/my-app` where `$repository` is an argument that should typically be set to the root of the Git repository containing the application, if it exists and is not in `site-packages`.
    - `$USER_DATA_ROOT/my-app` where `USER_DATA_ROOT` is `~\AppData\Roaming` on Windows or `~/.local/share` on Linux, if it exists
    - `$SYSTEM_DATA_ROOT/my-app` where `SYSTEM_DATA_ROOT` is `C:\ProgramData` on Windows or `'/usr/local/share` on Linux, if it exists

    If none exist, `$USER_DATA_ROOT/my-app`  is created and returned.
    """
    # Current directory
    cwd_path = Path.cwd().joinpath('data', app)
    if cwd_path.exists():
        return cwd_path
    
    # Repository
    repository_path = None
    if repository:
        if not isinstance(repository, Path):
            repository = Path(repository)
        if not 'site-packages' in repository.parts:
            repository_path = repository.joinpath('data')
            if repository_path.exists():
                return repository_path
    
    # User
    user_path = USER_DATA_ROOT.joinpath(app)
    if user_path.exists():
        return user_path
    
    # System
    system_path = SYSTEM_DATA_ROOT.joinpath(app)
    if system_path.exists():
        return system_path
    
    # Create if none existed
    if cwd_path.parent.exists():
        new_path = cwd_path
    elif repository_path and repository_path.parent.exists():
        new_path = repository_path
    else:
        new_path = user_path
    new_path.mkdir(parents=True, exist_ok=True)
    return new_path


def iter_app_data_files(apps: str|Iterable[str]|dict[str,str|os.PathLike], file: str|os.PathLike, *, repository: str|os.PathLike|None = None, include_data_parent = False) -> Generator[Path, None, None]:
    """
    :param apps: List of apps, or mapping of apps to their containing repository.
    :param file: Name of the file. Cannot be absolute.
    :param repository: Repository containing the application. Can only be used when argument `apps` was passed as a string.
    :param include_data_parent: Include files found in the root of the repository (thus not beeing in any 'data' directory).
    """
    apps_dict: dict[str,Path|None] = {}
    if isinstance(apps, str):
        apps_dict = {apps: repository if repository is None or isinstance(repository, Path) else Path(repository)}
    else:
        if repository is not None:
            raise ValueError("Argument 'repository' can only be used when argument `apps` was passed as a string")
        if isinstance(apps, dict):
            apps_dict = {app: repository if repository is None or isinstance(repository, Path) else Path(repository) for app, repository in apps.items()}
        else:
            apps_dict = {app: None for app in apps}

    if os.path.isabs(file):
        raise ValueError("Argument 'file' cannot be absolute: '%s'" % file)

    _already_tested: set[Path] = set()
    def not_already_tested_and_exists(path: Path) -> Path|None:
        if path in _already_tested:
            return None
        _already_tested.add(path)
        if not path.exists():
            return None
        return path
    
    # Current directory
    if include_data_parent:
        path = not_already_tested_and_exists(Path.cwd().joinpath(file))
        if path:
            yield path

        path = not_already_tested_and_exists(Path.cwd().joinpath('data', file))
        if path:
            yield path    
    
    for app in apps:
        path = not_already_tested_and_exists(Path.cwd().joinpath('data', app, file))
        if path:
            yield path

    # Repository
    for app, repository in apps_dict.items():
        if not repository:
            continue

        if include_data_parent:
            path = not_already_tested_and_exists(repository.joinpath(file))
            if path:
                yield path
        
        path = not_already_tested_and_exists(repository.joinpath('data', file))
        if path:
            yield path
        
    # User
    for app in apps:
        path = not_already_tested_and_exists(SYSTEM_DATA_ROOT.joinpath(app, file))
        if path:
            yield path
    
    # System
    for app in apps:
        path = not_already_tested_and_exists(USER_DATA_ROOT.joinpath(app, file))
        if path:
            yield path

#endregion


#region Find a file from a directory to the root

def find_to_root(name: str, start_dir: str|os.PathLike|None = None) -> Path|None:
    """
    Find the given file name from the given start directory (or current working directory if none given), up to the root.

    Return None if not found.
    """    
    if start_dir:
        if not isinstance(start_dir, Path):
            start_dir = Path(start_dir)
        start_dir = start_dir.absolute()

        if not start_dir.exists():
            raise FileNotFoundError("Argument 'start_dir' not found: '%s'" % start_dir)
        elif not start_dir.is_dir():
            raise ValueError("Argument 'start_dir' is not a directory: '%s'" % start_dir)
    else:
        start_dir = Path.cwd()

    last_dir = None
    current_dir = start_dir
    while last_dir != current_dir:
        path = current_dir.joinpath(name)
        if path.exists():
            return path
        parent_dir = current_dir.joinpath(os.path.pardir).absolute()
        last_dir, current_dir = current_dir, parent_dir

    return None

#endregion


#region Normalize and relativize paths

@overload
def normalize_path(path: str|os.PathLike, default_dir: str|os.PathLike|None = None, *, mkparents = False, **kwargs) -> Path:
    ...

@overload
def normalize_path(path: IO, default_dir: str|os.PathLike|None = None, *, mkparents = False, **kwargs) -> IO:
    ...

@overload
def normalize_path(path: None, default_dir: str|os.PathLike|None = None, *, mkparents = False, **kwargs) -> None:
    ...

def normalize_path(path: str|os.PathLike|IO|None, default_dir: str|os.PathLike|None = None, *, mkparents = False, **kwargs) -> Path|IO|None:
    """
    Relativize a path from the current working directory if it is inside its tree.

    :param path: The path to normalize.
    :param default_dir: If given and `path` is a string not containing '/' or '\\', consider `path` as a member of the `default_dir` directory.
    :param mkparents: If True, create parent directories if they do not exist.
    """
    if path is None:
        return None
    elif isinstance(path, (IOBase,IO)):
        return path
    
    if path == 'stdout':
        return sys.stdout
    if path == 'stderr':
        return sys.stderr
    
    if default_dir is not None and isinstance(path, str) and not ('/' in path or '\\' in path):
        if not isinstance(default_dir, Path):
            default_dir = Path(default_dir)
        if kwargs:
            path = path.format(**kwargs)
        path = default_dir.joinpath(path)
    else:
        if kwargs:
            if not isinstance(path, str):
                path = str(path).format(**kwargs)
        if not isinstance(path, Path):
            path = Path(path)

    if mkparents:
        path.parent.mkdir(parents=True, exist_ok=True)

    return relativize_path(path)

    
@overload
def relativize_path(path: str|os.PathLike, to: str|os.PathLike|None = None) -> Path:
    ...
        
@overload
def relativize_path(path: IO, to: str|os.PathLike|None = None) -> IO:
    ...

@overload
def relativize_path(path: None, to: str|os.PathLike|None = None) -> None:
    ...

def relativize_path(path: str|os.PathLike|IO|None, to: str|os.PathLike|None = None) -> Path|IO|None:
    """
    Express a path relatively to the given directory (current working directory by default) if it is inside its tree.
    """
    if path is None:
        return None
    elif isinstance(path, (IOBase,IO)):
        return path
    elif not isinstance(path, Path):
        path = Path(path)
    
    try:
        return path.relative_to(to or Path.cwd())
    except ValueError: # Path is not relative to the given directory
        return path

#endregion


#region Archivate a file

@overload
def archivate_file(path: str|os.PathLike, archive: Literal[True]|str|os.PathLike|None = None, *, prefix: str|None = None, missing_ok: Literal[False] = False, keep: bool = False) -> Path:
    ...

@overload
def archivate_file(path: str|os.PathLike, archive: Literal[True]|str|os.PathLike|None = None, *, prefix: str|None = None, missing_ok: Literal[True], keep: bool = False) -> Path|None:
    ...

@overload
def archivate_file(path: str|os.PathLike, archive: Literal[False], *, prefix: str|None = None, missing_ok: bool = False, keep: bool = False) -> None:
    ...

def archivate_file(path: str|os.PathLike, archive: bool|str|os.PathLike|None = None, *, prefix: str|None = None, missing_ok: bool = False, keep: bool = False) -> Path|None:
    """
    Archivate `path` to `archive_dir` directory, ensuring unique archive name.

    :param archive: By default (if None), use the same directory as the origin path. If relative (e.g. 'archive'), it is relative to the directory of the original path.
    :param prefix: Prefix to use on the archive file names. For example, use `.` to make them hidden files under Linux.
    :param missing_ok: If True, do not throw an exception if the original file does not exist.
    :param keep: If True, the original file is not removed after archiving.
    """
    if archive is False: # Disabled
        return None
    
    if not isinstance(path, Path):
        path = Path(path)
    
    if not path.exists():
        if missing_ok:
            return None
        raise FileNotFoundError(f"File not found: '{path}'")
    elif path.is_dir():
        raise ValueError(f"Cannot archive a directory: '{path}'")

    if archive is None or archive is True:
        archive = Path(path).parent
    
    else:
        if not isinstance(archive, (str,os.PathLike)):
            raise TypeError(f'archive: {archive}')
        if not isinstance(archive, Path):
            archive = Path(archive)
        if not archive.is_absolute():
            archive = path.parent.joinpath(archive)
        archive.mkdir(parents=True, exist_ok=True)

    mtime_mark = datetime.fromtimestamp(path.stat().st_mtime).strftime('%Y%m%d_%H%M%S')
    dedup_num = 1
    while True:
        name = (prefix if prefix is not None else '') + path.stem + '-' + mtime_mark + (f'_{dedup_num}' if dedup_num > 1 else '') +  path.suffix
        archive_path = archive.joinpath(name)
        if not archive_path.exists():
            break
        dedup_num += 1

    _logger.debug("Archivate %s to %s", path, archive_path)
    if keep:
        copy2(path, archive_path)
    else:
        path.unlink()
    return archive_path

#endregion
