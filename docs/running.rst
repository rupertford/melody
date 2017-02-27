
Running
=======

Melody supports 3 main concepts, `inputs`, a `function` and a `method`.

Melody `inputs` define the search space over which the user would like
to search. A number of pre-existing classes are provided to capture
this space. These can also be written by the user. Section xxx
discusses inputs in more detail.

The user writes the Melody `function` to perform the particular task
that requires analysis. Melody calls this function wth appropriate
inputs and expects to receive two return values once the function has
completed. Section yy discusses writing a Melody `function` in more
detail.

The Melody `method` defines how to search the input space. Currently
there is only one option here, which is brute force. The user may
write their own search/optimisation method if they so choose. Section
zzz discusses Melody methods in more detail.

A `Melody` convenience class binds these three concepts together and
can be used to initiate the search.

Example
+++++++

This section presents a simple Melody example which iterates over all
possible combinations of two types of input, a choice of specified
values and a range of integer values. The user supplied empty function
simply returns two 0's each time it is called.
::

   >>> from melody.inputs import Choice, IntRange
  >>> from melody.search import BruteForce
  >>> from melody.main import Melody
  >>> inputs = [Choice(name="input1", inputs=["a", "b", "c"]),
                IntRange(name="input2", low=1, high=3, step=1)]
  >>> def function(values):
  >>>     return 0, 0
  >>> method = BruteForce
  >>> melody = Melody(inputs=inputs, function=function, method=method)
  >>> melody.search()
  [{'input1': 'a'}, {'input2': 1}] 0 0
  [{'input1': 'a'}, {'input2': 2}] 0 0
  [{'input1': 'b'}, {'input2': 1}] 0 0
  [{'input1': 'b'}, {'input2': 2}] 0 0
  [{'input1': 'c'}, {'input2': 1}] 0 0
  [{'input1': 'c'}, {'input2': 2}] 0 0
  >>> 
