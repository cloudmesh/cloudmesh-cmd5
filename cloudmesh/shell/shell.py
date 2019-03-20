#
# in our rest architecture we want to interface to the backend systems while
# using a secure rest service. I
# Internally we will use the many functions that cloudmesh_client provides.
# Before we use them we need to implement some elementary functions
# lets first do administrative functions in an admin command

# pseudo code: task implement plugin

from __future__ import print_function

import importlib
import inspect
import os
import pkgutil
import pydoc
import shelve
import sys
import textwrap
import subprocess
import requests
import yaml

from cmd import Cmd

from cloudmesh.common.Printer import Printer
from cloudmesh.common.Shell import Shell
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.dotdict import dotdict
from cloudmesh.common.util import path_expand
from cloudmesh.common.default import Default
from cloudmesh.common.error import Error
from cloudmesh.common.console import Console

import cloudmesh
import cloudmesh.common
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command, basecommand
from cloudmesh.shell.plugin import PluginManager
from cloudmesh.shell.variables import Variables


def print_list(elements):
    """
    prints the element of a list
    :param elements: the elements to be printed
    """
    for name in elements:
        print("*", name)


class Plugin(object):
    """
    Some simple methods to manage dynamic namespace plugins for cloudmesh.
    """

    @classmethod
    def modules(cls):
        """
        list of cloudmesh modules in the cloudmesh namespace
        :return: list of modules
        """
        module_list = []
        package = cloudmesh
        for importer, modname, ispkg in pkgutil.walk_packages(
                path=package.__path__,
                prefix=package.__name__ + '.',
                onerror=lambda x: None):
            module_list.append(modname)
        return module_list

    @classmethod
    def classes(cls):
        """
        list of the commands in the cloudmesh namespace under cloudmesh.ext.command
        :return: list of the commands
        """
        module_list = cls.modules()
        commands = []
        for module_name in module_list:
            if module_name.startswith(
                    'cloudmesh.') and '.command.' in module_name:
                commands.append(module_name)
        return commands

    @classmethod
    def name(cls, command):
        """
        creates a name for a modules starting with do_
        :param command: returns a tuple with the module location and tge do_function
        :return:
        """
        command_name = "do_" + command

        class_name = "cloudmesh." + command + ".command." + command + "." \
                     + command.capitalize() + "Command"

        return class_name, command_name

    @classmethod
    def class_name(cls, command):
        """
        creates the default filename in which the module is defined
        :param command:  the name of the command
        :return: cloudmesh.ext.command.<command>+command.<Command>
        """
        return "cloudmesh." + command + ".command." + command + "." \
               + command.capitalize() + "Command"

    @classmethod
    def load(cls, commands=None):
        """

        :param commands: If None the commands will be found from import cloudmesh
                         Otherwise the commands can be explicitly specified with

                          commands = [
                            'cloudmesh.ext.command.bar.BarCommand',
                            'cloudmesh.ext.command.foo.FooCommand',
                            ]
                          A namespace package must exists. Foo and Bar ar just examples

        :return: the classes of the command
        """

        if commands is None:
            commands = [c.split('.')[-1] for c in cls.classes()]

        # print_list(commands)

        class_commands = [cls.class_name(c) for c in commands]
        commands = [getattr(importlib.import_module(mod), cls) for (mod, cls) in
                    (commands.rsplit(".", 1) for commands in class_commands)]
        return commands


Plugin.load()

PluginCommandClasses = type(
    'CommandProxyClass',
    tuple(PluginCommand.__subclasses__()),
    {})


