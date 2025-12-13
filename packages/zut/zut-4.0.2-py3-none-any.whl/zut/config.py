"""
Define application configuration settings using `config.ini` files (parsed with standard library's `ConfigParser` and `Sectionproxy`).
"""
from __future__ import annotations

import logging
import os
import sys
from configparser import ConfigParser, NoOptionError, SectionProxy
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import IO, TYPE_CHECKING, Any, Callable, Iterable, Sequence, Union, overload

if TYPE_CHECKING:
    from typing import Literal

_logger = logging.getLogger(__name__)


#region Configure: shortcut (env + logging + config)

def is_configured() -> bool:
    return CONFIG.is_configured


def configure(settings: Settings|None = None, *, modules: list[ModuleType|str|tuple[str,Path]]|ModuleType|str|tuple[str,Path]|None = None, files: Sequence[str|os.PathLike]|str|os.PathLike|None = None, log_colors = True, log_count_on_exit = True, reconfigure: bool|Literal['warn'] = 'warn') -> Config:
    from zut.env import configure_env
    from zut.logging import configure_logging

    configure_env(reconfigure=reconfigure)
    
    configure_logging(reconfigure=reconfigure, colors=log_colors, count_on_exit=log_count_on_exit)

    if settings is not None and settings.module is not None:
        modules_list: list[ModuleType|str|tuple[str,Path]]
        if modules is None:
            modules_list = [settings.module]
        elif not isinstance(modules, list):
            modules_list = [modules, settings.module]
        else:
            modules_list = [*modules, settings.module]
        return configure_config(modules_list, files=files, reconfigure=reconfigure)
    else:
        return configure_config(modules, files=files, reconfigure=reconfigure)

#endregion


#region Configure config

def configure_config(modules: list[ModuleType|str|tuple[str,Path]]|ModuleType|str|tuple[str,Path]|None = None, *, files: Sequence[str|os.PathLike]|str|os.PathLike|None = None, reconfigure: bool|Literal['warn'] = 'warn') -> Config:
    """
    Initialize and return the `CONFIG` object.
    """
    # Determine all config paths
    config_paths = get_config_paths(modules, files=files)

    # Determine paths to actually load
    if CONFIG.paths is None:
        if _logger.isEnabledFor(logging.DEBUG):
            if len(config_paths) == 0:
                _logger.debug("No config file to load")
            elif len(config_paths) == 1:
                _logger.debug("Load config file: %s", config_paths[0])
            else:
                _logger.debug("Load config files:\n- %s", "\n- ".join(str(path) for path in config_paths))

        paths_to_load = config_paths
    
    elif config_paths == CONFIG.paths:
        _logger.debug("Ignore reconfiguration of config: same paths in the same order")
        return CONFIG

    elif not reconfigure:
        _logger.debug("Ignore reconfiguration of config: reconfiguration disabled")
        return CONFIG

    else:
        paths_to_load = [path for path in config_paths if path not in CONFIG.paths]
        
        level = logging.DEBUG if reconfigure is True else logging.WARNING
        if _logger.isEnabledFor(level):
            message = "Reconfiguration of config:"
            for path in config_paths:
                message += f"- {path}"
                if path in paths_to_load:
                    message += " (APPEND)"
                else:
                    message += " (ignored)"
            _logger.log(level, message)

    # Append paths
    CONFIG.read(paths_to_load)    
    return CONFIG


