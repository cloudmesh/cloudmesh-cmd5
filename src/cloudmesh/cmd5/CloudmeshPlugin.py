import sys
import inspect
from cloudmesh.common.util import readfile


class CloudmeshPlugin:
    """A utility class for working with Cloudmesh plugins.

    This class provides static methods for discovering inheritors of a class
    and finding Cloudmesh plugin commands in the loaded modules.

    Methods:
        inheritors(klass):
            Returns the inheritors of a class if it is loaded.

        find_PluginCommands_in_sys():
            Finds Cloudmesh PluginCommands in the loaded modules.
    """

    @staticmethod
    def inheritors(klass):
        """Returns the inheritors of a class if it is loaded.

        Args:
            klass (class): The class to find inheritors for.

        Returns:
            set: A set of classes that inherit from the specified class.
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
        """Finds Cloudmesh PluginCommands in the loaded modules.

        This method searches through the loaded modules and identifies
        modules that start with "cloudmesh." and contain both "PluginCommand"
        and "cloudmesh.shell.command" in their content.

        Returns:
            list: A list of dictionaries containing module information.
        """

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
                    print(e)
                    pass

        return plugins
