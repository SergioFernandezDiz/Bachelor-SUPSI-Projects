# Group_06_Bernacchia_Fernandez\client> pipenv run pytest tests/

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../task_manager_library')))
print(sys.path)