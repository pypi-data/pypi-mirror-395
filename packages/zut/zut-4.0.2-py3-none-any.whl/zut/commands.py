"""
Define and run commands and command-line applications.
"""
from __future__ import annotations

import logging
import re
import sys
import textwrap
from argparse import ArgumentParser, RawDescriptionHelpFormatter, _HelpAction, _SubParsersAction
from importlib import import_module
from pkgutil import iter_modules
from types import ModuleType
from typing import TYPE_CHECKING, Any, Callable, Sequence

from zut.config import CONFIG, Settings, configure, is_configured

if TYPE_CHECKING:
    from typing import Literal


_configure = configure  # For use in functions which have an overlapping `configure` argument

__shortcuts__ = (CONFIG, Settings, configure, is_configured)


def add_command(subparsers: _SubParsersAction[ArgumentParser], handle: Callable|ModuleType|str, *, name: str|None = None, help: str|None = None, add_arguments: Callable[[ArgumentParser]]|None = None, parents: Sequence[ArgumentParser]|None = None, **defaults):
    module: ModuleType|None = None
    command_instance: object|None = None
    actual_handle: Callable

    # Determine actual handle
    if isinstance(handle, (ModuleType,str)):
        if isinstance(handle, str):
            module = import_module(handle)
        else:
            module = handle
        
        command_class = getattr(module, 'Command', None)
        if command_class:
            command_instance = command_class()
            actual_handle = getattr(command_instance, 'handle')
        else:
            try:
                actual_handle = getattr(handle, 'handle')
            except AttributeError:
                try:
                    actual_handle = getattr(module, '_handle')
                except AttributeError:
                    handle_name = name if name else module.__name__.split('.')[-1]
                    try:
                        actual_handle = getattr(module, handle_name)
                    except AttributeError:
                        raise AttributeError(f"Cannot use module {module.__name__} as a command: no attribute named \"Command\", \"handle\" , \"_handle\" or \"{handle_name}\"") from None
    elif callable(handle):
        actual_handle = handle
    else:
        raise TypeError("Argument 'handle' in neither a module nor a callable")
    
    # Determine default parameters if necessary
    if not name:
        name = getattr(handle, 'name', None)
        if not name:
            if module is not None:
                name = module.__name__.split('.')[-1]
            else:
                name = actual_handle.__name__

            m = re.match(r'^_?(?:cmd|handle)_(.+)$', name)
            if m:
                name = m[1]
            name = name.strip('_') # pyright: ignore[reportOptionalMemberAccess]

    if not help:
        if command_instance is not None:
            help = getattr(command_instance, 'help', None)

    if add_arguments is None:
        add_arguments = getattr(actual_handle, 'add_arguments', None)
        if add_arguments is None:
            if command_instance is not None:
                add_arguments = getattr(command_instance, 'add_arguments', None)
            if add_arguments is None:
                if module is not None:
                    add_arguments = getattr(module, 'add_arguments', None)

    # Analyze doc
    doc: str|None = getattr(actual_handle, 'doc', None)
    if not doc:
        doc = actual_handle.__doc__
        if not doc:
            if command_instance is not None:
                doc = command_instance.__class__.__doc__
            if not doc:
                if module is not None:
                    doc = module.__doc__

    action_helps: dict[str,str] = {}
    description = None

    if doc:
        for line in doc.splitlines():
            m = re.match(r'^\s*:param (?P<dest>[a-zA_Z0-9]+):\s*(?P<help>[^\s].*)$', line)
            if m:
                action_helps[m['dest']] = m['help'].strip()
            
            else:
                if help is None:
                    stripped_line = line.strip()
                    if stripped_line:
                        help = line
                                
                if not action_helps:
                    description = (f'{description}\n' if description is not None else '') + line

    if not description:
        description = help
    
    # Build command parser
    kwargs = {}
    if parents is not None:
        kwargs['parents'] = parents
    cmdparser = subparsers.add_parser(name, help=help, description=get_description_text(description), formatter_class=RawDescriptionHelpFormatter, **kwargs)

    cmdparser.set_defaults(handle=actual_handle, **defaults)
    
    if add_arguments:
        add_arguments(cmdparser)
        for action in cmdparser._actions:
            if isinstance(action, _HelpAction):
                action.help = "Show this help message and exit."
            elif not action.help:
                action.help = action_helps.get(action.dest)

    return cmdparser


def add_commands(subparsers: _SubParsersAction[ArgumentParser], package: ModuleType|str):
    """
    Add all sub modules of the given package as commands.
    """
    if isinstance(package, str):
        package = import_module(package)
    elif not isinstance(package, ModuleType):
        raise TypeError(f"Invalid argument 'package': not a module")

    package_path = getattr(package, '__path__', None)
    if not package_path:
        raise TypeError(f"Invalid argument 'package': not a package")

    for module_info in iter_modules(package_path):
        if module_info.name.startswith('_'):
            continue # skip

        add_command(subparsers, f'{package.__name__}.{module_info.name}')