class CMShell(Cmd, PluginCommandClasses):
    """
    The command shell that inherits all commands from PluginCommand
    """
    prompt = 'cms> '
    banner = textwrap.dedent("""
    +-------------------------------------------------------+
    |   ____ _                 _                     _      |
    |  / ___| | ___  _   _  __| |_ __ ___   ___  ___| |__   |
    | | |   | |/ _ \| | | |/ _` | '_ ` _ \ / _ \/ __| '_ \  |
    | | |___| | (_) | |_| | (_| | | | | | |  __/\__ \ | | | |
    |  \____|_|\___/ \__,_|\__,_|_| |_| |_|\___||___/_| |_| |
    +-------------------------------------------------------+
    |                  Cloudmesh CMD5 Shell                 |
    +-------------------------------------------------------+
    """)

    def precmd(self, line):
        StopWatch.start("command")
        return line

    def postcmd(self, stop, line):
        StopWatch.stop("command")

        try:
            variable = Variables()
            if "timer" not in variable:
                variable["timer"] = "off"
            if variable["timer"].lower() in ['on', 'true']:
                print("Timer: {:.4f}s ({})".format(StopWatch.get("command"),
                                                   line.strip()))
            variable.close()
        except Exception as e:
            Error.traceback(error=e)

        return stop

    # noinspection PyMethodMayBeStatic
    def replace_vars(self, line):

        # self.update_time()

        variable = Variables()
        newline = line

        if len(variable) is not None:
            for name in variable.data:
                value = str(variable[name])
                newline = newline.replace("$" + name, value)
                newline = newline.replace("var." + name, value)
            for v in os.environ:
                name = v.replace('os.', '')
                if name in newline:
                    value = os.environ[name]
                    newline = newline.replace("os." + v, value)

            default = Default()
            if default is not None:
                for v in default.data:
                    name = "default." + v.replace(",", ".")
                    value = default.data[v]
                    if name in newline:
                        newline = newline.replace(name, value)

                # replace if global is missing

                global_default = default["global"]
                if global_default is not None:
                    for v in global_default:
                        name = "default." + v
                        value = global_default[v]
                        if name in newline:
                            newline = newline.replace(name, value)

            default.close()
            variable.close()

        newline = path_expand(newline)
        return line, newline

    def onecmd(self, line):
        """Interpret the argument as though it had been typed in response
        to the prompt.

        This may be overridden, but should not normally need to be;
        see the precmd() and postcmd() methods for useful execution hooks.
        The return value is a flag indicating whether interpretation of
        commands by the interpreter should stop.

        """
        oldline, line = self.replace_vars(line)

        # -----------------------------
        # print comment lines, but do not execute them
        # -----------------------------
        if line.startswith('#') \
                or line.startswith('//') \
                or line.startswith('/*'):
            print(line)
            return ""

        if line.startswith('!'):
            os.system(line[1:])

            return ""
        # if line is None:
        #    return ""

        # if line.startswith("!"):
        #    line.replace("!", "! ")
        # line = self.var_replacer(line)
        # if line != "hist" and line:
        #    self._hist += [line.strip()]
        # if line.startswith("!") or line.startswith("shell"):
        #    self.do_shell_exec(line[1:])
        #    return ""
        cmd, arg, line = self.parseline(line)

        if line.startswith("$") or line.startswith('var.'):
            line = line.replace("$", "", 1)
            line = line.replace("var.", "", 1)
            print("FIND>", line, "<", sep='')
            variable = Variables()
            print(variable[line])
            variable.close()
            return ""

        # -----------------------------
        # handle empty line
        # -----------------------------
        if not line:
            return self.emptyline()

        # -----------------------------
        # handle file execution
        # -----------------------------
        #
        # this does not yet work
        #
        # if os.path.isfile(line):
        #    print ("... execute", line)
        #    self.do_exec(line)
        #    return ""

        if cmd != '':
            try:
                func = getattr(self, 'do_' + cmd)
                return func(arg)

            except AttributeError as e:

                variables = Variables()
                trace = "T" in variables['trace']
                debug = "T" in variables['debug']

                command_missing = "'CMShell' object has no attribute 'do_{cmd}'".format(
                    cmd=cmd)

                if e.args[0] == command_missing:
                    Console.error(
                        "this command does not exist: '{cmd}'".format(cmd=cmd),
                        traceflag=False)
                else:
                    Error.traceback(error=e, debug=debug, trace=trace)

                # noinspection PyUnusedLocal
                cmd = None
                line = oldline

        return ""

    # noinspection PyUnusedLocal
    @command
    def do_shell(self, args, arguments):
        """
        ::

           Usage:
                shell COMMAND
                
            Arguments:
                COMMAND  the command to be executed

           Description:
                shell COMMAND  executes the command 

        """
        # print ("Executing>", args, "<", sep='')
        # os.system(args)
        os.system(str(args))
        return ""

    '''
    #
    # List all commands that start with do
    #
    # noinspection PyMethodOverriding
    @command
    def do_help(self, args, arguments):
        """
        ::
           Usage:
                help

           Description:
                help - List of all registered commands

        """
        print("Help")
        print("====")
        method_list = [n for n, v in inspect.getmembers(self, inspect.ismethod)]
        function_list = [n for n, v in inspect.getmembers(self, inspect.isfunction)]

        commands = method_list + function_list

        for c in sorted(commands):
            if c.startswith("do_"):
                print(c.replace("do_", ""), end=' ')
        print()
        return ""

    '''

    def do_help(self, arg):
        """
        ::

            Usage:
                help
                help COMMAND

            Description:
                List available commands with "help" or detailed help with
                "help COMMAND".
        """

        if arg:
            try:
                func = getattr(self, 'help_' + arg)
            except AttributeError:
                try:
                    doc = getattr(self, 'do_' + arg).__doc__
                    if doc:
                        self.stdout.write("Command {arg}\n".format(arg=arg))
                        self.stdout.write(len("Command " + arg) * "=")
                        self.stdout.write("\n")

                        # doc = doc.replace("::\n\n", "")
                        self.stdout.write("%s\n" % str(doc))
                        return
                except AttributeError:
                    pass
                self.stdout.write("%s\n" % str(self.nohelp % (arg,)))
                return
            func()
        else:
            names = self.get_names()
            cmds_doc = []
            cmds_undoc = []
            help_page = {}
            for name in names:
                if name[:5] == 'help_':
                    help_page[name[5:]] = 1
            names.sort()
            # There can be duplicates if routines overridden
            prevname = ''
            for name in names:
                if name[:3] == 'do_':
                    if name == prevname:
                        continue
                    prevname = name
                    cmd = name[3:]
                    if cmd in help_page:
                        cmds_doc.append(cmd)
                        del help_page[cmd]
                    elif getattr(self, name).__doc__:
                        cmds_doc.append(cmd)
                    else:
                        cmds_undoc.append(cmd)

            self.stdout.write("%s\n" % str(self.doc_leader))
            self.print_topics(self.doc_header, cmds_doc, 15, 80)
            self.print_topics(self.misc_header, list(help_page.keys()), 15, 80)
            self.print_topics(self.undoc_header, cmds_undoc, 15, 80)

    def help_help(self):
        """
        ::

            Usage:
                help
                help COMMAND

            Description:
                List available commands with "help" or detailed help with
                "help COMMAND".
        """
        print(textwrap.dedent(self.help_help.__doc__))

    # noinspection PyUnusedLocal
    @command
    def do_info(self, args, arguments):
        """
        ::

          Usage:
                info [path|commands|files|cloudmesh]

          Description:
                info
                    provides internal info about the shell and its packages

        """
        arguments = dotdict(arguments)

        module_list = Plugin.modules()

        if arguments.commands:
            commands = Plugin.classes()
            print_list(commands)
        elif arguments.path:
            path_list = cloudmesh.__path__
            print_list(path_list)
        elif arguments.files:
            commands = Plugin.modules()
            for command in commands:
                try:
                    r = inspect.getfile(command)
                    print("*", type(command))
                except Exception as e:
                    print(e)
        elif arguments.help:
            for name in module_list:
                p = "cloudmesh." + name
                help_string = p + " not found."
                # noinspection PyBroadException
                try:
                    help_string = pydoc.render_doc(p,
                                                   "Help on %s" + "\n" + 79 * "=")
                except Exception as e:
                    pass
                print(help_string)

        else:
            print_list(module_list)

    def preloop(self):
        """adds the banner to the preloop"""

        lines = textwrap.dedent(self.banner).split("\n")
        for line in lines:
            # Console.cprint("BLUE", "", line)
            print(line)

    # noinspection PyUnusedLocal,PyPep8Naming,PyMethodMayBeStatic
    def do_EOF(self, args):
        """
        ::

          Usage:
            EOF

          Description:
            Command to the shell to terminate reading a script.
        """
        return True

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def do_quit(self, args):
        """
        ::

          Usage:
            quit

          Description:
            Action to be performed when quit is typed

        """
        return True

    do_q = do_quit

    def emptyline(self):
        return

    # noinspection PyUnusedLocal
    @command
    def do_plugin(self, args, arguments):
        """
        ::

          Usage:
            plugin install PLUGIN [-s]
            plugin uninstall PLUGIN
            plugin list
            plugin ? [--format=FORMAT]

          Arguments:
            PLUGIN   the name of the plugin

          Description:
            plugin available
                lists the available plugins
            plugin list
                lists the plugin
            plugin install
                installs the given plugin
            plugin uninstall
                uninstalls the given plugin

        """
        if arguments['--format'] is None:
            arguments['--format'] = 'table'

        # print (arguments)

        if arguments.install:
            plugins = PluginManager()
            plugins.load()
            if arguments["-s"]:
                plugins.source_install(arguments.PLUGIN)
            else:
                plugins.pip_install(arguments.PLUGIN)

        elif arguments.uninstall:
            plugins = PluginManager()
            plugins.load()
            plugins.uninstall(arguments.PLUGIN)

        elif '?' in arguments:

            plugins = PluginManager()
            plugins.load()

            print(Printer.write(plugins.data['plugins'],
                                output=arguments["--format"],
                                order=["name", "status", "description"],
                                sort_keys="name"))

    # noinspection PyUnusedLocal,PyPep8
    @basecommand
    def do_version(self, args, arguments):
        """
        ::

          Usage:
            version pip [PACKAGE]
            version [--format=FORMAT] [--check=CHECK]
           

          Options:
            --format=FORMAT  the format to print the versions in [default: table]
            --check=CHECK    boolean tp conduct an additional check [default: True]

          Description:
            version 
                Prints out the version number
            version pip
                Prints the contents of pip list
                
          Limitations:
            Package names must not have a . in them instead you need to use -
            Thus to query for cloudmesh.cmd5 use
            
              cms version pip cloudmesh-cmd5
           
        """

        # print (arguments)
        # print (">", args, "<")

        if arguments["pip"]:
            # noinspection PyBroadException
            try:
                package = arguments["PACKAGE"]

                if package is None:
                    result = Shell.execute('pip', ['list', '--format=columns'],
                                           traceflag=False, witherror=False)
                    print(result)
                else:
                    if "." in package:
                        package = package.replace(".", "-")
                    result = Shell.execute('pip', ['show', package],
                                           traceflag=False, witherror=False)
                    print(result)

            except Exception as e:
                result = 'N/A'
            return ""

        python_version, pip_version = Shell.get_python()

        # noinspection PyBroadException
        try:
            git_hash_version = Shell.execute('git', 'log -1 --format=%h',
                                             traceflag=False, witherror=False)
        except:
            git_hash_version = 'N/A'

        versions = {
            # "cloudmesh_client": {
            #    "name": "cloudmesh_client",
            #    "version": str(cloudmesh_client.__version__)
            # },
            # "cloudmesh_base": {
            #     "name": "cloudmesh_base",
            #     "version": str(cloudmesh_base.__version__)
            # },
            "python": {
                "name": "python",
                "version": str(python_version)
            },
            "pip": {
                "name": "pip",
                "version": str(pip_version)
            },
            "git": {
                "name": "git hash",
                "version": str(git_hash_version)
            }

        }

        # dynamically check all installed cloudmesh packages and versions
        pipcheck = subprocess.Popen(('pip', 'freeze'), stdout=subprocess.PIPE)
        try:
            # python 3 returns byte sequence so the decode is necessary
            output = subprocess.check_output(('grep', "cloudmesh"),
                                             stdin=pipcheck.stdout).decode(
                "utf-8")
            pkglines = output.strip().split("\n")

            for pkgline in pkglines:
                if "==" in pkgline:
                    values = pkgline.split("==")
                    pkg = values[0]
                    version = values[1].strip()
                    versions[pkg] = {
                        "name": pkg,
                        "version": version
                    }
                elif "git" in pkgline:

                    pkgline = pkgline.replace(
                        "-e git+git@github.com:cloudmesh-community/", "")
                    pkgline = pkgline.replace(
                        "-e git+https://github.com/cloudmesh/", "")
                    pkgline = pkgline.replace("egg=", "")

                    version, pkg = pkgline.split("#")

                    versions[pkg] = {
                        "name": pkg,
                        "version": version
                    }
        except subprocess.CalledProcessError as e:
            pass
        pipcheck.wait()

        # installedpkgs = []
        #
        # for a preset set of named packages
        '''
        #pkgs = ['cloudmesh.common', 'cloudmesh.cmd5', 'cloudmesh.comet']
        for package in pkgs:
            # check version from pip
            pipcheck = subprocess.Popen(('pip', 'freeze'), stdout=subprocess.PIPE)
            try:
                output = subprocess.check_output(('grep', package), stdin=pipcheck.stdout)
                version = output.split("==")[1].strip()
                versions[package] = {"name": package,
                                     "version": version
                                     }
            except subprocess.CalledProcessError as e:
                pass
            pipcheck.wait()
        '''

        # __version__ not maintained in package file so this won't work
        '''
            try:
                print ("trying package |%s|" % package)
                try_module = __import__(package)
                print ("added one package into the list...")
                installedpkgs.append(package)
            except ImportError as e:
                print ("error importing |%s|" % package)
                pass

        #print (installedpkgs)
        for package in installedpkgs:
            versions[package] = {package: {"name": package,
                                           "version": str(package.__version__)
                                           }
                                 }
        print (versions)
        '''

        print(Printer.write(versions, output=arguments["--format"],
                            order=["name", "version"],
                            sort_keys="name"))
        if arguments["--check"] in ["True"]:
            Shell.check_python()