def get_config_paths(modules: list[ModuleType|str|tuple[str,Path]]|ModuleType|str|tuple[str,Path]|None = None, *, files: Sequence[str|os.PathLike]|str|os.PathLike|None = None) -> list[Path]:
    """
    Return the list of possible `config.ini` files for a package, depending on the app name (= slugified module name = section name and prog by default).

    - Defaults: `defaults.ini` from the package source path
    - System:  `C:/ProgramData/{app}/config.ini` on Windows, `/usr/local/share/{app}/config.ini` on Linux
    - User: `~/AppData/Roaming/{app}/config.ini` on Windows,   `~/.local/share/{app}/config.ini` on Linux
    - Repository: `../data/config.ini` or `../config.ini` from the package source path (if the package is not deployed in site-packages ~ not in a venv)
    - Non-module specific files: `files` argument
    - Working directory: `$PWD/config.ini`
    """
    from zut.paths import iter_app_data_files

    config_paths: list[Path] = []

    # Build list of app names and directories from the 'modules' argument
    apps_and_dirs: list[tuple[str,Path]] = []

    if modules is None:
        modules = []
    elif not isinstance(modules, list):
        modules = [modules]
    
    for module in modules:
        if isinstance(module, (str,ModuleType)):
            if isinstance(module, str):
                if '.' in module:
                    continue # ignore non top-level modules
                module = import_module(module.replace('-', '_'))
            else:
                if '.' in module.__name__:
                    continue # ignore non top-level modules

            try:
                module_paths = [Path(p) for p in module.__path__]
            except AttributeError:
                # Not a package
                if not (module.__file__ is None or not module.__file__.lower().endswith('.py')):
                    module_paths = [Path(module.__file__)]
                else:
                    raise ValueError("Module '%s' is not a package or a '.py' file" % module.__name__)
            if len(module_paths) != 1:
                raise ValueError("Package '%s' has not exactly one path: %s" % (module.__name__, module_paths))
            module_path = module_paths[0]

            if module_path.is_file():
                app = module.__name__.removesuffix('.py').replace('_', '-')
                dir = module_path.parent
            else:            
                app = module.__name__.replace('_', '-')
                dir = module_path
        elif isinstance(module, tuple):
            app, dir = module
            if '.' in app:
                continue # ignore non top-level modules
            app = app.replace('_', '-')
        else:
            raise TypeError("Invalid type: '%s'" % type(module))

        apps_and_dirs.append((app, dir))
    
    # Add specific files, from 'files' argument (not comming from 'modules' argument)
    if files:        
        # Ensure working directories comes first
        for path in iter_app_data_files({}, 'config.ini'):
            config_paths.append(path)

        # Add specific files
        if isinstance(files, (str,os.PathLike)):
            files = [files]

        for file in files:
            if not isinstance(file, Path):
                file = Path(file)
            file = file.absolute()
            if not file in config_paths and file.exists():
                config_paths.append(file)

    # Add config.ini files, comming from 'modules' argument
    for path in iter_app_data_files({app: dir.parent for app, dir in apps_and_dirs}, 'config.ini', include_data_parent=True):
        if not path in config_paths:
            config_paths.append(path)
    
    # Add defaults.ini files, comming from 'modules' argument
    for _, dir in apps_and_dirs:
        path = dir.joinpath('defaults.ini')
        if path.exists():
            config_paths.append(path)

    # Reverse results
    config_paths.reverse()
    return config_paths

#endregion


#region Config class (extends ConfigParser)

class Config(ConfigParser):
    def __init__(self, *args, converters={}, **kwargs):
        self._skip_configured_check = True
        if not 'password' in converters:
            from zut.secrets import resolve_secret
            converters['password'] = resolve_secret
        if not 'path' in converters:
            converters['path'] = Path
        super().__init__(*args, converters=converters, **kwargs)
        self.paths: list[Path]|None = None
        self._skip_configured_check = False
        
    def __getattribute__(self, key: str):
        if key.startswith('_') or key in {'read', 'is_configured', 'paths', 'converters'}:
            return super().__getattribute__(key)
        
        if not self._skip_configured_check and not self.is_configured:
            raise ValueError("Trying to access config (attribute '%s') while it was not configured" % key)
        
        return super().__getattribute__(key)
    
    def read(self, filenames: str|bytes|os.PathLike[str]|os.PathLike[bytes]|Iterable[str|bytes|os.PathLike[str]|os.PathLike[bytes]], encoding: str|None = None) -> list[str]:
        if encoding is None:
            encoding = 'utf-8'
        
        additional_paths: list[Path] = []
        if self.paths is None:
            self.paths = []

        if isinstance(filenames, (str,bytes,os.PathLike)):
            filenames = [filenames]
        for path in filenames:
            if not isinstance(path, Path):
                try:
                    path = Path(path) # pyright: ignore[reportArgumentType]
                except:
                    raise TypeError("Config cannot be used with input of type '%s'", type(path))
            additional_paths.append(path)
            self.paths.append(path)
        
        return super().read(additional_paths, encoding)
    
    @property
    def is_configured(self):
        return self.paths is not None

    if TYPE_CHECKING:
        @overload
        def getpassword(self, section: str, option: str) -> str: # pyright: ignore[reportNoOverloadImplementation]
            ...
        
        @overload
        def getpassword(self, section: str, option: str, *, fallback: str|None = None) -> str|None:
            ...

        @overload
        def getpath(self, section: str, option: str) -> Path: # pyright: ignore[reportNoOverloadImplementation]
            ...
        
        @overload
        def getpath(self, section: str, option: str, *, fallback: str|os.PathLike|None = None) -> Path|None:
            ...


