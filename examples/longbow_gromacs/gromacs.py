'''A demonstration of how to search some gromacs options. We will use
jinja2 to set input values, Longbow to run gromacs and some text
processing to extract the required results. However, we do not yet do
so.'''

from melody.inputs import Switch, Choice, IntRange, FloatRange, Subsets
from melody.main import Melody
from melody.search import BruteForce


def test_function(option):
    '''A dummy test function. The function takes a list of inputs as an
    argument and returns whether the execution was successful (in our
    case we always return True) followed by the target output (in our
    case we simply copy the inputs to the outputs'''
    print option
    return True, option

INPUTS = [ Choice(name="tcoupl", inputs=["Berendsen", "Nose-Hoover"]),
           FloatRange(name="rcoulomb", low=1.1, high=1.6, step=0.1)]

MELODY = Melody(inputs=INPUTS, function=test_function, method=BruteForce)
MELODY.search()
