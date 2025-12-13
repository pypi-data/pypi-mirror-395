"""
Run processes and handle process errors (wrappers and extensions on stdlib's `subprocess`).
"""
from __future__ import annotations

import logging
import os
import subprocess
from queue import Queue
from shutil import which
from threading import Thread
from typing import IO, TYPE_CHECKING, Any, Callable, Mapping, Sequence, overload

if TYPE_CHECKING:
    from typing import Literal

class ProcessGlobals:
    """
    Configuration of `zut.process` module globals.
    """
    processerror_maxlen = 200


_globals = ProcessGlobals()


#region Sudo availability

_sudo_available: bool|Literal['non-interactive']|None = None

def is_sudo_available(*, non_interactive = False) -> bool:
    global _sudo_available
    
    if _sudo_available is None:
        if not which('sudo'):
            _sudo_available = False
        else:
            try:
                return_code = subprocess.call(['sudo', '-n', 'sh', '-c', 'id -u >/dev/null'], stderr=subprocess.DEVNULL)
                _sudo_available = 'non-interactive' if return_code == 0 else True
            except BaseException: # e.g. SIGINT / CTRL+C
                _sudo_available = False
    
    if non_interactive:
        return _sudo_available == 'non-interactive'
    
    return True if _sudo_available else False


class SudoNotAvailable(subprocess.SubprocessError):
    def __init__(self):
        super().__init__("Sudo is not available")

#endregion


#region Low-level stream and error management

_UNSET = object()

class ProcessError(subprocess.CalledProcessError):
    """
    Extended and configurable version of `CalledProcessError` (of module `subprocess` of the standard library), displaying `stderr` and `stdout` in the error message.

    This class is automatically used by `run_process`, `run_process_callback` and `verify_run_process` (of module `zut.process`).
    It can also be used when manually using `subprocess`. Example:

    ```
    try:
        value = subprocess.check_output(['gpg', '--quiet', '--batch', '--no-tty', '--decrypt', path], text=True, encoding='utf-8', stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as err:
        from zut.process import ProcessError
        raise ProcessError(err, cmd='gpg --decrypt') from None
    ```
    """
    def __init__(self, original_error: subprocess.CalledProcessError|None = None, *, returncode: int|None = None, cmd: str|Sequence|None = _UNSET, stdout: str|bytes|None = _UNSET, stderr: str|bytes|None = _UNSET, maxlen: int|None = _UNSET): # pyright: ignore[reportArgumentType]
        if returncode is None:
            if original_error is not None:
                returncode = original_error.returncode
            else:
                raise ValueError("Either argument 'original_error' or argument 'returncode' must be given")
            
        if cmd is _UNSET:
            if original_error is not None:
                cmd = original_error.cmd
            else:
                cmd = None

        if stdout is _UNSET:
            if original_error is not None:
                stdout = original_error.stdout
            else:
                stdout = None

        if stderr is _UNSET:
            if original_error is not None:
                stderr = original_error.stderr
            else:
                stderr = None
        
        super().__init__(returncode, cmd or '', stdout, stderr)
        self._maxlen = _globals.processerror_maxlen if maxlen is _UNSET else maxlen
        self._message = None

    def __str__(self):
        return self.message

    @property
    def message(self):
        if self._message is None:
            self._message = super().__str__()

            details = self._get_stream_details('stderr', self.stderr)
            if details:
                self._message += details

            details = self._get_stream_details('stdout', self.stdout)
            if details:
                self._message += details

        return self._message

    def with_maxlen(self, maxlen: int|None):
        self._message = None
        self._maxlen = maxlen
        return self
    
    def _get_stream_details(self, name: Literal['stdout','stderr'], value: bytes|str|None) -> str|None:
        if not value:
            return None
            
        if not isinstance(value, str):
            try:
                value = value.decode('utf-8', 'replace') # pyright: ignore[reportAttributeAccessIssue]
            except:
                value = str(value)
        
        value = value.strip()
        if not value:
            return None
        
        if self._maxlen is not None and len(value) > self._maxlen:
            value = value[0:self._maxlen] + '…'
        
        result = ''
        for line in value.splitlines():
            result += '\n[%s] %s' % (name, line)
        return result

#endregion


#region High-level run functions

@overload
def run_process(cmd: str|os.PathLike|bytes|Sequence[str|os.PathLike|bytes], *,
                encoding: Literal['bytes'],
                # (no difference with base function)
                sudo = False,
                check: int|Sequence[int]|bool = False,
                capture_output: bool|None = None,
                stdout: Literal['disable','raise','warning','error']|Callable[[bytes],Any]|None = None,
                stderr: Literal['disable','raise','warning','error']|Callable[[bytes],Any]|None = None,
                strip: Literal['rstrip-newline','strip',True]|None = None,
                strip_stderr: Literal['rstrip-newline','strip',True]|None = None,
                input: str|None = None,
                shell = False,
                env: Mapping[str,Any]|None = None,
                logger: logging.Logger|None = None) -> subprocess.CompletedProcess[bytes]:
    ...

