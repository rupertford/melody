# BSD 3-Clause License
#
# Copyright (c) 2017, Science and Technology Failities Council
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author R. Ford STFC Daresbury Lab.
#
'''An example showing how to optimise PSyclone algorithms from
melody. The specific example will be the shallow benchmark but we do
not interface to it yet.'''

from melody.inputs import Switch, Choice, IntRange, FloatRange, Subsets
from melody.search import BruteForce
from melody.main import Melody


def test_function(options, psy):
    '''A dummy test function. The function takes a list of inputs as an
    argument and returns whether the execution was successful (in our
    case we always return True) followed by the target output (in our
    case we simply copy the inputs to the outputs'''

    for option in options:
        name = option.keys()[0]
        values = option[name]
        if name == "Module inline":
            print "skipping module inline"
        elif name == "Problem Size":
            print "skipping problem size"
        elif name == "Loop Fusion":
            print "Performing requested loop fusion ..."
            for invoke in values:
                print "fusion for invoke '{0}'".format(invoke.name)
                print dir(my_psy.invokes)
                my_invoke = my_psy.invokes.invoke_map[invoke.name]
                print my_invoke.name
                from transformations import GOceanLoopFuseTrans, TransformationError
                for loops in values:
                    psy, _ = trans.apply(loops[0], loops[1])
            my_invoke.view()
    exit(1)
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

    def __init__(self, dependent_invokes=False):
        self.state = True # tell melody that I expect state data (psy) to be passed
        self._name = "Loop Fusion"
        self._dependent_invokes = dependent_invokes

    def options(self, psy):
        ''' '''
        # compute options dynamically here as they may depend on previous changes to the psy tree
        my_options = []
        invokes = psy.invokes.invoke_list
        #print "there are {0} invokes".format(len(invokes))
        if self._dependent_invokes:
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
                        self._recurse(siblings, my_index, option, my_options, invoke)

        return my_options

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
    GOLoopFuse(),
    ModuleInline(psy=psy),
    Choice(name="Problem Size", inputs=["64", "128", "256", "512", "1024"])]

MELODY = Melody(inputs=INPUTS, function=test_function, state=psy, method=BruteForce)
MELODY.search()
