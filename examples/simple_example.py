'''A first example showing how to initialise and run melody. The
different input types are shown, along with a dummy test function,
using a brute force search'''

from melody.inputs import Switch, Choice, IntRange, FloatRange, Subsets
from melody.search import BruteForce
from melody.main import Melody

def test_function(option):
    '''A dummy test function. The function takes a list of inputs as an
    argument and returns whether the execution was successful (in our
    case we always return True) followed by the target output (in our
    case we simply copy the inputs to the outputs'''
    print option
    return True, option

INPUTS = [
    Switch(name="Debug Flag", off="", on="-g"),
    Choice(name="Opt Flags", inputs=["-O", "-O2", "-O3"]),
    IntRange(name="Segment Size", low=0, high=20, step=10),
    FloatRange(name="Tolerance", low=0.0, high=1.0, step=0.5),
    Subsets(name="Silly", inputs=["-fast", "-great", "-super"])]

MELODY = Melody(inputs=INPUTS, function=test_function, method=BruteForce)
MELODY.search()
