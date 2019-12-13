from __future__ import print_function

import textwrap

from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command
from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import writefile


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


    def _man_rst(self, data):
        result = [
            data['name'],
            "=" * len(data['name']),
            "",
            textwrap.dedent(data['help']) \
              .replace("::\n\n", ".. parsed-literal::\n\n") \
              .strip(),
            ""]
        return ("\n".join(result))

    def _man_txt(self, data):
        result = [
            "=" * 79,
            data['name'],
            "=" * 79,
            "",
            textwrap.dedent(data['help'].replace("::\n\n", "")).strip(),
            ""
        ]
        return ("\n".join(result))

    def _man_md(self, data):
        result = [
            "# " + data['name'],
            "",
            "```",
            textwrap.dedent(data['help'].replace("::\n\n", "")).strip(),
            "```",
            ""
        ]
        return ("\n".join(result))

    def _man_content(self, data, kind):
        result = ""
        if kind == "md":
            result = self._man_md(data)
        elif kind == "txt":
            result = self._man_txt(data)
        elif kind == "rst":
            result = self._man_rst(data)
        else:
            tmp = [
            data["name"],
            "=" * len(data["name"]),
            data["help"].replace("::\n\n", "", 1)
            ]
            result = "\n".join(tmp)

        return result

    def _print(self, data, kind):
        print (self._man_content(data, kind))

    # noinspection PyUnusedLocal
    @command
    def do_man(self, arg, arguments):
        """
        ::

            Usage:
                   man COMMAND [--format=FORMAT]
                   man [--format=FORMAT] [--noheader]
                   man --dir=DIR [COMMANDS...] [--format=FORMAT]

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

        cmds_doc = []
        cmds_undoc = []
        help_page = {}

        def get_manual_pages():

            names = self.get_names()

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


        arguments.kind = arguments["--format"] or "md"
        print(arguments)
        if arguments["--dir"]:
            d = arguments["--dir"]
            if len(arguments.COMMANDS) == 0:
                get_manual_pages()
            else:
                names = arguments.COMMANDS
            print (d, cmds_doc)

            Shell.mkdir(d)

            for entry in cmds_doc:
                print (f"Printing Manual page for {entry}")
                data = self._get_help(entry)
                content = self._man_content(data, arguments.kind)
                writefile(f"{d}/{entry}.{arguments.kind}", content)

        elif arguments.COMMAND is None:

            get_manual_pages()

            for entry in cmds_doc:
                data = self._get_help(entry)
                self._print(data, arguments["--format"])

            # self.stdout.write("%s\n" % str(self.doc_leader))
            # self.print_topics(self.doc_header, cmds_doc, 15, 80)
            # self.print_topics(self.misc_header, list(help_page.keys()), 15, 80)
            # self.print_topics(self.undoc_header, cmds_undoc, 15, 80)

        else:

            entry = arguments.COMMAND
            data = self._get_help(entry)
            self._print(data, arguments["--format"])
