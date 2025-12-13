"""
Encryption and decryption with GnuPG, including management of passwords using `pass` file structure, "the standard unix password manager" (see: https://www.passwordstore.org/).

See also other implementations:
- keyring-pass (v0.9.3, 2024-03-08): https://github.com/nazarewk/keyring_pass
- keyrings.unixpass (v0.0.2, 2022-08-08): https://gitlab.com/chrooti/keyrings.unixpass
- keyrings.passwordstore (v0.1.0, 2021-01-04): https://github.com/stv0g/keyrings.passwordstore
"""
from __future__ import annotations

import logging
import os
import re
import subprocess
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from shutil import which
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import TYPE_CHECKING, overload
from uuid import uuid4

if TYPE_CHECKING:
    from typing import Any, Generator, Literal, TextIO


_logger = logging.getLogger(__name__)


#region Globals

PASS_ROOT: Path = Path.home().joinpath('.password-store')
_gpg_exe: str|None = None
_default_recipient: str|None = None


def get_gpg_exe() -> str:
    global _gpg_exe

    if _gpg_exe is None:
        _gpg_exe = which('gpg')
        if not _gpg_exe:
            raise FileNotFoundError("No 'gpg' executable found")
        
    return _gpg_exe


def get_default_gpg_recipient() -> str:
    global _default_recipient

    if _default_recipient is None:
        path = PASS_ROOT.joinpath('.gpg-id')
        if not path.exists():
            raise FileNotFoundError("Pass GPG id file not found: '%s'" % path)
        
        _default_recipient = path.read_text('utf-8').strip()
        if not _default_recipient:
            raise ValueError("Pass GPG id file is blank: '%s'" % path)
    
    return _default_recipient

#endregion


#region Files

def gpg_encrypt_file(file: str|os.PathLike, output: str|os.PathLike|None = None, *, recipient: str|None = None, password: str|None = None) -> None:
    """
    Encrypt a file using GPG asymetrical encryption (or symmetrical encryption if argument `password` is given).
    
    :param recipient: Identification of the public key to use for this file (asymmetrical encryption).
    :param password: Password for this file (symmetrical encryption).
    """
    if not output:
        output = f"{file}.gpg"
    
    cmd = [get_gpg_exe(), '--quiet', '--batch', '--no-tty', '--output', output]

    if password is not None:
        if recipient:
            raise ValueError("Arguments 'recipient' and 'password' cannot be both given")
        from zut.secrets import resolve_secret
        password = resolve_secret(password)
        cmd += ['--passphrase-fd', '0', '--symmetric', file]

    elif not recipient:
        try:
            recipient = get_default_gpg_recipient()
        except FileNotFoundError:
            raise ValueError("No GPG recipient or password configured") from None
        
        cmd += ['--recipient', recipient, '--encrypt', file]

    _logger.debug("Encrypt file '%s'", file)
    try:
        subprocess.run(cmd, input=password, text=True, encoding='utf-8', check=True, capture_output=True)
    except subprocess.CalledProcessError as err:
        from zut.process import ProcessError
        raise ProcessError(err, cmd='gpg --encrypt') from None


@contextmanager
def open_gpg_decrypt_file(file: str|os.PathLike, password: str|None = None, *, buffering: int = -1, encoding: str|None = None, newline: str|None = None, **kwargs) -> Generator[TextIO, Any, Any]:
    """
    Decrypt and open a GPG-encrypted file as a context manager file .

    :param password: Password of the private key (if file was asymmetrically encrypted) or password for this file (if file was symmetrically encrypted).
    """
    if password is not None:
        from zut.secrets import resolve_secret
        password = resolve_secret(password)
            
    tmpdir = TemporaryDirectory()
    fp = None
    try:
        tmp = os.path.join(tmpdir.name, str(uuid4()))

        cmd = [get_gpg_exe(), '--quiet', '--batch', '--no-tty', '--output', tmp]
        if password is not None:
            cmd += ['--passphrase-fd', '0']
        cmd += ['--decrypt', file]
        
        _logger.debug("Decrypt file '%s'", file)
        try:
            subprocess.run(cmd, input=password, text=True, encoding='utf-8', check=True, capture_output=True)
        except subprocess.CalledProcessError as err:
            from zut.process import ProcessError
            raise ProcessError(err, cmd='gpg --decrypt') from None
        
        fp = open(tmp, 'r', buffering=buffering, encoding=encoding, newline=newline, **kwargs)
        yield fp

    finally:
        if fp:
            fp.close()
        tmpdir.cleanup()

