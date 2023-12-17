from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command

class IiCommand(PluginCommand):
    # noinspection PyUnusedLocal
    @command
    def do_ii(self, args, arguments):
        """
        ::

          Usage:
            ii

        """  # noqa: W605


        print ("ii")
        # from cloudmesh.cmd5.CloudmeshPlugin import  CloudmeshPlugin
        # print (CloudmeshPlugin.inheritors(PluginCommand))
        #
        # print ("ho")
        # import cloudmesh
        # print (dir(cloudmesh))
        #
        # print ("111", PluginCommand.__subclasses__())
        #
        # import inspect
        # import cloudmesh
        # print(inspect.getmembers(PluginCommand, inspect.isclass))
        #
        #
        # for name in cloudmesh.__dict__:
        #     print(name)
        # from pprint import pprint
        # pprint(globals())
        #
        from cloudmesh.shell.shell import CMShell
        #
        # commands = dir(CMShell)
        # commands = [s for s in commands if s.startswith("do_")]
        # commands = [s.replace("do_", "") for s in commands]

        # print (commands)
        import cloudmesh
        print(dir(cloudmesh))
