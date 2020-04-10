from datetime import datetime

from cloudmesh.common.Shell import Shell
from cloudmesh.common.console import Console
from cloudmesh.common.variables import Variables
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command


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

            
        """

        database = Variables(filename="~/.cloudmesh/variables.dat")

        if arguments["NAME=VALUE"]:
            if '=' in arguments["NAME=VALUE"]:
                name, value = arguments["NAME=VALUE"].split("=", 1)

                if name in ['debug', 'trace', 'timer']:
                    value = str(str(value).lower() in ['1', 'on', 'true'])

            else:
                name = arguments["NAME=VALUE"]
                try:
                    value = database[name]
                except:
                    value = None

        if arguments["clear"]:
            database.clear()

        elif arguments["list"]:
            for name in database:
                value = database[name]
                print(name, "=", "'", value, "'", sep="")

        elif arguments.delete:
            del database[arguments.NAME]

        elif name and not value:
            Console.error("variable {name} does not exist".format(name=name))

        elif name and not value:
            print(database[arguments.NAME])

        elif name and value:
            if value.startswith("cloudmesh."):
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
                value = database[var]
            elif value.startswith("$"):
                var = value.replace("$", "")
                value = database[var]

            print(name, "=", "'", value, "'", sep="")
            database[name] = value
