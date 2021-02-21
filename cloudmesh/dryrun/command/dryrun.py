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
                dryrun

            Description:

                dryrun on

                    Sets the variable

                    dryrun=True

                dryrun off

                    Sets the variable

                    dryrun=False

                dryrun

                    Returns the value of dryrun
        """

        variables = Variables()

        if arguments.on:
            variables["dryrun"] = True

        elif arguments.off:
            variables["dryrun"] = False

        else:
            print("dryrun =", variables["dryrun"])
