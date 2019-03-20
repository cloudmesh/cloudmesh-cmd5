import yaml
import requests
import os


class PluginManager(object):

    def __init(self):
        self.data = None

    def load(self):
        url = 'https://raw.githubusercontent.com/cloudmesh/cloudmesh.cmd5/install/plugins.yml'
        r = requests.get(url)
        self.data = yaml.load(r.text)
        for key in self.data['plugins']:
            entry = self.data['plugins'][key]
            entry['description'] = entry['description'].strip()

    def uninstall(self, name):
        plugin = "cloudmesh." + name
        print("Uninstalling:", )
        os.system("pip uninstall {name}".format(name=plugin))

    def pip_install(self, name):
        plugin = "cloudmesh." + name
        print("Installing:", )
        os.system("pip install {name}".format(name=plugin))

    def source_install(self, name):
        pass