#endregion


#region Agent

def clear_gpg_agent(*, missing_ok = False) -> None:
    _logger.debug("Reload GPG agent")
    try:
        subprocess.run(['gpg-connect-agent', 'reloadagent', '/bye'], text=True, capture_output=True)
    except FileNotFoundError:
        if missing_ok:
            return
        raise
    except subprocess.CalledProcessError as err:
        from zut.process import ProcessError
        raise ProcessError(err) from None    

#endregion


#region Pass

def get_pass_path(name: str):
    if not name:
        raise ValueError("Argument 'name' cannot be empty")
    name = re.sub(r'\\', '', name)
    parts = name.split('/')
    path = PASS_ROOT.joinpath(*parts)
    return path.with_name(f'{path.name}.gpg')


def list_pass_names():
    pass_names: list[str] = []

    def recurse(dir: Path):
        for path in sorted(dir.iterdir()):
            if path.is_dir():
                recurse(path)
            elif path.suffix == '.gpg' and not path.name.startswith('.'):
                path = path.relative_to(PASS_ROOT)
                pass_names.append(path.with_suffix('').as_posix())

    recurse(PASS_ROOT)
    return pass_names


@overload
def get_pass(name: str|Path, *, required: Literal[True]) -> str:
    ...

@overload
def get_pass(name: str|Path, *, required: Literal[False] = False) -> str|None:
    ...

def get_pass(name: str|Path, *, required = False) -> str|None:
    """
    Read a password from `pass`.
    """
    path = name if isinstance(name, Path) else get_pass_path(name)

    if not path.exists():
        if required:
            raise FileNotFoundError("Pass entry not found: '%s'" % path)
        return None

    _logger.debug("Decrypt pass entry at '%s'", path)
    try:
        return subprocess.check_output([get_gpg_exe(), '--quiet', '--batch', '--no-tty', '--decrypt', path], text=True, encoding='utf-8')
    except subprocess.CalledProcessError as err:
        from zut.process import ProcessError
        raise ProcessError(err, cmd='gpg --decrypt') from None


def set_pass(name: str|Path, value: str, *, archivate = False):
    """
    Define a password in `pass`.
    """
    path = name if isinstance(name, Path) else get_pass_path(name)

    gpg_id = get_default_gpg_recipient()
    
    path.parent.mkdir(parents=True, exist_ok=True)

    new_path = path.with_name(f'{path.name}~')
    if new_path.exists():
        new_path.unlink()

    with NamedTemporaryFile('w', encoding='utf-8', prefix='pass-', delete=False) as tmp:
        try:
            tmp.write(value)
            tmp.close()
            
            _logger.debug("Encrypt pass entry at '%s'", path)
            try:
                subprocess.check_output([get_gpg_exe(), '--quiet', '--batch', '--no-tty', '--output', new_path, '--encrypt', '--recipient', gpg_id, tmp.name], text=True, encoding='utf-8', stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as err:
                from zut.process import ProcessError
                raise ProcessError(err, cmd='gpg --encrypt') from None
            
            if path.exists():
                if archivate:
                    from zut.paths import archivate_file
                    archivate_file(path, prefix='.')
                else:
                    path.unlink()

            new_path.rename(path)
        
        finally:
            if not tmp.closed:
                tmp.close()            
            os.unlink(tmp.name)

            if new_path.exists():
                new_path.unlink()


def delete_pass(name: str, *, missing_ok = False):
    """
    Remove a password from `pass`.
    """
    path = get_pass_path(name)

    if not path.exists():
        if not missing_ok:
            raise FileNotFoundError("Pass entry not found: '%s'" % path)
        return False
    
    _logger.debug("Delete pass entry at '%s'", path)
    path.unlink()
    return True

#endregion
