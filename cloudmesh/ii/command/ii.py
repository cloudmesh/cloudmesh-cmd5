from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command
from cloudmesh.var.command.var import VarCommand
import cloudmesh

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
        from cloudmesh.cmd5.CloudmeshPlugin import  CloudmeshPlugin
        print (CloudmeshPlugin.inheritors(PluginCommand))

        import inspect

        import cloudmesh
        print (dir(cloudmesh))

        def find_classes_in_namespace(namespace):
            classes = []
            for name, obj in inspect.getmembers(namespace):
                if inspect.isclass(obj):
                    classes.append(obj)
            return classes


        all_classes = find_classes_in_namespace(cloudmesh.common)
        print(all_classes)

        print ("ho")

