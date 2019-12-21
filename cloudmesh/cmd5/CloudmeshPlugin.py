import sys
import inspect
from cloudmesh.common.util import readfile

class CloudmeshPlugin:

    @staticmethod
    def inheritors(klass):
        """
        returns the inheritors of a class if it is loaded

        :return: a set of classes
        """
        subclasses = set()
        work = [klass]
        while work:
            parent = work.pop()
            for child in parent.__subclasses__():
                if child not in subclasses:
                    subclasses.add(child)
                    work.append(child)
        return subclasses

    @staticmethod
    def find_PluginCommands_in_sys():

        modules = sys.modules.keys()
        plugins = []
        for module in modules:
            if module.startswith("cloudmesh."):
                try:

                    _class = __import__(module)

                    print("check", module, _class)

                    filename = inspect.getfile(_class)
                    content = readfile(filename)
                    if "PluginCommand" in content and "cloudmesh.shell.command" in content:
                        entry = {
                            "module": module,
                            "filename": filename
                        }
                        plugins.append(entry)
                except Exception as e:
                    print (e)
                    pass

        return plugins
