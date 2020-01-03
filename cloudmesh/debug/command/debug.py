from datetime import datetime

from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command
from cloudmesh.common.variables import Variables
from cloudmesh.common.console import Console


class DebugCommand(PluginCommand):
    # noinspection PyUnusedLocal

    @command
    def do_debug(self, args, arguments):
        """
        ::

            Usage:
                debug on
                debug off


            Description:

                debug on

                    sets the variables

                    debug=True
                    trace=True
                    verbose=10
                    timer=True

                debug off

                    sets the variables

                    debug=False
                    trace=False
                    verbose=0
                    timer=False


        """

        database = Variables(filename="~/.cloudmesh/var-data")

        if arguments.on:
            database["debug"] = True
            database["trace"] = True
            database["verbose"] = '10'
            database["timer"] = True

        elif arguments.off:
            database["debug"] = False
            database["trace"] = False
            database["verbose"] = '0'
            database["timer"] = False
