from __future__ import print_function

import shelve

from cloudmesh.common.util import path_expand


class Variables(object):
    def __init__(self, filename=None):
        if filename is None:
            self.filename = path_expand("~/.cloudmesh/var-data")

        self.data = shelve.open(self.filename, writeback=True)
        self.data.sync()

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
        self.data.sync()

    def __delitem__(self, key):
        del self.data[key]
        self.data.sync()

    def __contains__(self, item):
        return item in self.data

    def __str__(self):
        return (str(self.data))

    def __len__(self):
        return len(self.data)

    def __add__(self, directory):
        for key in directory:
            self.data[key] = directory[key]

    def __sub__(self, keys):
        for key in keys:
            del self.data[key]

    def close(self):
        self.data.close()


if __name__ == "__main__":
    v = Variables()
    print(v)

    v["gregor"] = "gregor"
    assert "gregor" in v
    del v["gregor"]
    assert "gregor" not in v
