###############################################################
# pytest -v --capture=no tests/test_cms.py
# pytest -v  tests/test_cms.py
# pytest -v --capture=no  tests/test_cms.py:Test_cms.<METHIDNAME>
###############################################################
import pytest
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import HEADING


@pytest.mark.incremental
class TestConfig:

    def test_help(self):
        HEADING()

        result = Shell.execute("cms help", shell=True)

        VERBOSE(result)

        assert "quit" in result
        assert "clear" in result

    def test_invalid_command(self):
        HEADING()

        result = Shell.execute("cms help wrong", shell=True)

        VERBOSE(result)

        assert "No help on wrong" in result
