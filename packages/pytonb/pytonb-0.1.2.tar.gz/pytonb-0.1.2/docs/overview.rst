Overview
========
   

Welcome to the ``pytonb`` documentation. This project is a
minimal example of a utility that converts jupyter notebooks to python filey and vice versa. 

The input/output marks added to python files when converting are taken into consideratin when creating separate cells when backconverting. The utility can also sync a notebook or notebook folder to a .py file(s). Reverse syncing is not supported.

Getting Started
---------------

Install the package::

   pip install pytonb


Key Functions
-------------

* :mod:`write_script` — convert notebook to python script
* :mod:`write_notebook` — convert script to notebook
* :mod:`sync` — sync a notebook with the corresponding .py file
* :mod:`sync_folder`- sync a folder with notebooks with the corresponding .py files


Use the :doc:`api` reference for full details of the available Python APIs.
