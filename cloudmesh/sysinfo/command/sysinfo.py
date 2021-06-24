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
                sysinfo [-v] [-t]

            Description:
                prints information about the system

        """  # noqa: W605

        if arguments["-t"]:
            info = systeminfo()
            p = 1
            t = info["cpu_threads"]
            c = info["cpu_cores"]
            n = 1

            print(f"(Nodes, Processors, Cores, Threads) = ({n}, {p}, {c}, {t})")
        elif arguments["-v"]:
            info = systeminfo()
            p = 1
            t = info["cpu_threads"]
            c = info["cpu_cores"]
            n = 1

            print(f"(Nodes, Processors, Cores, Threads) = ({n}, {p}, {int(c/p)}, {int(t/(c*p))})")

        else:
            print (Printer.attribute(systeminfo()))

