import textwrap

from cloudmesh.common.Shell import Shell
from cloudmesh.common.console import Console
from cloudmesh.common.util import readfile
from cloudmesh.common.util import writefile
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command


class ManCommand(PluginCommand):
    # noinspection PyUnusedLocal

    def _convert_file(self, file=None, command=None, include=None, tag="MANPAGE"):
        file = file or "README.md"
        tag_string = f"<!--{tag}-->"
        try:
            if command is not None:
                man = Shell.run(f"cms help {command}")
            elif include is not None:
                man = readfile(include)
            else:
                man = "No command or file specified"

            # remove timer
            if "\n# Timer: " in man:
                man = man.split("\n# Timer: ")[0]

            readme = readfile(file)

            parts = readme.split(tag_string)

            content = []

            content.append(parts[0].strip())
            content.append("")
            content.append(tag_string)
            if command is not None:
                content.append("```")
                content.append(textwrap.dedent("\n".join(man.splitlines()[7:])))
                content.append("```")
            else:
                content.append(textwrap.dedent("\n".join(man.splitlines())))

            content.append(tag_string)
            try:
                content.append(parts[2])
            except:
                pass
        except Exception as e:
            print(e)
            content.append("")
            content.append(tag_string)
            content.append("```")
            content.append(e)
            content.append("```")

            content.append(tag_string)

        manpage = "\n".join(content).strip()

        return manpage, man

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
            textwrap.dedent(data['help']).replace("::\n\n", ".. parsed-literal::\n\n").strip(),
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
                man readme [-p] --toc [--file=FILE]
                man readme [-p] [--tag=TAG] [--file=FILE] --include=INCLUDE
                man readme [-p] [--tag=TAG] [--file=FILE] --command=COMMAND
                man [--dir=DIR] [--format=FORMAT] [--noheader]
                man COMMANDS... [--dir=DIR] [--format=FORMAT]

            Options:
                --toc        adds a table of content between the TOC tag
                -p           replacement in the file instead of stdout
                --noheader   no rst header
                --tag=TAG    the tag used to embed the manual
                             page [default: MANUAL]
                --file=FILE  the file for the replacement between the
                             tags [default: README.md]

            Arguments:
                COMMANDS   the command manual pages to be printed

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
        arguments.directory = arguments["--dir"]
        arguments.file = arguments["--file"] or "README.md"
        arguments.tag = arguments["--tag"] or "MANUAL"

        get_manual_pages()

        if arguments["--dir"]:
            d = arguments["--dir"]
            Shell.mkdir(d)

        if arguments["readme"] and arguments["--toc"]:

            in_place = arguments["-p"]
            if in_place:
                man = Shell.run(f"md_toc -p github {arguments.file}")
                print(man)
            else:
                man = Shell.run(f"md_toc github {arguments.file}")
                print(man)

        elif arguments["readme"] and arguments["--include"]:

            in_place = arguments["-p"]

            manpage, old = self._convert_file(file=arguments.file,
                                              include=arguments["--include"],
                                              tag=arguments.tag)
            if in_place and manpage != old:
                writefile(arguments.file, manpage)
            else:
                print(manpage)

        elif arguments["readme"] and arguments["--command"]:

            in_place = arguments["-p"]

            manpage, old = self._convert_file(file=arguments.file,
                                              command=arguments["--command"],
                                              tag=arguments.tag)
            if in_place and manpage != old:
                writefile(arguments.file, manpage)
            else:
                print(manpage)

        elif arguments["readme"]:

            in_place = arguments["-p"]

            manpage, old = self._convert_file(arguments.file,
                                              arguments.COMMAND,
                                              arguments.tag)
            if in_place and manpage != old:
                writefile(arguments.file, manpage)
            else:
                print(manpage)

        elif len(arguments.COMMANDS) == 0:

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
                    Console.error(f"Cloud not find man page for {entry}")

        return ""
