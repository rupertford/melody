# BSD 3-Clause License
#
# Copyright (c) 2017, Science and Technology Facilities Council
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

from melody.inputs import Choice, Subsets
from melody.search import BruteForce
from melody.main import Melody
from parse import parse
from psyGen import PSyFactory


def test_function(options, my_psy):
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
                from transformations import GOceanLoopFuseTrans
                trans = GOceanLoopFuseTrans()
                for loops in values:
                    _, _ = trans.apply(loops[0], loops[1])
            my_invoke.view()
    exit(1)
    return True, [42]


class ArrayBounds(Choice):
    '''A specialisation of the melody Choice input class providing
    array-bound-specific choices for the GOcean 1.0 api.'''
    def __init__(self):
        Choice.__init__(self, name="Array Bounds",
                        options=["", "Specified", "Constant"])


class ModuleInline(Subsets):
    '''A specialisation of the melody Subsets input class providing all
    possible combinations of module inlining for the particular code.'''

    def __init__(self, psy):
        self._psy = psy
        # get the kernels that can be inlined from PSyclone
        kernels = []
        kernel_names = []
        for invoke in self._psy.invokes.invoke_list:
            for kernel in invoke.schedule.kern_calls():
                if kernel.name not in kernel_names:
                    kernel_names.append(kernel.name)
                    kernels.append(kernel)
        Subsets.__init__(self, name="Module inline", inputs=kernels)


class GOLoopFuse(object):
    '''A GOcean-specific melody input class providing all possible
    combinations of loop fusion for the particular code.'''

    def _recurse(self, siblings, my_index, options, all_options, invoke):
        from transformations import GOceanLoopFuseTrans, TransformationError
        my_options = list(options)
        trans = GOceanLoopFuseTrans()
        # siblings includes this loop
        n_siblings = len(siblings)
        index = my_index+1
        while index < n_siblings:
            try:
                trans._validate(siblings[index-1], siblings[index])
                my_options.append([siblings[index-1], siblings[index]])
                #print "Fusion for {0} possible".format(my_options)
                if my_options:
                    all_options.append({invoke: list(my_options)})
                self._recurse(siblings, index+1, my_options, all_options,
                              invoke)
            except TransformationError:
                break
            index += 1

    def __init__(self, dependent_invokes=False):
        # tell melody that I expect state data (psy) to be passed
        self.state = True
        self._name = "Loop Fusion"
        self._dependent_invokes = dependent_invokes

    def options(self, my_psy):
        '''Returns all potential loop fusion options for the psy object
        provided'''
        # compute options dynamically here as they may depend on previous
        # changes to the psy tree
        my_options = []
        invokes = my_psy.invokes.invoke_list
        #print "there are {0} invokes".format(len(invokes))
        if self._dependent_invokes:
            raise RuntimeError(
                "dependent invokes assumes fusion in one invoke might "
                "affect fusion in another invoke. This is not yet "
                "implemented")
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
                        self._recurse(siblings, my_index, option, my_options,
                                      invoke)

        return my_options

    @property
    def name(self):
        '''Returns the name of the melody input class'''
        return self._name

FILE = ("shallow/shallow_alg.f90")
_, INVOKE_INFO = parse(FILE, api="gocean1.0")
PSY = PSyFactory("gocean1.0").create(INVOKE_INFO)

# TBD   ArrayBounds(),
INPUTS = [
    GOLoopFuse(),
    ModuleInline(PSY),
    Choice(name="Problem Size", inputs=["64", "128", "256", "512", "1024"])]

MELODY = Melody(inputs=INPUTS, function=test_function, state=PSY,
                method=BruteForce)
MELODY.search()
