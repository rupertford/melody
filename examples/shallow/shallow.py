'''A first example showing how to initialise and run melody. The
different input types are shown, along with a dummy test function,
using a brute force search'''

from melody.inputs import Fixed, Switch, Choice
from melody.search import BruteForce
from melody.main import Melody
from execute import execute

# inputs taken from https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html
# more flags and info is here ... https://gcc.gnu.org/onlinedocs/gcc-4.5.3/gcc/i386-and-x86_002d64-Options.html
INPUTS = [
    Fixed(name="F90", value="gfortran"),
    Choice(name="F90FLAGS", inputs=["-O2", "-O3", "-Ofast"]),
    Choice(name="native", inputs=["", "-mtune=native", "-march=native"]),
    Switch(name="Inline limit", on="-finline-limit=5000"),
    Fixed(name="Problem Size", value="128")]

# TBD
# *** try different inline-limit values
# -fwhole-program needs to be part of compile and fails as we link timer libraries
#    Switch(name="Single program", on="-fwhole-program"),
# flto needs to be on both compile and link as do all optimisation options

# ignore lower levels of optimisation
#    Choice(name="F90FLAGS", inputs=["", "-O", "-O1", "-O2", "-O3", "-Ofast"]),

# start with one problem size to limit the time
#    Choice(name="Problem Size", inputs=["64", "128", "256"])]

# 512 and 1024 take too long to run
#    Choice(name="Problem Size", inputs=["64", "128", "256", "512", "1024"])]

# unsupported in my version of gfortran
#    Choice(name="Vector Cost Model", pre="-fvect-cost-model=",
#           inputs=["unlimited", "dynamic", "cheap"]),

# ignored for the moment
#    Switch(name="Stores Out Of Loops", on="-fgcse-sm"),
#    Switch(name="Remove Redundant Loads", on="-fgcse-las"),
#    Switch(name="Loop Nests", on="-floop-nest-optimize"),
#    Switch(name="Maths Optimisations", on="-funsafe-math-optimizations"),
#    Switch(name="No Nans and infs", on="-ffinite-math-only"),
#    Switch(name="No user traps", on="-fno-trapping-math"),
#    Switch(name="No signed zeros", on="-fno-signed-zeros"),
#    Switch(name="Always unroll", on="-funroll-all-loops"),

MELODY = Melody(inputs=INPUTS, function=execute, method=BruteForce)
MELODY.search()
