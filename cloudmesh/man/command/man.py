import textwrap

from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command
from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import writefile
from pprint import pprint
from cloudmesh.common.console import Console


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

    def _print(self, name, data, kind, directory=None):
        content = self._man_content(data, kind)
        if directory is None:
            print(content)
        else:
            writefile(f"{directory}/{name}.{kind}", content)

    # noinspection PyUnusedLocal
    @command
    def do_man(self, arg, arguments):
        """
        ::

            Usage:
                man [--dir=DIR] [--format=FORMAT] [--noheader]
                man COMMANDS... [--dir=DIR] [--format=FORMAT]

            Options:
                --noheader  no rst header

            Arguments:
                COMMANDS   the command manual pages to be printed

            Description:
                man
                    Prints out the help pages
                man COMMAND
                    Prints out the help page for a specific command
        """

        print(arguments)

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
        arguments.directory = arguments["--dir"]

        get_manual_pages()

        if arguments["--dir"]:
            d = arguments["--dir"]
            Shell.mkdir(d)

        if len(arguments.COMMANDS) == 0:

            for entry in cmds_doc:
                data = self._get_help(entry)
                self._print(entry, data, arguments.kind, arguments.directory)

        else:

            commands = arguments.COMMANDS

            for entry in commands:
                if entry in cmds_doc:

                    data = self._get_help(entry)
                    self._print(entry, data, arguments.kind, arguments.directory)

                else:
                    Console.error(f"Cloud not firn man page for {entry}")



        return ""
