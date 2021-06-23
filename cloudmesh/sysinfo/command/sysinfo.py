from datetime import datetime

from cloudmesh.common.Shell import Shell
from cloudmesh.common.console import Console
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command
from cloudmesh.common.systeminfo import systeminfo
from cloudmesh.common.Printer import Printer

class SysinfoCommand(PluginCommand):
    # noinspection PyUnusedLocal

    @command
    def do_sysinfo(self, args, arguments):
        """
        ::

            Usage:
                sysinfo

            Description:
                prints information about the system

        """  # noqa: W605

        print (Printer.attribute(systeminfo()))

