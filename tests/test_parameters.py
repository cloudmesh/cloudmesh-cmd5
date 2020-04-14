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
from cloudmesh.shell.command import map_parameters

@pytest.mark.incremental
class Test_cmd5_parameters(object):

    def test_variables_overwrite(self):
        HEADING()

        arguments = {
            "list": True,
            "--list": "hello"
        }
        try:
            map_parameters(arguments, 'list')
            assert False
        except:
            assert True
            print(arguments)


    def test_variables_predefined(self):
        HEADING()

        for argument in ['clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop',
                   'popitem', 'setdefault', 'update', 'values', 'format',
                   'type']:
            arguments = {
                argument: True,
            }
            print (arguments)
            try:
                map_parameters(arguments, argument)
                assert False
            except Exception as e:
                print (e)
                assert True

    def test_map(self):
        HEADING()

        arguments = {
            "--test": "hello"
        }
        map_parameters(arguments, 'test')
        print (arguments)

