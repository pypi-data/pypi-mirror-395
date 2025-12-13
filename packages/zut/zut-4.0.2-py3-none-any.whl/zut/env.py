"""
Environment helpers: load `.env` file, detect specificities, install pip packages.
"""
from __future__ import annotations

import logging
import os
import re
import subprocess
import sys
from configparser import ConfigParser
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from typing import Literal


#region Configure env

_configured_env: list[Path]|None = None

def configure_env(paths: str|os.PathLike|Sequence[str|os.PathLike]|None = None, *, encoding = 'utf-8-sig', parents = False, reconfigure: bool|Literal['warn'] = 'warn') -> None:
    """
    Load `.env` from the given or current directory (or the given file if any) to environment variables.
    If the given file is a directory, search `.env` in this directory.
    If `parents` is True, also search if parent directories until a `.env` file is found.
    """
    global _configured_env

    from zut.logging import is_log_preinit_enabled_for, log_preinit
    from zut.paths import find_to_root

    # Determine all env paths
    if not paths:
        paths = [Path('.env')]
    elif isinstance(paths, (str,os.PathLike)):
        paths = [paths]

    env_paths: list[Path] = []
    for path in paths:
        if not isinstance(path, Path):
            path = Path(path)

        if path.is_dir():
            if parents:
                path = find_to_root('.env', path)
            else:
                path = path.joinpath('.env').absolute()
            if not path or not path.exists():
                continue
            env_paths.append(path)

        elif not path.is_file() and parents:
            if path.parent:
                path = find_to_root(path.name, path.parent)
                if path:
                    env_paths.append(path)
            
        elif path.exists():
            env_paths.append(path.absolute())

    # Determine paths to actually load
    if _configured_env is None:
        if is_log_preinit_enabled_for(logging.DEBUG):
            if len(env_paths) == 0:
                log_preinit(logging.DEBUG, "No env file to load")
            elif len(env_paths) == 1:
                log_preinit(logging.DEBUG, "Load env file: %s", env_paths[0])
            else:
                log_preinit(logging.DEBUG, "Load env files:\n- %s", "\n- ".join(str(path) for path in env_paths))

        paths_to_load = env_paths

    elif env_paths == _configured_env:
        log_preinit(logging.DEBUG, "Ignore reconfiguration of env: same paths in the same order")
        return

    elif not reconfigure:
        log_preinit(logging.DEBUG, "Ignore reconfiguration of env: reconfiguration disabled")
        return

    else:
        paths_to_load = [path for path in env_paths if path not in _configured_env]
        
        level = logging.DEBUG if reconfigure is True else logging.WARNING
        if is_log_preinit_enabled_for(level):
            message = "Reconfiguration of env:"
            for path in env_paths:
                message += f"- {path}"
                if path in paths_to_load:
                    message += " (APPEND)"
                else:
                    message += " (ignored)"
            log_preinit(level, message)

    # Load env paths
    if _configured_env is None:
        _configured_env = []

    for path in paths_to_load:        
        parser = ConfigParser()
        with open(path, 'r', encoding=encoding, newline=None) as fp:
            parser.read_string("[env]\n" + fp.read())

        for name, value in parser['env'].items():
            m = re.match(r'^"(.+)"$', value)
            if m:
                value = m[1].replace('\\"', '"')
            os.environ[name] = value

        _configured_env.append(path)

    # Ensure NO_PROXY contains localhost and 127.0.0.1 in case HTTP_PROXY and HTTPS_PROXY are given
    # This permit to avoid a lot of misconfigurations that are hard to debug
    if (os.environ.get('HTTP_PROXY') or os.environ.get('HTTPS_PROXY')):
        no_proxy = os.environ.get('NO_PROXY', '').split(',')
        fix = False

        for host in ['localhost', '127.0.0.1']:
            if not host in no_proxy:
                no_proxy.append(host)
                fix = True

        if fix:
            log_preinit(logging.WARNING, "Add missing localhost or 127.0.0.1 in NO_PROXY")
            os.environ['NO_PROXY'] = ','.join(no_proxy)

#endregion


#region Detect environment specificities

_in_docker_container: bool|None = None
_desktop_environment: str|None = None


def in_docker_container():
    """
    Indicate whether the application is running in a Docker container.
    """
    global _in_docker_container
    if _in_docker_container is None:
        _in_docker_container = os.path.exists('/.dockerenv')
    return _in_docker_container


