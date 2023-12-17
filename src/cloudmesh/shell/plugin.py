import yaml
import requests
import os


class PluginManager(object):

    def __init(self):
        self.data = None

    def load(self):
        """
        TODO: DEPRECATED:

        loads the plugins form the plugin.yml file in github

        :return:
        """
        url = 'https://raw.githubusercontent.com/cloudmesh/cloudmesh-cmd5/install/plugins.yml'
        r = requests.get(url)
        self.data = yaml.load(r.text)
        for key in self.data['plugins']:
            entry = self.data['plugins'][key]
            entry['description'] = entry['description'].strip()

    def uninstall(self, name):
        """
        pip uninstalls the package with the specified name
        :param name: The package name
        :return:
        """
        plugin = "cloudmesh." + name
        print("Uninstalling:", )
        os.system("pip uninstall {name}".format(name=plugin))

    def pip_install(self, name):
        """
        pip installs the package with the specified name
        :param name: The package name
        :return:
        """
        plugin = "cloudmesh." + name
        print("Installing:", )
        os.system("pip install {name}".format(name=plugin))

    def source_install(self, name):
        """
        TODO: DEPRECATED

        :param name:
        :return:
        """
        pass
