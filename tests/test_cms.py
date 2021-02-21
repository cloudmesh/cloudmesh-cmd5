###############################################################
# pytest -v --capture=no tests/test_cms.py
# pytest -v  tests/test_cms.py
# pytest -v --capture=no  tests/test_cms..py::Test_cms::<METHODNAME>
###############################################################
import pytest
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.Shell import Shell
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING


@pytest.mark.incremental
class TestConfig:

    def test_help(self):
        HEADING()
        Benchmark.Start()
        result = Shell.execute("cms help", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "quit" in result
        assert "clear" in result

    def test_invalid_command(self):
        HEADING()
        Benchmark.Start()
        result = Shell.execute("cms help wrong", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "No help on wrong" in result

    def test_version(self):
        HEADING()
        Benchmark.Start()
        result = Shell.execute("cms version", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        # assert "No help on wrong" in result

    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, sysinfo=False, tag="cmd5")
