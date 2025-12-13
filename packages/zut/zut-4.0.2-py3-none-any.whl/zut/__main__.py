"""
Zut command-line tools.
"""
import logging
import sys
from argparse import ArgumentParser

from zut.commands import create_command_parser
from zut.secrets import get_random_string

_logger = logging.getLogger(__name__)

def main():    
    parser = create_command_parser('zut', doc=__doc__, log_count_on_exit=False)
    parser.add_command(pass_handle, name='pass')
    parser.add_command(gen_handle, name='gen')
    parser.exec()


#region Pass

def pass_add_arguments(parser: ArgumentParser):
    parser.add_argument('command', nargs='?', help="Command name: 'ls' (or 'list', this is the default), 'show', 'insert', 'rm' (or 'remove').")
    parser.add_argument('arg', nargs='?', help="Command argument (empty for 'ls', name of the password for 'show', 'insert' or 'rm').")

def pass_handle(command: str|None, arg: str|None):
    """
    Manage passwords using `pass` file structure (see: https://www.passwordstore.org/).
    """
    from zut.gpg import delete_pass, get_pass, list_pass_names, set_pass

    def ls_command():
        for name in list_pass_names():
            sys.stdout.write(f"{name}\n")
        return 0

    def show_command(name: str):
        value = get_pass(name)
        if value is None:
            _logger.error(f"'{name}' is not in the password store")
            return 1
        
        sys.stdout.write(f"{value}")

    def insert_command(name: str):
        password = input(f"Enter password for '{name}': ")
        password_confirmation = input(f"Retype password for '{name}': ")
        if password_confirmation != password:
            _logger.error(f"The entered passwords do not match")
            return 1

        set_pass(name, password)

    def rm_command(name: str):
        if not delete_pass(name, missing_ok=True):
            _logger.error(f"'{name}' is not in the password store")
            return 1

        return 0
    
    if not command or command in {'ls', 'list'}:
        if arg is not None:
            _logger.error(f"Invalid argument '{arg}' for '{command}' command")
            return 1
        else:
            return ls_command()
    elif command in {'show'}:
        if arg:
            return show_command(arg)
        else:
            return ls_command()
    elif command in {'insert'}:
        if not arg:
            _logger.error(f"Missing argument for '{command}' command")
            return 1
        else:
            return insert_command(arg)
    elif command in {'rm', 'remove'}:
        if not arg:
            _logger.error(f"Missing argument for '{command}' command")
            return 1
        else:
            return rm_command(arg)
    else:
        if arg:
            _logger.error(f"Invalid argument '{arg}' for 'show' command (passed argument is '{command}')")
            return 1
        else:
            return show_command(command)

setattr(pass_handle, 'add_arguments', pass_add_arguments)


def pass_main():
    parser = create_command_parser('pass', doc=pass_handle.__doc__, log_count_on_exit=False)

    pass_add_arguments(parser)

    ns = parser.parse_args()
    command = ns.command
    arg = ns.arg
    r = pass_handle(command, arg)
    exit(r)

#endregion


#region Gen

def gen_add_arguments(parser: ArgumentParser):
    parser.add_argument('-l', '--length', type=int, default=16, help="Number of characters to generate (default: %(default)s)")

def gen_handle(length = 16):
    """
    Generate a random string securely.
    """
    value = get_random_string(length=length)
    sys.stdout.write(value)

setattr(gen_handle, 'add_arguments', gen_add_arguments)
setattr(gen_handle, 'doc', get_random_string.__doc__)
    

#endregion


if __name__ == '__main__':
    main()