CONFIG = Config()
""" Global configuration object, must be initialized with `configure`, `configure_config` or `configure_settings`. """

#endregion


#region Settings class (extends SectionProxy)

_option_attributes: dict[type[Settings], dict[str,_OptionAttribute]] = {}


class Settings(SectionProxy):
    module: ModuleType|None

    def __init__(self, module: ModuleType|str|None = None, *, name: str|None = None):
        """
        :param name: Name of the configuration section (if module is not given or if the section is not the module's default).
        """
        self._data_dir = None

        if module is None:
            self.module = None
        elif isinstance(module, str):
            self.module = import_module(module.replace('-', '_'))
        else:
            self.module = module

        if not name:
            if self.module is not None:
                name = self.module.__name__.split('.')[-1].replace('_', '-')
            else:
                raise ValueError("Missing 'module' or 'name' (section) argument")

        CONFIG._skip_configured_check = True
        super().__init__(CONFIG, name)
        CONFIG._skip_configured_check = False

    if TYPE_CHECKING:
        @overload
        def getpassword(self, option: str, *, fallback: str) -> str: # pyright: ignore[reportNoOverloadImplementation]
            ...
        
        @overload
        def getpassword(self, option: str, *, fallback: str|None = None) -> str|None:
            ...

        @overload
        def getpath(self, option: str, *, fallback: str|os.PathLike) -> Path: # pyright: ignore[reportNoOverloadImplementation]
            ...
        
        @overload
        def getpath(self, option: str, *, fallback: str|os.PathLike|None = None) -> Path|None:
            ...

    def _get_repository_path(self):        
        if self.module is None:
            return None
        
        module_path = None
        try:
            if len(self.module.__path__) == 1:
                module_path = Path(self.module.__path__[0])
        except:
            return None

        if module_path and not 'site-packages' in module_path.parts:
            return module_path.parent
        else:
            return None
    
    @property
    def data_dir(self) -> Path:
        """
        Return application data directory
        """
        if self._data_dir is None:
            from zut.paths import get_app_data_dir
            self._data_dir = get_app_data_dir(self.name, repository=self._get_repository_path())
        return self._data_dir
        
    @overload
    def normalize_data_path(self, path: str|os.PathLike, *, mkparents = False, **kwargs) -> Path:
        ...

    @overload
    def normalize_data_path(self, path: IO, *, mkparents = False, **kwargs) -> IO:
        ...

    @overload
    def normalize_data_path(self, path: None, *, mkparents = False, **kwargs) -> None:
        ...

    def normalize_data_path(self, path: str|os.PathLike|IO|None, *, mkparents = False, **kwargs) -> Path|IO|None:
        from zut.paths import normalize_path
        return normalize_path(path, self.data_dir, mkparents=mkparents, **kwargs)
        
    @property
    def parser(self) -> Config:
        return super().parser # pyright: ignore[reportReturnType]
        
    def __getattribute__(self, name: str):
        if name.startswith('_') or name in {'name', 'module', 'data_dir', 'normalize_data_path', 'parser', 'get_option_attributes', 'get_option_attribute_value'}:
            return super().__getattribute__(name)
        
        if not CONFIG._skip_configured_check and not CONFIG.is_configured:
            raise ValueError("Trying to access settings section '%s' while config was not configured" % (self.name))

        try:
            return self.get_option_attribute_value(name)
        except AttributeError:
            pass # will use super method

        return super().__getattribute__(name)

    def get_option_attribute_value(self, option: str):
        attr = self._get_option_attributes().get(option)
        if attr is None:
            raise AttributeError("No option attribute '%s'" % option)

        if attr.type is None:
            raise TypeError("Internal error: 'type' not set for settings option '%s' of section '%s" % (attr.name, self.name))
        
        getter: Callable|None
        if attr.type == str:
            getter = self.get
        elif attr.type == bool:
            getter = self.getboolean
        elif attr.type == Path:
            getter = self.getpath
        else:
            try:
                getter = super().__getattribute__(f"get{attr.type.__name__.lower()}")
            except AttributeError:
                getter = None
        
        if getter is None:
            raise TypeError("No converter registered for type '%s' (settings option '%s' of section '%s')" % (attr.type, attr.name, self.name))

        value = getter(attr.name, fallback=self.__class__._default)
        if value is self.__class__._default:
            if attr.default_value is not None:
                return attr.default_value
            elif attr.required:
                raise NoOptionError(attr.name, self.name)
            else:
                return None
        else:
            return value

    @classmethod
    def _get_option_attributes(cls) -> dict[str,_OptionAttribute]:
        if cls in _option_attributes:
            return _option_attributes[cls]
        
        if cls == Settings:
            _option_attributes[cls] = {}
            return _option_attributes[cls]
        
        base_attrs: set[str]
        try:
            base_attrs = Settings._base_attrs
        except AttributeError:
            base_attrs = set(dir(Settings))
            Settings._base_attrs = base_attrs

        attrs = {}

        for attr_name, typing in cls.__annotations__.items():
            attr = _OptionAttribute(attr_name)
            attrs[attr_name] = attr
            attr.set_annotation_typing(typing)

        for attr_name in dir(cls):
            if attr_name.startswith('_') or attr_name in base_attrs:
                continue
            default_value = getattr(cls, attr_name)
            attr = attrs.get(attr_name)
            if not attr:
                attr = _OptionAttribute(attr_name)
                attrs[attr_name] = attr
            attr.set_default_value(default_value)

        _option_attributes[cls] = attrs
        return attrs

    _default = object()


