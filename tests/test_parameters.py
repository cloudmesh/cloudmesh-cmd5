###############################################################
# pytest -v --capture=no tests/test_parameters.py
# pytest -v  tests/test_parameters.py
# pytest -v --capture=no -v --nocapture tests/test_parameters.py::TestCmd5Parameters.test_001
###############################################################
import pytest
from cloudmesh.common.util import HEADING
from cloudmesh.shell.command import map_parameters


@pytest.mark.incremental
class TestCmd5Parameters(object):

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

        for argument in ['clear',
                         'copy',
                         'fromkeys',
                         'get',
                         'items',
                         'keys',
                         'pop',
                         'popitem',
                         'setdefault',
                         'update',
                         'values',
                         'format',
                         'type']:
            arguments = {
                argument: True,
            }
            print(arguments)
            try:
                map_parameters(arguments, argument)
                assert False
            except Exception as e:
                print(e)
                assert True

    def test_map(self):
        HEADING()

        arguments = {
            "--test": "hello"
        }
        map_parameters(arguments, 'test')
        print(arguments)
