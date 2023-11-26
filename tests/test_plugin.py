###############################################################
# pytest -v --capture=no tests/test_plugin.py
# pytest -v  tests/test_plugin.py
# pytest -v --capture=no  tests/test_plugin..py::Test_plugin::<METHODNAME>
###############################################################
import pytest
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.Shell import Shell
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING

from cloudmesh.shell.shell import Plugin

@pytest.mark.incremental
class TestConfig:

    def test_plugin(self):
        HEADING()
        Benchmark.Start()

        plugin = Plugin()
        l = plugin.list()
        print (l)

        Benchmark.Stop()

    def test_modules(self):
        HEADING()
        Benchmark.Start()

        plugin = Plugin()
        m = plugin.modules()
        print(m)

        Benchmark.Stop()

    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, sysinfo=False, tag="cmd5")
