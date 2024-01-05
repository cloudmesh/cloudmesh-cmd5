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

    def test_arguments(self):
        HEADING()
        Benchmark.Start()
        result = Shell.execute("cms banner abc", shell=True)
        Benchmark.Stop()
        VERBOSE(result)
        assert "# abc\n" in result

    def test_arguments(self):
        HEADING()
        Benchmark.Start()
        result = Shell.execute('cms banner "abc --minus"', shell=True)
        Benchmark.Stop()
        VERBOSE(result)
        assert "# abc --minus\n" in result

    def test_script(self):
        HEADING()
        Benchmark.Start()
        result = Shell.execute('cat tests/a.cm | cms', shell=True).strip()
        
        print (result)
        Benchmark.Stop()
        VERBOSE(result)
        assert "# ls -lisa\n" in result
        assert "# a b c\n" in result


    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, sysinfo=False, tag="cmd5")