def create_command_parser(settings_or_prog: Settings|str|None = None, *, prog: str|None = None, version: str|None = None, doc: str|None = None, configure: bool|Literal['check','warn'] = 'check', log_colors = True, log_count_on_exit = True) -> CommandParser:
    settings: Settings|None = None
    if isinstance(settings_or_prog, Settings):
        settings = settings_or_prog
        
        if prog is None:
            prog = settings.name
        elif prog == '':
            prog = None

        if not doc and settings.module is not None:
            doc = getattr(settings.module, '__doc__', None)
    else:
        if isinstance(settings_or_prog, str):
            if prog is None:
                prog = settings_or_prog
            elif prog != settings_or_prog:
                raise ValueError(f"Argument 'prog' is provided both as positionnal and named parameter")
    
    if version is None:
        if settings is not None and settings.module is not None:
            version = getattr(settings.module, '__version__', None)
    
    if configure:
        if configure == 'check':
            if not is_configured():
                _configure(settings, log_colors=log_colors, log_count_on_exit=log_count_on_exit)
        else:
            _configure(settings, log_colors=log_colors, log_count_on_exit=log_count_on_exit, reconfigure=configure)

    return CommandParser(prog, version=version, description=get_description_text(doc), settings=settings)


def use_default_subparser(parser: ArgumentParser, name: str, args: list[str]|None = None) -> list[str]:
    """
    Transform the program arguments to use a default subparser if no subparser is mentionned.

    The result may be passed to `parse_args`.
    """
    if args is None:
        args = sys.argv[1:]

    help_option_strings = []
    option_string_nargs: dict[str,int|str|None] = {}
    subparser_names = []
    for action in parser._actions:
        if isinstance(action, _HelpAction):
            help_option_strings = action.option_strings
        elif isinstance(action, _SubParsersAction):
            for sp_name in action._name_parser_map.keys():
                subparser_names.append(sp_name)
        else:
            for op_name in action.option_strings:
                option_string_nargs[op_name] = action.nargs

    target_args = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in help_option_strings:
            # Help: modify nothing
            return args
        
        elif arg in option_string_nargs:
            target_args.append(arg)            
            nargs = option_string_nargs[arg]
            if isinstance(nargs, int):
                for _ in range(nargs):
                    i += 1
                    arg = args[i]
                    target_args.append(arg)
            else:
                # Special option: modify nothing
                return args
            
        elif arg in subparser_names:
            # A subparser is given: modify nothing
            return args
        
        else:
            # Use default subparser
            target_args.append(name)
            while i < len(args):
                target_args.append(args[i])
                i += 1
            break

        i += 1

    if not target_args:
        target_args = [name]

    return target_args


class CommandParser(ArgumentParser):
    """
    Create, configure and execute a command-line application.
    """
    def __init__(self, prog: str|None, *, version: str|None = None, settings: Settings|None = None, formatter_class = RawDescriptionHelpFormatter, **kwargs):
        super().__init__(prog, formatter_class=formatter_class, add_help=False, **kwargs)
        
        self.add_argument('-h', '--help', action='help', help = "Show this help message and exit.")
        
        if version is not None:
            version_text = (f"{self.prog} " if self.prog else "") + f"{version or '?'}"
            self.add_argument('--version', action='version', version=version_text, help = "Show this program version information and exit.")
        self.version = version

        self._logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__qualname__}")
        self._settings = settings
        self._commands = None

    @property
    def settings(self) -> Settings:
        if self._settings is None:
            raise AttributeError("No application settings registered")
        return self._settings

    @property
    def commands(self) -> _SubParsersAction[ArgumentParser]:
        if self._commands is None:
            self._commands = self.add_subparsers(title='commands')
        return self._commands # pyright: ignore[reportReturnType]
    
    def add_command(self, handle: Callable|ModuleType|str, *, name: str|None = None, help: str|None = None, add_arguments: Callable[[ArgumentParser]]|None = None, parents: Sequence[ArgumentParser]|None = None, **defaults):
        return add_command(self.commands, handle, name=name, help=help, add_arguments=add_arguments, parents=parents, **defaults)
    
    def run(self, *, default: str|None = None, args: list[str]|None = None) -> int:
        """
        Run the command application without exiting.
        """
        if default:
            args = use_default_subparser(self, default, args)
        elif args is None:
            args = sys.argv[1:]
        
        kwargs = vars(self.parse_args(args))
        return self.run_args(**kwargs)

    def run_args(self, *args, **kwargs):
        from zut.errors import SimpleError

        handle = kwargs.pop('handle', None)
    
        if not handle:
            self._logger.error("Missing command name")
            return 0
        
        try:        
            r = handle(*args, **kwargs)
            return get_exit_code(r)
        except SimpleError as err:
            self._logger.error(str(err))
            return 1
        except KeyboardInterrupt:
            self._logger.error("Exit on keyboard interrupt")
            return 1
        except BaseException as err:
            message = str(err)
            self._logger.exception(f"Exit on {type(err).__name__}{f': {message}' if message else ''}")
            return 1
    
    def exec(self, *, default: str|None = None, args: list[str]|None = None) -> None:
        """
        Run the command application and exit.
        """
        r = self.run(default=default, args=args)
        self._logger.debug("Exit with code %d", r)
        sys.exit(r)
    
    def exec_args(self, *args, **kwargs) -> None:
        r = self.run_args(*args, **kwargs)
        self._logger.debug("Exit with code %d", r)
        sys.exit(r)


def get_help_text(doc: str|None):
    if doc is None:
        return None
    
    doc = doc.strip()
    try:
        return doc[0:doc.index('\n')].strip()
    except:
        return doc
    

def get_description_text(doc: str|None):
    if doc is None:
        return None
    
    return textwrap.dedent(doc)


def get_exit_code(code: Any) -> int:
    if not isinstance(code, int):
        code = 0 if code is None or code is True else 1
    return code
