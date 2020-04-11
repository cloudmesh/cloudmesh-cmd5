from cloudmesh.common.variables import Variables
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command


class DebugCommand(PluginCommand):
    # noinspection PyUnusedLocal

    @command
    def do_dryrun(self, args, arguments):
        """
        ::

            Usage:
                dryrun on
                dryrun off

            Description:

                dryrun on

                    sets the variable

                    dryrun=True

                dryrun off

                    sets the variable

                    dryrun=False

        """

        variables = Variables()

        if arguments.on:
            variables["dryrun"] = True

        elif arguments.off:
            variables["dryrun"] = False