@overload
def run_process(cmd: str|os.PathLike|bytes|Sequence[str|os.PathLike|bytes], *,
                encoding: Literal['utf-8', 'cp1252', 'unknown']|None = None,
                # (no difference with base function)
                sudo = False,
                check: int|Sequence[int]|bool = False,
                capture_output: bool|None = None,
                stdout: Literal['disable','raise','warning','error']|Callable[[str],Any]|None = None,
                stderr: Literal['disable','raise','warning','error']|Callable[[str],Any]|None = None,
                strip: Literal['rstrip-newline','strip',True]|None = None,
                strip_stderr: Literal['rstrip-newline','strip',True]|None = None,
                input: str|None = None,
                shell = False,
                env: Mapping[str,Any]|None = None,
                logger: logging.Logger|None = None) -> subprocess.CompletedProcess[str]:
    ...

def run_process(cmd: str|os.PathLike|bytes|Sequence[str|os.PathLike|bytes], *,
                sudo = False,
                check: int|Sequence[int]|bool = False,
                capture_output: bool|None = None,
                stdout: Literal['disable','raise','warning','error']|Callable[[str],Any]|Callable[[bytes],Any]|None = None,
                stderr: Literal['disable','raise','warning','error']|Callable[[str],Any]|Callable[[bytes],Any]|None = None,
                strip: Literal['rstrip-newline','strip',True]|None = None,
                strip_stderr: Literal['rstrip-newline','strip',True]|None = None,
                input: str|None = None,
                encoding: str|Literal['unknown','bytes']|None = None,
                shell = False,
                env: Mapping[str,Any]|None = None,
                logger: logging.Logger|None = None) -> subprocess.CompletedProcess:

    # If stdout or stderr is a callable, use `subprocess.Popen`
    if (stdout and callable(stdout)) or (stderr and callable(stderr)):
        return run_process_callback(cmd, sudo=sudo, check=check, capture_output=capture_output, stdout=stdout, stderr=stderr, strip=strip, strip_stderr=strip_stderr, input=input, encoding=encoding, shell=shell, env=env, logger=logger)
    
    if sudo:
        if not is_sudo_available():
            raise SudoNotAvailable()
        if isinstance(cmd, (str,os.PathLike)):
            cmd = f'sudo {cmd}'
        elif isinstance(cmd, bytes) or any(isinstance(arg, bytes) for arg in cmd):
            raise ValueError(f"Cannot use sudo with a bytes command")
        else:
            cmd = ['sudo', *cmd] # type: ignore
    
    # If neither stdout nor stderr is a callable, use `subprocess.run`
    if capture_output is None:
        if (stdout and stdout != 'disable') or (stderr and stderr != 'disable'):
            capture_output = True
        else:
            capture_output = False

    cp = subprocess.run(cmd,
                        capture_output=capture_output,
                        text=encoding not in {'unknown', 'bytes'},
                        stdout=subprocess.DEVNULL if stdout == 'disable' else None,
                        stderr=subprocess.DEVNULL if stderr == 'disable' else None,
                        input=input,
                        encoding=encoding if encoding not in {'unknown', 'bytes'} else None,
                        shell=shell,
                        env=env)
    
    return verify_run_process(cp, check=check, stdout=stdout, stderr=stderr, strip=strip, strip_stderr=strip_stderr, bytes=encoding == 'bytes', logger=logger)


