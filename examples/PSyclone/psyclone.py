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

    #mi_name = "Module inline"
    #for option in options:
    #    if option.keys()[0] == mi_name:
    #        print "{'"+mi_name+"': [",
    #        for item in option[mi_name]:
    #            print "'"+item.name+"'",
    #        print "]",
    #    else:
    #        print option,
    #print
    return True, [42]


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

    def _recurse(self, siblings, my_index, options, all_options, invoke):
        from transformations import GOceanLoopFuseTrans, TransformationError
        my_options = list(options)
        trans = GOceanLoopFuseTrans()
        # siblings includes this loop
        n_siblings = len(siblings)
        index = my_index+1
        while index<n_siblings:
            try:
                trans._validate(siblings[index-1], siblings[index])
                my_options.append([siblings[index-1], siblings[index]])
                #print "Fusion for {0} possible".format(my_options)
                if my_options:
                    all_options.append({invoke:list(my_options)})
                self._recurse(siblings, index+1, my_options, all_options, invoke)
            except TransformationError:
                break
            index += 1

    def __init__(self, psy=None, dependent_invokes=False):
        self._name = "Loop Fusion"
        self._options = []
        self._psy = psy
        invokes = psy.invokes.invoke_list
        #print "there are {0} invokes".format(len(invokes))
        if dependent_invokes:
            print ("dependent invokes assumes fusion in one invoke might affect fusion "
                   "in another invoke. This is not yet implemented")
            exit(1)
        else:
            # treat each invoke separately
            for idx, invoke in enumerate(invokes):
                print "invoke {0}".format(idx)
                # iterate through each outer loop
                for loop in invoke.schedule.loops():
                    if loop.loop_type == "outer":
                        siblings = loop.parent.children
                        my_index = siblings.index(loop)
                        option = []
                        self._recurse(siblings, my_index, option, self._options, invoke)
            #print self._options

    @property
    def options(self):
        ''' '''
        return self._options

    @property
    def name(self):
        ''' '''
        return self._name

#FILE = "/home/rupert/proj/GungHo/PSyclone_trunk/examples/gocean/shallow_alg.f90"
FILE = "/home/rupert/proj/GungHoSVN/PSyclone_trunk/examples/gocean/shallow_alg.f90"
from parse import parse
from psyGen import PSyFactory
_, invoke_info = parse(FILE, api="gocean1.0")
psy = PSyFactory("gocean1.0").create(invoke_info)

# TBD   ArrayBounds(),
INPUTS = [
    GOLoopFuse(psy=psy),
    ModuleInline(psy=psy),
    Choice(name="Problem Size", inputs=["64", "128", "256", "512", "1024"])]

MELODY = Melody(inputs=INPUTS, function=test_function, method=BruteForce)
MELODY.search()
