.. _function:

Function
========

Melody functions are user-written Python functions that perform the
action that the user would like to be optimised and/or
investigated. Melody is not aware of what this action is, it simply
calls the Melody function with a set of inputs and collects the
result(s).

If, for example, you wanted to find the time taken to perform a google
search for different keywords you would use the Melody inputs to
specify the keywords themselves and create a Melody function to take a
particular keyword as input, perform and time the google search for
that keyword and then return the time taken for that particular
search.

API
+++

A user-written Melody function must contain a single input
argument. Melody will call the function with particular input values
from the inputs specified by the user and will expect results to be
provided when the function completes.

The input argument is a Python list containing one or more dictionaries,
each containing a key/value pair. The number of dictionary entries
will correspond to the number of input objects specified by the
user. Each dictionary will contain the name of the input as the key
and one of its specified input options as the value.

Results are returned as two arguments. The first argument is a boolean
value indicating whether the function was successful or not. For
example, the a code might not compile, or the results might be
incorrect. In this case ``False`` should be returned.

The second argument returns the results that the user would like to be
optimised and/or evaluated for the function. For example, this might
be the time a code took to run. The format of the second argument
should be a dictionary of key/value pairs, but the format is not
currently enforced.
::
   
   def function(input):
       return success, result

Example
+++++++

A simple example should help explain the API described in the previous
section.
::

   >>> from melody.inputs import Switch
   >>> inputs = [Switch(name="option1", off="dark", on="light")]
   >>> def function(input):
           print "function {0}".format(str(input))
	   return True, {"value": 10}
   >>> from melody.search import BruteForce
   >>> from melody.main import Melody
   >>> melody = Melody(inputs=inputs, function=function,
                       method=BruteForce)
   >>> melody.search()
   function [{'option1': 'dark'}]
   [{'option1': 'dark'}] True {'value': 10}
   function [{'option1': 'light'}]
   [{'option1': 'light'}] True {'value': 10}

In the above example we have a single input object which can take two
values (either ``"dark"`` or ``"light"``. We use the BruteForce method
(see Section :ref:`method-brute-force`) so the user-written function
will be called twice, once for each value. As the function prints out
the input values it can be seen that it is called twice and that the
input is a list containing a single dictionary (as there is only one
input object) and that dictionary contains a single key, the name
given to the input object (``"option1"``) and a value which is one of
the options provided in the input object (either ``"dark"`` or
``"light"``). The function then returns ``True`` as it is always
successful and a dictionary containing a key/value pair with a fixed
value (``10``) that (in a useful function) would be used to indicate
how the function performed. By default melody prints out the
particular inputs passed to the function and the results provided by
the function. These values can also be seen in the output from the
example.

More examples of user-written Melody functions can be found in the
Melody examples directory.

Support
+++++++

As explained earlier it is up to the user to write a Melody
function. A typical function might

1) Take the input values for the function call and write those into
   appropriate input files e.g. a make include file
2) Compile a code using appropriate input files (e.g. a Makefile)
3) Check that the code compiled OK. If not return False.
4) Run a code based on appropriate input files (e.g. Gromacs config files)
5) Check that the code ran OK and gives valid answers. If not return False
6) Extract performance information from the run.
7) Return from the function call specifying success (True) for the job
   and providing the performance information itself (e.g. time taken).

For example:
::

   def function(input):
       ''' user written function '''
       # use input to set compiler flag in Makefile
       # build the code with the Makefile
       # check it built OK. If not return False
       # run the code
       # check it ran OK. If not return False
       # extract the timing results
       return success, time

As many user-written Melody functions are likely to follow a similar
path to the one described above it is expected that a set of utility
routines can be built up to support the process.

At this point one utility is provided. This utility is useful when
setting up configuration files from the input data supplied to the
function.

The utility takes the inputs to the function (or another equivalent
data-structure created by the user) and matches any keys in the
data-structure with keys within a template (using jinja2) replacing
any matching key with its corresponding value.

.. autofunction:: melody.inputs.create_input

For example
::

   > cat template.txt
   Hello {{name}}.
   > python
   >>> from melody.inputs import create_input
   >>> input = [{"name": "fred"}]
   >>> result = create_input(input, "template.txt",
                             template_location=".")
   >>> print result
   Hello fred.

Examples of the ``create_input`` function being used in Melody functions
can be found in the Melody examples directory.
