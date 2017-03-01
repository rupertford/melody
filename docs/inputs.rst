
Inputs
======

Melody inputs allow the user to specify the space that they would like
to search. Inputs are specified as a list of individual input objects.

Supported
+++++++++

The following input classes are currently supported.

Fixed
*****

.. autoclass:: melody.inputs.Fixed
    :members:

For example
::

   >>> from melody.inputs import Fixed
   >>> inputs = [Fixed(name="option1", value="value1")]

The above example will generate an input named ``option1`` with the value
``value1``.

Switch
******

.. autoclass:: melody.inputs.Switch
    :members:

For example
::
   
   >>> from melody.inputs import Switch
   >>> inputs = [Switch(name="option1", off="dark", on="light")]

The above example will generate an input named ``option1`` with two
values, ``dark`` and ``light``. If one of the arguments ``off`` or
``on`` is not provided then an empty string is returned for that
option. If both of the arguments ``off`` and ``on`` are not provided
then a ``Runtime`` exception is raised.

Choice
******

.. autoclass:: melody.inputs.Choice
    :members:

For example
::
   
   >>> from melody.inputs import Choice
   >>> inputs = [Choice(name="input2", inputs=["a", "b", "c"])]

The above example will generate an input named ``input2`` with three
values, ``a``, ``b`` and ``c``. The list can be arbitrarily long.

IntRange
********

.. autoclass:: melody.inputs.IntRange
    :members:

For example
::
   
   >>> from melody.inputs import IntRange
   >>> inputs = [IntRange(name="range1", low=0, high=3, step=1)]

The above example will generate an input named ``range1`` with three
integer values, ``0``, ``1`` and ``2``.

.. warning::

   You might expect the integer 3 to appear, however consistency is
   being maintained with the Python range function which will not
   return this value.

IntRange
********

.. autoclass:: melody.inputs.FloatRange
    :members:

For example
::
   
   >>> from melody.inputs import FloatRange
   >>> inputs = [FloatRange(name="range2", low=0.0, high=0.4, step=0.1)]


The above example will generate an input named ``range2`` with four
floating point values, ``0.0``, ``0.1``, ``0.2`` and ``0.3``.

.. warning::

   You might expect the value 0.4 to appear, however consistency is
   being maintained with the Python range function which will not
   return this value.

Subsets
*******

.. autoclass:: melody.inputs.Subsets
    :members:

For example
::
   
   >>> from melody.inputs import Subsets
   >>> inputs = [Subsets(name="combinations", inputs=["a", "b", "c"])]


The above example will generate an input named ``combinations`` with 8
combinations of values ``[]``, ``["a"]``, ``["b"]``, ``["c"]``,
``["a", "b"]``, ``["a", "c"]``, ``["b", "c"]`` and ``["a", "b", "c"]``.

This option is useful when you have a set of inputs that are optional
and can be used with eachother in any combination.


Multiple input objects
++++++++++++++++++++++

So far each of the suported input options has been presented
individually. You might naturally be wondering why inputs has been
defined as a list of input objects.

The reason for this is that an arbitrary number of input objects can
be included in the inputs list. The implication of doing this is that
all combinations of options are potentially valid inputs.

If we combine two of the earlier examples into one ...
::

   >>> from melody.inputs import Fixed, Choice
   >>> inputs = [FloatRange(name="range2", low=0.0, high=0.4, step=0.1),
                 Choice(name="input2", inputs=["a", "b", "c"])]

we will be specifying the following valid combinations for ``range2``
and ``input2``: ``0.0, "a"``, ``0.0, "b"``, ``0.0, "c"``, ``0.1,
"a"``, ``0.1, "b"``, ``0.1, "c"``, ``0.2, "a"``, ``0.2, "b"``, ``0.2,
"c"``, ``0.3, "a"``, ``0.3, "b"`` and ``0.3, "c"``.

.. note::

   The last input object specified in the list iterates fastest,
   followed by the penultimate one etc. So, in the above example the
   values for ``input2`` are changing more rapidly than the values for
   ``range2``.

Extending
+++++++++

If the supported input classes do not cover your requirements then you
can create your own input classes. All of the input classes inherit
from the Input base class.

.. autoclass:: melody.inputs.Input
    :members:

You can subclass the input class. For example, if you wanted to
provide all values greater than a tolerance as inputs from a list of values:
::
   
   >>> from melody.inputs import Input
   >>> class IntTolerance(Input):
           ''' returns values if they are greater than a tolerance '''
           def __init__(self, name, inputs, tolerance):
               options = []
	       for value in inputs:
	           if value>tolerance:
	               options.append(value)
           Input.__init__(self, name, options)
   >>> inputs = [IntTolerance("tolerance", [8, 9, 2, 4, 10], 7)]


Alternatively you can subclass one of the supporting input types if
that is simpler. For example, if you wanted to append a string to all
Switch values:
::

   >>> from melody.inputs import Switch
   >>> class SwitchAppend(Switch):
           ''' append a string to all switch values '''
           def __init__(self, name, off, on, append):
               Switch.__init__(self, name, off+append, on+append)
   >>> inputs = [SwitchAppend("switch", "a", "b", "_value")]


If you do create your own subclass and you think it might be a
useful addition we ask that you consider contributing your code so
that it can be incorporated into Melody for others to use.
