from cloudmesh.common.variables import Variables
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command


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
        print(args, arguments)
        self.set_debug(args)
