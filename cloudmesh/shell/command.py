import inspect
import shlex
import textwrap

from cloudmesh.common.dotdict import dotdict
from docopt import docopt
from cloudmesh.common.console import Console
from pprint import pprint, pformat
from cloudmesh.shell.variables import Variables
from cloudmesh.common.util import banner


class PluginCommand(object):
    pass


class CloudPluginCommand(object):
    pass


class ShellPluginCommand(object):
    pass


class HPCPluginCommand(object):
    pass


class CometPluginCommand(object):
    pass


def map_parameters(arguments, *args):
    """
    This command is useful to map parameters with -- to regular argument dicts for easier processing.

    :param arguments:
    :param args:
    :return:

    an example is

    map_parameters(arguments,
                       'active',
                       'cloud')

    where --active=ACTIVE is mapped to arguments["active"]
    and  --cloud=CLOUD is mapped to arguments["cloud"]

    as arguments is a dotdict, they can than for example be called as

    arguments.cloud

    """
    for arg in args:
        flag = "--" + arg
        if flag in arguments:
            arguments[arg] = arguments[flag]
        else:
            arguments[arg] = None


# noinspection PySingleQuotedDocstring,PyUnusedLocal
def command(func):
    '''
    A decorator to create a function with docopt arguments.
    It also generates a help function

    @command
    def do_myfunc(self, args):
        """ docopts text """
        pass

    will create

    def do_myfunc(self, args, arguments):
        """ docopts text """
        ...

    def help_myfunc(self, args, arguments):
        ... prints the docopt text ...

    :param func: the function for the decorator
    '''
    classname = inspect.getouterframes(inspect.currentframe())[1][3]
    name = func.__name__
    help_name = name.replace("do_", "help_")
    doc = textwrap.dedent(func.__doc__)

    def new(instance, args):
        # instance.new.__doc__ = doc
        # noinspection PyUnusedLocal
        try:
            argv = shlex.split(args)
            # pprint(argv)
            arguments = dotdict(docopt(doc, help=True, argv=argv))
            # pprint(arguments)
            verbose = int(Variables()["verbose"] or 0)
            if verbose > 9:
                s = pformat(arguments)
                banner(s, label="Arguments", color="BLUE")
            func(instance, args, arguments)
        except SystemExit as e:
            if args not in ('-h', '--help'):
                Console.error("Could not execute the command.")
                Console.error("Check usage..")
                # print (args)
                # print(e)
                # print(doc)

    new.__doc__ = doc
    return new


# noinspection PySingleQuotedDocstring,PyUnusedLocal
def basecommand(func):
    '''
    A decorator to create a function with docopt arguments.
    It also generates a help function

    @command
    def do_myfunc(self, args):
        """ docopts text """
        pass

    will create

    def do_myfunc(self, args, arguments):
        """ docopts text """
        ...

    def help_myfunc(self, args, arguments):
        ... prints the docopt text ...

    :param func: the function for the decorator
    '''
    classname = inspect.getouterframes(inspect.currentframe())[1][3]
    name = func.__name__
    help_name = name.replace("do_", "help_")
    doc = textwrap.dedent(func.__doc__)

    def new(instance, args):
        # instance.new.__doc__ = doc
        # noinspection PyUnusedLocal
        try:
            # print("ARGS", args)
            argv = shlex.split(args)
            # print ("ARGV", argv)
            arguments = docopt(doc, help=True, argv=argv)
            func(instance, args, arguments)
        except docopt.DocoptExit as e:
            if args not in ('-h', '--help'):
                Console.error("Could not execute the command.")
                Console.error("Check usage..")
            print(doc)

        except SystemExit as e:
            if args not in ('-h', '--help'):
                Console.error("Could not execute the command.")
                Console.error("Check usage..")
                print(e)
            print(doc)

    new.__doc__ = doc
    return new
