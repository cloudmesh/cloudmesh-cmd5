import inspect
import shlex
import textwrap

from cloudmesh.common.dotdict import dotdict
from docopt import docopt
from cloudmesh.common.console import Console


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
            arguments = dotdict(docopt(doc, help=True, argv=argv))
            func(instance, args, arguments)
        except SystemExit as e:
            if args not in ('-h', '--help'):
                Console.error("Could not execute the command.")
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
        try:
            # print("ARGS", args)
            argv = shlex.split(args)
            # print ("ARGV", argv)
            arguments = docopt(doc, help=True, argv=argv)
            func(instance, args, arguments)
        except SystemExit as e:
            if args not in ('-h', '--help'):
                Console.error("Could not execute the command.")
                print(e)
            print(doc)

    new.__doc__ = doc
    return new
