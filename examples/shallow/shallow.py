'''A first example showing how to initialise and run melody. The
different input types are shown, along with a dummy test function,
using a brute force search'''

from melody.inputs import Fixed, Switch, Choice
from melody.search import BruteForce
from melody.main import Melody
from execute import execute

# inputs taken from https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html
INPUTS = [
    Fixed(name="F90", value="gfortran"),
    Choice(name="F90FLAGS", inputs=["", "-O", "-O1", "-O2", "-O3", "-Ofast"]),
    Switch(name="Inline limit", on="-inline-limit=1000000"),
    Switch(name="Stores Out Of Loops", on="-fgcse-sm"),
    Switch(name="Remove Redundant Loads", on="-fgcse-las"),
    Switch(name="Loop Nests", on="-floop-nest-optimize"),
    Choice(name="Vector Cost Model", pre="-fvect-cost-model=",
           inputs=["unlimited", "dynamic", "cheap"]),
    Switch(name="Maths Optimisations", on="-funsafe-math-optimizations"),
    Switch(name="No Nans and infs", on="-ffinite-math-only"),
    Switch(name="No user traps", on="-fno-trapping-math"),
    Switch(name="No signed zeros", on="-fno-signed-zeros"),
    Switch(name="Always unroll", on="-funroll-all-loops"),
    Choice(name="Problem Size", inputs=["64", "128", "256", "512", "1024"])]

MELODY = Melody(inputs=INPUTS, function=execute, method=BruteForce)
MELODY.search()
