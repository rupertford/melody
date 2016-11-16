'''An example showing how to optimise PSyclone algorithms from
melody. The specific example will be the shallow benchmark but we do
not interface to it yet.'''

from melody.inputs import Switch, Choice, IntRange, FloatRange, Subsets
from melody.search import BruteForce
from melody.main import Melody

def test_function(options):
    '''A dummy test function. The function takes a list of inputs as an
    argument and returns whether the execution was successful (in our
    case we always return True) followed by the target output (in our
    case we simply copy the inputs to the outputs'''

    mi_name = "Module inline"
    for option in options:
        if option.keys()[0] == mi_name:
            print "{'"+mi_name+"': [",
            for item in option[mi_name]:
                print "'"+item.name+"'",
            print "]",
        else:
            print option,
    print
    return True, options


class ArrayBounds(Choice):
    def __init__(self):
        Choice.__init(self, name="Array Bounds",
                      options=["", "Specified", "Constant"])


class ModuleInline(Subsets):
    ''' '''

    def __init__(self, psy=None):
        self._psy = psy
        # get the kernels that can be inlined from PSyclone
        kernels = []
        kernel_names = []
        for invoke in psy.invokes.invoke_list:
            for kernel in invoke.schedule.kern_calls():
                if kernel.name not in kernel_names:
                    kernel_names.append(kernel.name)
                    kernels.append(kernel)
        Subsets.__init__(self, name="Module inline", inputs=kernels)


class GOLoopFuse(object):
    ''' '''

    def __init__(self, psy=None):
        self._name = "Loop Fusion"
        self._psy = psy
        from transformations import GOceanLoopFuseTrans, TransformationError
        trans = GOceanLoopFuseTrans()
        for invoke in psy.invokes.invoke_list:
            print "new invoke ..."
            loops = []
            for loop in invoke.schedule.loops():
                if loop.loop_type == "outer":
                    loops.append(loop)
            for index1 in range(len(loops)):
                for index2 in range(index1+1, len(loops)):
                    try:
                        trans._validate(loops[index1], loops[index2])
                        print "Fusion of {0} {1} possible".format(index1, index2)
                    except TransformationError:
                        break
        exit(1)
        # get the loop fusion input options from PSyclone
        self._options = []

    @property
    def options(self):
        ''' '''
        return self._options

    @property
    def name(self):
        ''' '''
        return self._name

FILE = "/home/rupert/proj/GungHo/PSyclone_trunk/examples/gocean/shallow_alg.f90"
from parse import parse
from psyGen import PSyFactory
_, invoke_info = parse(FILE, api="gocean1.0")
psy = PSyFactory("gocean1.0").create(invoke_info)

# TBD   ArrayBounds(),
# TBD   GOLoopFuse(psy=psy),
INPUTS = [
    ModuleInline(psy=psy),
    Choice(name="Problem Size", inputs=["64", "128", "256", "512", "1024"])]

MELODY = Melody(inputs=INPUTS, function=test_function, method=BruteForce)
MELODY.search()
