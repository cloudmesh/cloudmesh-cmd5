###############################################################
# pytest -v --capture=no tests/test_variables.py
# pytest -v  tests/test_variables.py
# pytest -v --capture=no  tests/test_variables.py::TestVariables::<METHODNAME>
###############################################################
import pytest
from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import HEADING
from cloudmesh.common.util import path_expand
from cloudmesh.common.variables import Variables


def _run(command):
    print()
    print("Command:", command)
    result = Shell.run(command)
    print("Result:", result)
    return result


@pytest.mark.incremental
class TestVariables(object):

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
        HEADING()
        r = _run("cms var deleteme=abc")
        print(r)

        data = path_expand("~/.cloudmesh/variables.dat")
        cat = _run(f"cat {data}")
        print(cat)
        assert "deleteme: abc" in cat

        v = Variables()
        print("Data", v.__dict__["data"].__dict__)

        value = v['deleteme']
        print("Value:", value)

        assert value == 'abc'

    def test_cli_get(self):
        HEADING()
        r = _run("cms var deleteme")
        v = Variables()
        print(r)
        assert v['deleteme'] == 'abc'

    def test_cli_list(self):
        HEADING()
        r = _run("cms var list")
        v = Variables()
        print(r)
        assert v['deleteme'] == 'abc'
        assert "deleteme='abc'" in r

    def test_cli_delete(self):
        HEADING()
        r = _run("cms var delete deleteme")
        v = Variables()
        print("Result:", r)
        print("Variable:", v)

        assert v['deleteme'] != 'abc'
