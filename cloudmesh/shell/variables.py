from __future__ import print_function

from ruamel import yaml
import os
import os.path

from cloudmesh.common.util import path_expand


class VarDB(object):
    """A replacement for :mod:`shelve` that should work for Python 2 and 3.

    This uses a YAML file as the underlying persistent storage

    Assumption
    ==========

    Values are strings so there is no need to pickle/unpickle objects.
    """

    def __init__(self, path):
        self._db = dict()

        self.path = path

        prefix = os.path.dirname(self.path)
        if not os.path.exists(prefix):
            os.makedirs(prefix)

        if os.path.exists(self.path):
            with open(self.path) as dbfile:
                self._db = yaml.safe_load(dbfile) or dict()

        self.flush()

    def flush(self):
        with open(self.path, 'w') as dbfile:
            yaml.dump(self._db, dbfile, default_flow_style=False)

    def __setitem__(self, k, v):
        assert isinstance(v, str) or isinstance(v, unicode), repr(v)
        # the assertion should short-circuit, supporting Py2 and Py3
        self._db[k] = v
        self.flush()

    def __getitem__(self, k):
        return self._db[k]

    def __delitem__(self, k):
        del self._db[k]
        self.flush()

    def __contains__(self, k):
        return k in self._db

    def __iter__(self):
        return iter(self._db)

    def __len__(self):
        return len(self._db)

    def close(self):
        "This is a NoOP for backwards compatibility"
        pass

    def clear(self):
        "Truncate the database"
        self._db.clear()
        self.flush()


class Variables(object):
    def __init__(self, filename=None):
        self.filename = path_expand(filename or "~/.cloudmesh/var-data")
        self.data = VarDB(self.filename)

    def __getitem__(self, key):
        if key not in self.data:
            return None
        else:
            return self.data[key]

    def __setitem__(self, key, value):
        print ("set", key, value)
        self.data[str(key)] = value

    def __delitem__(self, key):
        del self.data[str(key)]

    def __contains__(self, item):
        return str(item) in self.data

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

    def __iter__(self):
        return iter(self.data)

    def close(self):
        self.data.close()

    def clear(self):
        self.data.clear()


if __name__ == "__main__":
    v = Variables()
    print(v)

    v["gregor"] = "gregor"
    assert "gregor" in v
    del v["gregor"]
    assert "gregor" not in v