# def main():
#    CMShell().cmdloop()

def inheritors(klass):
    subclasses = set()
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses


# noinspection PyBroadException,PyUnusedLocal
def main():
    """cms.

    Usage:
      cms --help
      cms [--echo] [--debug] [--nosplash] [-i] [COMMAND ...]

    Arguments:
      COMMAND                  A command to be executed

    Options:
      --file=SCRIPT  -f  SCRIPT  Executes the script
      -i                 After start keep the shell interactive,
                         otherwise quit [default: False]
      --nosplash    do not show the banner [default: False]
    """

    def manual():
        print(main.__doc__)

    args = sys.argv[1:]

    arguments = {
        '--echo': '--echo' in args,
        '--help': '--help' in args,
        '--debug': '--debug' in args,
        '--nosplash': '--nosplash' in args,
        '-i': '-i' in args}

    echo = arguments["--echo"]
    if arguments['--help']:
        manual()
        sys.exit()

    for a in args:
        if a in arguments:
            args.remove(a)

    arguments['COMMAND'] = [' '.join(args)]

    commands = arguments["COMMAND"]
    # commands = list(arguments["COMMAND"])

    if len(commands) > 0:
        if ".cm" in commands[0]:
            arguments["SCRIPT"] = commands[0]
            commands = commands[1:]
        else:
            arguments["SCRIPT"] = None

        arguments["COMMAND"] = ' '.join(commands)
        if arguments["COMMAND"] == '':
            arguments["COMMAND"] = None

    # noinspection PySimplifyBooleanCheck
    if arguments['COMMAND'] == []:
        arguments['COMMAND'] = None

    splash = not arguments['--nosplash']
    debug = arguments['--debug']
    interactive = arguments['-i']
    script = arguments["SCRIPT"]
    command = arguments["COMMAND"]

    # context = CloudmeshContext(
    #    interactive=interactive,
    #    debug=debug,
    #    echo=echo,
    #    splash=splash)

    cmd = CMShell()

    #    if script is not None:
    #        cmd.do_exec(script)

    try:
        if echo:
            print(cmd.prompt, command)
        if command is not None:
            cmd.precmd(command)
            stop = cmd.onecmd(command)
            cmd.postcmd(stop, command)
    except Exception as e:
        print("ERROR: executing command '{0}'".format(command))
        print(70 * "=")
        print(e)
        d = Default()
        trace = d["global", "trace"] == "True"
        trace = True
        Error.traceback(error=e, debug=True, trace=trace)
        d.close()
        print(70 * "=")

    if interactive or (command is None and script is None):
        cmd.cmdloop()


if __name__ == '__main__':
    main()