def run_process_callback(cmd: str|os.PathLike|bytes|Sequence[str|os.PathLike|bytes], *,
                         sudo = False,
                         check: int|Sequence[int]|bool = False,
                         capture_output: bool|None = None,
                         stdout: Literal['disable','raise','warning','error']|Callable[[str],Any]|Callable[[bytes],Any]|None = None,
                         stderr: Literal['disable','raise','warning','error']|Callable[[str],Any]|Callable[[bytes],Any]|None = None,
                         strip: Literal['rstrip-newline','strip',True]|None = None,
                         strip_stderr: Literal['rstrip-newline','strip',True]|None = None,
                         input: str|None = None,
                         encoding: str|Literal['unknown','bytes']|None = None,
                         shell = False,
                         env: Mapping[str,Any]|None = None,
                         logger: logging.Logger|None = None) -> subprocess.CompletedProcess:
    """
    Run a process, transfering live output to callbacks.
    """
    # See: https://stackoverflow.com/a/60777270
    queue = Queue()

    def enqueue_stream(stream: IO, source: str):
        for data in iter(stream.readline, ''):
            queue.put((source, data))
        stream.close()

    def enqueue_process(proc: subprocess.Popen):
        if input is not None:
            returncode = proc.communicate(input)
        else:
            returncode = proc.wait()
        queue.put(('process', returncode))
    
    captured: dict[str, str|bytes] = {}

    def capture_callback(output, stream_name: str):
        if stream_name in captured:
            content = captured[stream_name]
            content = content + output
            captured[stream_name] = content
        else:
            captured[stream_name] = output

    verify_stdout = None
    if stdout == 'disable' or (not stdout and not capture_output):
        stdout = None
    elif stdout and not callable(stdout):
        verify_stdout = stdout
        stdout = lambda output: capture_callback(output, 'stdout')

    verify_stderr = None
    if stderr == 'disable' or (not stderr and not capture_output):
        stderr = None
    elif stderr and not callable(stderr):
        verify_stderr = stderr
        stderr = lambda output: capture_callback(output, 'stderr')

    if sudo:
        if not is_sudo_available():
            raise SudoNotAvailable()
        if isinstance(cmd, (str,os.PathLike)):
            cmd = f'sudo {cmd}'
        elif isinstance(cmd, bytes) or any(isinstance(arg, bytes) for arg in cmd):
            raise ValueError(f"Cannot use sudo with a bytes command")
        else:
            cmd = ['sudo', *cmd] # type: ignore

    proc = subprocess.Popen(cmd,
                        text=encoding not in {'unknown', 'bytes'},
                        encoding=encoding if encoding not in {'unknown', 'bytes'} else None,
                        shell=shell,
                        env=env,
                        stdout=subprocess.PIPE if stdout is not None else subprocess.DEVNULL,
                        stderr=subprocess.PIPE if stderr is not None else subprocess.DEVNULL,
                        stdin=subprocess.PIPE if input is not None else None)
    
    if stdout:
        Thread(target=enqueue_stream, args=[proc.stdout, 'stdout'], daemon=True).start()
    if stderr:
        Thread(target=enqueue_stream, args=[proc.stderr, 'stderr'], daemon=True).start()
    Thread(target=enqueue_process, args=[proc], daemon=True).start()

    if strip_stderr is None:
        strip_stderr = strip
        
    while True:
        source, data = queue.get()
        if source == 'stdout':
            if callable(stdout):
                if encoding != 'bytes':
                    data = _parse_string_stream(data, strip=strip)
                stdout(data) # type: ignore
        elif source == 'stderr':
            if callable(stderr):
                if encoding != 'bytes':
                    data = _parse_string_stream(data, strip=strip)
                stderr(data) # type: ignore
        else: # process
            cp = subprocess.CompletedProcess(cmd, returncode=data, stdout=captured.get('stdout'), stderr=captured.get('stderr'))    
            return verify_run_process(cp, check=check, stdout=verify_stdout, stderr=verify_stderr, logger=logger)


def verify_run_process(cp: subprocess.CompletedProcess, *,
                       check: int|Sequence[int]|bool = False,
                       stdout: Literal['disable','raise','warning','error']|None = None,
                       stderr: Literal['disable','raise','warning','error']|None = None,
                       strip: Literal['rstrip-newline','strip',True]|None = None,
                       strip_stderr: Literal['rstrip-newline','strip',True]|None = None,
                       bytes = False,
                       logger: logging.Logger|None = None) -> subprocess.CompletedProcess:
    
    if strip_stderr is None:
        strip_stderr = strip
    
    if not bytes:
        cp.stdout = _parse_string_stream(cp.stdout, strip=strip)
        cp.stderr = _parse_string_stream(cp.stderr, strip=strip_stderr)
    
    must_raise = False
    if check:
        if check is True:
            check = 0
        if not (cp.returncode in check if not isinstance(check, int) else cp.returncode == check):
            must_raise = True

    if cp.stdout:
        if stdout == 'raise':
            must_raise = True
        else:
            level = None
            if stdout == 'warning':
                level = logging.WARNING
            elif stdout == 'error':
                level = logging.ERROR
            if level:
                (logger or logging.getLogger(__name__)).log(level, "[stdout] %s", cp.stdout)
            
    if cp.stderr:
        if stdout == 'raise':
            must_raise = True
        else:
            level = None
            if stderr == 'warning':
                level = logging.WARNING
            elif stderr == 'error':
                level = logging.ERROR
            if level:
                (logger or logging.getLogger(__name__)).log(level, "[stderr] %s", cp.stderr)

    if must_raise:
        raise ProcessError(returncode=cp.returncode, cmd=cp.args, stdout=cp.stdout, stderr=cp.stderr)    
    return cp


def _parse_string_stream(output: str|bytes, *, strip: Literal['rstrip-newline','strip',True]|None = None) -> str|bytes:
    if isinstance(output, bytes): # Encoding might be unknown
        try:
            output = output.decode('utf-8')
        except UnicodeDecodeError:
            output = output.decode('cp1252')

    if strip:
        if isinstance(output, str):
            if strip == 'rstrip-newline':
                return output.rstrip('\r\n')
            elif strip == 'rstrip':
                return output.rstrip()
            else:
                return output.strip()
        else:
            raise TypeError(f"Cannot strip output of type {type(output).__name__}")
    else:
        return output

#endregion
