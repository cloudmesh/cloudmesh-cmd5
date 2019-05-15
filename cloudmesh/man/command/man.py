from __future__ import print_function

from cloudmesh.common.Printer import Printer
from cloudmesh.common.console import Console
from cloudmesh.common.default import Default

import textwrap

from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command

from pprint import pprint


class ManCommand(PluginCommand):
    # noinspection PyUnusedLocal

    def _get_help(self, what):
        """
        prints the rst page of the command what
        :param what: the command
        :type what: string
        """
        h = None
        data = {"name": what}
        h = eval("self.do_{what}.__doc__".format(what=what))
        # noinspection PyUnboundLocalVariable
        data["help"] = h
        return data

    def _print_rst(self, data):
        print(data['name'])
        print("=" * len(data['name']))
        print()
        print(textwrap.dedent(data['help']).strip())
        print()

    def _print_txt(self, data):
        print("=" * 79)
        print(data['name'])
        print("=" * 79)
        print()
        print(textwrap.dedent(data['help'].replace("::\n\n", "")).strip())
        print()

    def _print_md(self, data):
        print("# " + data['name'])
        print()
        print("```")
        print(textwrap.dedent(data['help'].replace("::\n\n", "")).strip())
        print("```")
        print()

    def _print(self, data, kind):
        if kind == "md":
            self._print_md(data)
        elif kind == "txt":
            self._print_txt(data)
        elif kind == "rst":
            self._print_rst(data)

    # noinspection PyUnusedLocal
    @command
    def do_man(self, arg, arguments):
        """
        ::

            Usage:
                   man [--kind=FORMAT] COMMAND
                   man [--kind=FORMAT] [--noheader]

            Options:
                   --noheader  no rst header

            Arguments:
                   COMMAND   the command to be printed

            Description:
                man
                    Prints out the help pages
                man COMMAND
                    Prints out the help page for a specific command
        """
        arguments.kind = arguments["--kind"]

        if arguments.COMMAND is None:

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

            for entry in cmds_doc:
                data = self._get_help(entry)
                self._print(data, arguments.kind)

            # self.stdout.write("%s\n" % str(self.doc_leader))
            # self.print_topics(self.doc_header, cmds_doc, 15, 80)
            # self.print_topics(self.misc_header, list(help_page.keys()), 15, 80)
            # self.print_topics(self.undoc_header, cmds_undoc, 15, 80)

        else:

            entry = arguments.COMMAND
            data = self._get_help(entry)
            self._print(data, arguments.kind)