class _OptionAttribute:
    def __init__(self, name: str):
        self.name = name
        self.type: type|None = None
        self.required: bool|None = None
        self.default_value: Any = None
        self.annotation_typing: type|None = None

    def set_annotation_typing(self, typing: type):
        self.annotation_typing = typing

        if sys.version_info >= (3, 14):
            is_union = isinstance(typing, Union)
        elif sys.version_info >= (3, 10):
            from types import UnionType
            is_union = isinstance(typing, UnionType)
        else:
            raise NotImplementedError("Cannot use annotation typing for settings option attribute for Python <= 3.10")
            # This would oblige the class to be declared in a Python module containing `from __future__ import annotations`,
            # which would make annotations appear as strings instead of types in set_annotation_typing()

        types: list[type]
        if is_union:
            types = [t for t in getattr(typing, '__args__') or []]
        else:
            types = [typing]
    
        try:
            types.remove(type(None))
            self.required = False
        except Exception as err:
            self.required = True

        if len(types) != 1:
            raise ValueError("Unsupported type annotation for option attribute '%s': '%s'" % (self.name, typing))
        self.type = types[0]
    
    def set_default_value(self, value: Any):
        self.default_value = value  
        value_type = type(value)

        if issubclass(value_type, Path):
            value_type = Path

        if self.type is not None:
            if value is not None and value_type != self.type:
                raise TypeError("Invalid type '%s' for default value of option attribute '%s': expected '%s' because of annotations" % (value_type, self.name, self.type))
        else:
            self.type = value_type
        
        if self.required is None:
            self.required = value is not None

#endregion
