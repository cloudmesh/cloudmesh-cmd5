###############################################################
# pip install .; pytest -v --capture=no -v --nocapture tests/test_cmd5..py::Test_cmd5.test_001
# pytest -v --capture=no tests/test_cmd5.py
# pytest -v  tests/test_cmd5.py
###############################################################
from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import HEADING

from cloudmesh.common.variables import Variables
import pytest
from cloudmesh.common.run.subprocess import run
from cloudmesh.common.util import path_expand


def run(command):
    print()
    print("Command:", command)
    result = Shell.run(command)
    print("Result:", result)
    return result


@pytest.mark.incremental
class Test_cmd5(object):

    def test_variables_assign(self):
        HEADING("assign key=value")
        v = Variables()
        n = len(v)
        v["gregor"] = "gregor"
        assert (len(v) == n + 1)
        assert "gregor" in v
        v.close()

    def test_variables_delete(self):
        HEADING("delete")
        v = Variables()
        del v["gregor"]
        assert "gregor" not in v
        v.close()

    def test_variables_add(self):
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

    def test_test_variable_remove(self):
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

    def test_cli_set(self):
        r = run("cms var deleteme=abc")
        print(r)


        data = path_expand("~/.cloudmesh/variables.dat")
        cat= run(f"cat {data}")
        print(cat)
        assert "deleteme: abc" in cat

        v = Variables()
        print ("Data", v.__dict__["data"].__dict__)

        value = v['deleteme']
        print ("Value:",  value)

        assert value == 'abc'

    def test_cli_get(self):
        r = run("cms var deleteme")
        v = Variables()
        print(r)
        assert v['deleteme'] == 'abc'

    def test_cli_list(self):
        r = run("cms var list")
        v = Variables()
        print(r)
        assert v['deleteme'] == 'abc'
        assert "deleteme='abc'" in r

    def test_cli_delete(self):
        r = run("cms var delete deleteme")
        v = Variables()
        print("Result:", r)
        print("Variable:", v)

        assert v['deleteme'] != 'abc'

    def test_cli_delete(self):
        r = run("cms var delete deleteme")
        v = Variables()
        print("Result:", r)
        print("Variable:", v)

        assert v['deleteme'] != 'abc'
