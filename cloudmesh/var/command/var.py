import os
from datetime import datetime

from cloudmesh.common.Shell import Shell
from cloudmesh.common.console import Console
from cloudmesh.common.variables import Variables
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command
from cloudmesh.common.base import Base
from cloudmesh.common.console import Console


class VarCommand(PluginCommand):
    # noinspection PyUnusedLocal

    @command
    def do_var(self, args, arguments):
        """
        ::

            Usage:
                var list
                var clear
                var delete NAME
                var NAME=VALUE
                var NAME
                var

            Arguments:
                NAME      the name of the variable
                VALUE     the value of the variable
                FILENAME  the filename of the variable

            Description:
                Manage persistent variables

                var NAME=VALUE
                   sets the variable with the name to the value
                   if the value is one of data, time, now it will be
                   replaced with the value at this time, the format will be
                    date    2017-04-14
                    time    11:30:33
                    now     2017-04-14 11:30:41
                It will wbe replaced accordingly

                The value can also refer to another variable name.
                In this case the current value will be copied in the named
                variable. As we use the $ sign it is important to distinguish
                shell variables from cms variables while using proper quoting.

                Examples include:

                   cms var a=\$b
                   cms var 'a=$b'
                   cms var a=val.b

                The previous command copy the value from b to a. The val command
                was added to avoid quoting.


        """  # noqa: W605

        if arguments["NAME=VALUE"] == "base":
            print("base")
            base = Base()

            try:
                if os.path.exists(base.path):
                    Console.ok(".cloudmesh directory", base.path)
                else:
                    Console.warning(f"{base.path} does not exist use `cms help` to create it")
            except:
                Console.warning("could not find cloudmesh base.path")

            try:
                if os.path.exists(base.file):
                    Console.ok(f"cloudmesh.yaml is at {base.file}")
                else:
                    Console.warning(f"{base.file} does not exist use `cms help` to create it")
            except:
                Console.warning("could not find cloudmesh base.file")

            if base.key in os.environ:
                Console.ok(f"{base.key}={os.environ[base.key]}")
            else:
                Console.warning(f"{base.key} is not set, ignoring and using other values")

            try:
                vars = f"{base.path}/variables.dat"
                if os.path.exists(vars):
                    Console.ok(f"variables.dat found at {vars}")
                else:
                    Console.warning("variables.dat not found")
            except:
                Console.warning("variables.dat not found")

            return ""

        if args == '':
            arguments["list"] = True

        variables = Variables()

        if arguments["NAME=VALUE"]:
            if '=' in arguments["NAME=VALUE"]:
                name, value = arguments["NAME=VALUE"].split("=", 1)

                if name in ['debug', 'trace', 'timer']:
                    value = str(str(value).lower() in ['1', 'on', 'true'])

            else:
                name = arguments["NAME=VALUE"]
                try:
                    value = variables[name]
                except:
                    value = None

        if arguments["clear"]:
            variables.clear()

        elif arguments["list"]:
            for name in variables:
                value = variables[name]
                print(name, "=", "'", value, "'", sep="")

        elif arguments.delete:
            del variables[arguments.NAME]

        elif name and not value:
            Console.error("variable {name} does not exist".format(name=name))

        elif name and not value:
            print(variables[arguments.NAME])

        elif name and value:
            if name in ["dryrun"]:
                if value.lower() in ["on", "true", "1", "t"]:
                    value = True
                elif value.lower() in ["off", "false", "0", "f"]:
                    value = True
                else:
                    Console.error(f"value of {name} must be True/False")
                    return ""
            elif value.startswith("cloudmesh."):
                try:
                    from cloudmesh.configuration.Config import Config
                    config = Config()
                except:
                    Console.error("cloudmesh configuration not loaded.")
                try:
                    value = config[value]
                except:
                    Console.error(f"problem reading {value}")
                    return ""
            elif value.startswith("!"):
                # cms set a=\!pwd
                command = value[1:]
                value = Shell.run(command)
            elif value.startswith("py "):
                # cms set a=\!pwd
                command = value.split("py ")[1]
                value = eval(command)

            elif value == "time":
                value = datetime.now().strftime("%H:%M:%S")
            elif value == "date":
                value = datetime.now().strftime("%Y-%m-%d")
            elif value == "now":
                value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elif value.startswith("value."):
                var = value.replace("value.", "")
                value = variables[var]
            elif value.startswith("$"):
                var = value.replace("$", "")
                value = variables[var]

            print(name, "=", "'", value, "'", sep="")
            variables[name] = value