def get_desktop_environment() -> str:
    # From http://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment
    # and http://ubuntuforums.org/showthread.php?t=652320
    # and http://ubuntuforums.org/showthread.php?t=652320
    # and http://ubuntuforums.org/showthread.php?t=1139057
    global _desktop_environment
    if _desktop_environment is not None:
        return _desktop_environment
    
    if sys.platform in ["win32", "cygwin"]:
        _desktop_environment = 'windows'
        return _desktop_environment
    elif sys.platform == "darwin":
        _desktop_environment = 'mac'
        return _desktop_environment        
    else: # Most likely either a POSIX system or something not much common
        def is_running(process):
            # From http://www.bloggerpolis.com/2011/05/how-to-check-if-a-process-is-running-using-python/
            # and http://richarddingwall.name/2009/06/18/windows-equivalents-of-ps-and-kill-commands/
            try: # Linux/Unix
                s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE, text=True)
            except: # Windows
                s = subprocess.Popen(["tasklist", "/v"], stdout=subprocess.PIPE, text=True)
            if s.stdout is not None:
                for x in s.stdout:
                    if re.search(process, x):
                        return True
            return False

        def detect() -> str:
            desktop_session = os.environ.get("DESKTOP_SESSION")
            if desktop_session is not None: #easier to match if we doesn't have  to deal with caracter cases
                desktop_session = desktop_session.lower()
                if desktop_session in ["gnome","unity", "cinnamon", "mate", "xfce4", "lxde", "fluxbox", 
                                        "blackbox", "openbox", "icewm", "jwm", "afterstep","trinity", "kde"]:
                    return desktop_session
                ## Special cases ##
                # Canonical sets $DESKTOP_SESSION to Lubuntu rather than LXDE if using LXDE.
                # There is no guarantee that they will not do the same with the other desktop environments.
                elif "xfce" in desktop_session or desktop_session.startswith("xubuntu"):
                    return "xfce4"
                elif desktop_session.startswith('ubuntustudio'):
                    return 'kde'
                elif desktop_session.startswith('ubuntu'):
                    return 'gnome'     
                elif desktop_session.startswith("lubuntu"):
                    return "lxde" 
                elif desktop_session.startswith("kubuntu"): 
                    return "kde" 
                elif desktop_session.startswith("razor"): # e.g. razorkwin
                    return "razor-qt"
                elif desktop_session.startswith("wmaker"): # e.g. wmaker-common
                    return "windowmaker"
            if os.environ.get('KDE_FULL_SESSION') == 'true':
                return "kde"
            elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):
                if not "deprecated" in os.environ.get('GNOME_DESKTOP_SESSION_ID', ''):
                    return "gnome2"
            #From http://ubuntuforums.org/showthread.php?t=652320
            elif is_running("xfce-mcs-manage"):
                return "xfce4"
            elif is_running("ksmserver"):
                return "kde"
            return "unknown"
            
        _desktop_environment = detect()
        return _desktop_environment


def find_gdal_library_path() -> str|None:
    """
    Find GDAL library.

    See: https://docs.djangoproject.com/en/5.2/ref/contrib/gis/install/geolibs/
    """
    from ctypes.util import find_library

    if os.name == "nt":
        lib_names = [
            "libgdal-35", # PostGIS installed on Windows with PostgreSQL 17 or 18 StackBuilder.
            "gdal311",
            "gdal310",
            "gdal309",
            "gdal308",
            "gdal307",
            "gdal306",
            "gdal305",
            "gdal304",
            "gdal303",
            "gdal302",
            "gdal301",
            "gdal300",
        ]
    else:
        lib_names = [
            "gdal",
            "GDAL",
            "gdal3.11.0",
            "gdal3.10.0",
            "gdal3.9.0",
            "gdal3.8.0",
            "gdal3.7.0",
            "gdal3.6.0",
            "gdal3.5.0",
            "gdal3.4.0",
            "gdal3.3.0",
            "gdal3.2.0",
            "gdal3.1.0",
            "gdal3.0.0",
        ]

    for name in lib_names:
        path = find_library(name)
        if path:
            return path


def find_geos_library_path() -> str|None:
    """
    Find GEOS library.

    See: https://docs.djangoproject.com/en/5.2/ref/contrib/gis/install/geolibs/
    """
    from ctypes.util import find_library

    if os.name == "nt":
        lib_names = [
            "geos_c",
            "libgeos_c", # PostGIS installed on Windows with PostgreSQL 17 or 18 StackBuilder.
            "libgeos_c-1",
        ]
    else:
        lib_names = [
            "geos_c",
            "GEOS"
        ]
    
    for name in lib_names:
        path = find_library(name)
        if path:
            return path

#endregion


#region PyPI

def ensure_pip_dependency(modules: str|list[str]|dict[str,str|None], *, yes = False):
    if isinstance(modules, dict):
        _modules = modules
    elif isinstance(modules, str):
        _modules = {modules: None}
    else:
        _modules = {module: None for module in modules}

    missing_packages = []
    for module in _modules:
        try:
            import_module(module)
        except ModuleNotFoundError:
            package = _modules.get(module) or module.replace('_', '-')
            missing_packages.append(package)

    if not missing_packages:
        return False
    
    missing_packages_str = ' '.join(missing_packages)
    in_str = os.path.dirname(os.path.dirname(sys.executable))
    if not yes:        
        from zut.console import Color
        response = input(f"Confirm installation of {Color.YELLOW}%s{Color.RESET} in %s? (y/N) " % (missing_packages_str, in_str))
        if response.lower() != 'y':
            sys.exit(1)

    from zut.logging import log_preinit
    log_preinit(logging.INFO, "Install %s in %s", missing_packages_str, in_str)
    subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_packages])
    return True

#endregion
