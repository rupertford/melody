'''A demonstration of how to search some gromacs options. We will use
jinja2 to set input values, Longbow to run gromacs and some text
processing to extract the required results. However, we do not yet do
so.'''

from melody.inputs import Switch, Choice, IntRange, FloatRange, Subsets
from melody.main import Melody
from melody.search import BruteForce
from launch import launch

INPUTS = [ Choice(name="tcoupl", inputs=["Berendsen", "Nose-Hoover"]),
           FloatRange(name="rcoulomb", low=1.1, high=1.6, step=0.1)]

MELODY = Melody(inputs=INPUTS, function=launch, method=BruteForce)
MELODY.search()
