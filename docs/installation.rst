
Installation
============

Python version
++++++++++++++

Melody is currently tested with Python 2.7.

Using pip
+++++++++

You can install and uninstall using pip.
::

   $ sudo pip install melody
   $ sudo pip uninstall melody

If you don't have admin rights you can install and uninstall locally.
::
   
   $ pip install melody --user
   $ pip uninstall melody

.. note ::

   In some systems the resultant installation directory for a local
   install is not automatically added to the PYTHONPATH so must be
   done manually. The installation path will be
   ``${HOME}/.local/lib/pythonx.y/site-packages`` where ``x.y`` is the
   version of Python being used.

Downloading and installing
++++++++++++++++++++++++++

We recommend using pip for installation but if you would prefer to
download and install locally then follow the instructions in this
section.

Latest release
**************

First download the source from github. You can download a zip file ...
::

   $ wget https://github.com/rupertford/melody/archive/0.1.1.zip
   $ unzip 0.1.1.zip

or clone the repository and switch to the latest release ...
::
 
   $ git clone https://github.com/rupertford/melody.git
   $ git checkout tags/0.1.1

Latest stable version
*********************

First download the source from github. You can download a zip file ...
::

   $ wget https://github.com/rupertford/melody/archive/master.zip
   $ unzip master.zip

or clone the repository and switch to the latest release ...
::
 
   $ git clone https://github.com/rupertford/melody.git

Installation
************

Using setup.py
--------------

Melody includes an installation setup file called setup.py in its top level
directory.
::

   $ cd <melody_dir>
   $ python setup.py install

If you do not have appropriate permissions you can perform a local
installation instead
::

   $ cd <melody_dir>
   $ python setup.py install --user

.. note ::

   In some systems the resultant installation directory is not
   automatically added to the PYTHONPATH so must be done manually. The
   installation path will be
   ``${HOME}/.local/lib/pythonx.y/site-packages`` where ``x.y`` is the
   version of Python being used.
   
If you would like to uninstall melody (after installing using the setup.py
script) you can do so using pip. You may see a number of error messages but
the removal should complete successfully.
::

   $ pip uninstall melody

Local pip install
-----------------

This installation relies on you not moving or modifying the downloaded
source code. In the top level directory type:
::
   
   $ cd <melody_dir>
   $ pip install -e .

Manual setup
------------

This solution also relies on you not moving or modifying the
downloaded source code. In this case you simply set your python path
appropriately.
::
   
   $ export PYTHONPATH=<melody_dir>/src
   

Testing
+++++++

If you have successfully installed melody then you should be able to import it from Python.
::
   
   $ python
   >>> import melody
   >>>

There is also a test suite, written to use pytest, that can be used to
test the installation. Note, the tests are not included in the pip
installation procedure. If you do not have pytest you can install it
using ``pip install pytest``.
::

   $ py.test
   ============================= test session starts ==============================
   platform linux2 -- Python 2.7.12, pytest-2.8.7, py-1.4.31, pluggy-0.3.1
   rootdir: /xxx/melody, inifile: 
   plugins: cov-2.4.0
   collected 33 items 
   
   src/melody/tests/inputs/choice_test.py ..
   src/melody/tests/inputs/create_input_test.py ....
   src/melody/tests/inputs/fixed_test.py .
   src/melody/tests/inputs/floatrange_test.py .
   src/melody/tests/inputs/input_test.py ..
   src/melody/tests/inputs/intrange_test.py .
   src/melody/tests/inputs/subsets_test.py .
   src/melody/tests/inputs/switch_test.py ....
   src/melody/tests/main/melody_test.py ....
   src/melody/tests/search/bruteforce_test.py .x..
   src/melody/tests/search/searchmethod_test.py .........
   
   ===================== 32 passed, 1 xfailed in 0.25 seconds =====================
   
