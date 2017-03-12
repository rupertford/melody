.. _method:

Method
======

Melody methods determine how the search/optimisation space is going to
be traversed. In the first instance melody is being used to search the
optimisation space rather than optimise over it.

Methods
+++++++

Melody currently only supports a single method called ``BruteForce``.

.. _method-brute-force:

BruteForce
**********

The BruteForce method iterates over all possible combinations
specified in the inputs irrespective of the return values. Thus it is
a parameter search method rather than an optimisation method. It has
proven useful to investigate relatively small optimisation-space
landscapes if they are not known. For example, the performance of a
code for a set of input parameters.

For example, if we specify three input objects, the associated
function will be called for all combinations of their values.
::

   >>> from melody.inputs import Fixed, Switch, IntRange
   >>> inputs = [Fixed(name="opt1", value="grey"),
                 Switch(name="opt2", off="dark", on="light"),
		 IntRange("opt3", low=1, high=3, step=1)]
   >>> def function(input):
           print "function {0}".format(str(input))
	   return True, {"value": 10}
   >>> from melody.search import BruteForce
   >>> from melody.main import Melody
   >>> melody = Melody(inputs=inputs, function=function,
                       method=BruteForce)
   >>> melody.search()
   function [{'opt1': 'grey'}, {'opt2': 'dark'}, {'opt3': 1}]
   [{'opt1': 'grey'}, {'opt2': 'dark'}, {'opt3': 1}] True {'value': 10}
   function [{'opt1': 'grey'}, {'opt2': 'dark'}, {'opt3': 2}]
   [{'opt1': 'grey'}, {'opt2': 'dark'}, {'opt3': 2}] True {'value': 10}
   function [{'opt1': 'grey'}, {'opt2': 'light'}, {'opt3': 1}]
   [{'opt1': 'grey'}, {'opt2': 'light'}, {'opt3': 1}] True {'value': 10}
   function [{'opt1': 'grey'}, {'opt2': 'light'}, {'opt3': 2}]
   [{'opt1': 'grey'}, {'opt2': 'light'}, {'opt3': 2}] True {'value': 10}

In the above example, the first input object has 1 option, the second
2 options and the third 2 options. Therefore for a brute force
combination one would expect to have 1*2*2 combinations in total
equaling 4. As you can see, 4 options are output.

   
Extending
+++++++++

The user can create new Melody methods if they so wish. All methods
should inherit from the ``SearchMethod`` base class.

.. note::

   Please ignore the state argument and method in the ``SearchMethod``
   class. These are not used at the moment and are placeholders for
   future developments.

.. autoclass:: melody.search.SearchMethod
    :members:

The user can subclass the ``SearchMethod`` base class. The ``run``
method must be implemented as this is called by the ``Melody`` class
(see the :ref:`melody` section). The ``run`` method should take all of
the supplied ``inputs`` and call the function appropriately.

In the example below an illustrative ``PrintInputs`` class is created
which simply prints out the input objects supplied (it does not call
the function)
::

   >>> from melody.inputs import Fixed, Switch, IntRange
   >>> inputs = [Fixed(name="option1", value="grey"),
                 Switch(name="option2", off="dark", on="light"),
                 IntRange("option3", low=1, high=3, step=1)]
   >>> def function(input):
           return True, {"value": 10}
   >>> from melody.search import SearchMethod
   >>> class PrintInputs(SearchMethod):
           ''' example searchmethod subclass '''
           def __init__(self, inputs, function, state=None):
               SearchMethod.__init__(self, inputs, function, state)
           def run(self):
	       ''' example run method '''
               for input in inputs:
                   print input
   >>> from melody.main import Melody
   >>> melody = Melody(inputs=inputs, function=function,
                       method=PrintInputs)
   >>> melody.search()
   <melody.inputs.Fixed object at 0x7f7c1136a490>
   <melody.inputs.Switch object at 0x7f7c1136a650>
   <melody.inputs.IntRange object at 0x7f7c1136a990>
