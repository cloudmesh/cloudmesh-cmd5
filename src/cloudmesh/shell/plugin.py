import yaml
import requests
import os


class PluginManager(object):
    """
    This class is deprecated. and dynamic loading is used.

    A class for managing Cloudmesh plugins.

    This class provides methods for loading plugins from a YAML file on GitHub,
    uninstalling, and installing plugins using pip.

    Methods:
        load():
            DEPRECATED: Loads plugins from the 'plugins.yml' file on GitHub.

        uninstall(name):
            Pip uninstalls the package with the specified name.

        pip_install(name):
            Pip installs the package with the specified name.

        source_install(name):
            DEPRECATED: Installs the package with the specified name from source.
    """

    def __init(self):
        """
        Initializes the PluginManager object.
        """
        self.data = None

    def load(self):
        """TODO: DEPRECATED:

        loads the plugins form the plugin.yml file in github

        Returns:

        """
        url = "https://raw.githubusercontent.com/cloudmesh/cloudmesh-cmd5/install/plugins.yml"
        r = requests.get(url)
        self.data = yaml.load(r.text)
        for key in self.data["plugins"]:
            entry = self.data["plugins"][key]
            entry["description"] = entry["description"].strip()

    def uninstall(self, name):
        """
         Pip uninstalls the package with the specified name.

         Args:
             name (str): The package name to uninstall.
         """
        plugin = "cloudmesh." + name
        print(
            "Uninstalling:",
        )
        os.system("pip uninstall {name}".format(name=plugin))

    def pip_install(self, name):
        """
        Pip installs the package with the specified name.

        Args:
            name (str): The package name to install.
        """
        plugin = "cloudmesh." + name
        print(
            "Installing:",
        )
        os.system("pip install {name}".format(name=plugin))

    def source_install(self, name):
        """TODO: DEPRECATED

        Args:
            name

        Returns:

        """
        pass
