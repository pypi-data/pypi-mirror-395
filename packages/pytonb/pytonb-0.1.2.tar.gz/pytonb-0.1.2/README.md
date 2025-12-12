[![License](https://img.shields.io/github/license/k4144/pytonb)](https://github.com/k4144/pytonb/blob/main/LICENSE)
[![CI](https://github.com/k4144/pytonb/actions/workflows/project-ci.yml/badge.svg)](https://github.com)
[![Tests](https://github.com/k4144/pytonb/badges/tests.svg)](https://docs.pytest.org/en/stable/)
[![Coverage](https://github.com/k4144/pytonb/badges/coverage.svg)](https://docs.pytest.org/en/stable/)
[![Bandit](https://github.com/k4144/pytonb/badges/bandit.svg)](https://bandit.readthedocs.io/en/latest/)
[![Black](https://github.com/k4144/pytonb/badges/black.svg)](https://pypi.org/project/black/)
[![Docs](https://github.com/k4144/pytonb/badges/docs.svg)](https://www.sphinx-doc.org/en/master/usage/quickstart.html)
[![Wheel](https://img.shields.io/pypi/wheel/pytonb)](https://pypi.org/project/pytonb/)
![Status](https://img.shields.io/badge/status-beta-blue)
![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)


## simple converter for pa files vs notebooks
### example:
```
from pytonb import write_notebook, write_script
write_notebook('filename.py')
```
### writes notebook filename.ipynb. optional parameters:
* save_name, notebook file name
* use_ast, ignore notebook markers (In[ ]:), create a separate cell for each function
```
write_script('filename.ipynb')
```
### writes filename.py, including notebook markers (In[ ]:). optional parameters:
* save_name, py file name  
* overwrite, write over existing py file
### example syncing notebook to py file:
```
from pytonb import sync, sync_folder
sync('filename.ipynb')
```
### sync ipynb file to filename.py. optional parameters:
* py_path: py file save path
* delay: delay in s before checking change
### example syncing folder to py files:
```
from pytonb import sync, sync_folder           
sync_folder('folder')
```
### sync ipynb files in folder to corresponding py files.  optional parameters:
* recursion_level: sync ipynb files up to this depth 
* delay: delay in s before checking change

