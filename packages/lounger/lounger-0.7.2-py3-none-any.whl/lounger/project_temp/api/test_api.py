# test_api.py
from typing import Dict

from lounger.analyze_cases import load_teststeps
from lounger.case import execute_teststeps


@load_teststeps()
def test_api(teststeps: Dict) -> None:
    """
    Execute the 'teststeps' test case in YAML.
    """
    execute_teststeps(teststeps)
