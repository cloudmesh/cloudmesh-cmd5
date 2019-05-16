###############################################################
# pip install .; pytest -v --capture=no -v --nocapture tests/test_configdict.py:Test_configdict.test_001
# pytest -v --capture=no tests/test_configdictr.py
# pytest -v  tests/test_configdict.py
###############################################################
from __future__ import print_function

from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import HEADING

from cloudmesh.common.variables import Variables
import pytest

def run(command):
    print(command)
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    print(result)
    return result


@pytest.mark.incremental
class Test_cmd5(object):

    def test_001(self):
        HEADING("assign key=value")
        v = Variables()
        n = len(v)
        v["gregor"] = "gregor"
        assert (len(v) == n + 1)
        assert "gregor" in v
        v.close()

    def test_002(self):
        HEADING("delete")
        v = Variables()
        del v["gregor"]
        assert "gregor" not in v
        v.close()

    def test_003(self):
        HEADING("directory add ")
        d = {"a": "1", "b": "2"}
        v = Variables()
        v + d
        print(v)
        assert "a" in v and "b" in v
        del v["a"]
        del v["b"]

        v + d
        assert "a" in v and "b" in v
        v - d
        assert "a" not in v and "b" not in v

        print(v)
        v.close()

    def test_004(self):
        HEADING("directory and key subtract ")
        d = {"a": "1", "b": "2"}
        v = Variables()
        v + d
        print(v)
        assert "a" in v and "b" in v
        v - d.keys()
        assert "a" not in v and "b" not in v

        print(v)
        v.close()
