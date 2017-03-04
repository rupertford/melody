
Installation
============

Downloading
+++++++++++

First download the source from github. You can download a zip file ...
::

   $ wget https://github.com/rupertford/melody/archive/master.zip
   $ unzip master.zip

or clone the repository ...
::
 
   $ git clone https://github.com/rupertford/melody.git

Python version
++++++++++++++

Melody is currently tested on Python 2.7.

Installation
++++++++++++

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

If you would like to uninstall melody (after installing using the setup.py
script) you can do so using pip. You may see a number of error messages but
the installation should complete successfully.
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
