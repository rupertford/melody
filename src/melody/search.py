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
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Author R. Ford STFC Daresbury Lab.
#
''' '''


class SearchMethod(object):
    '''A utility baseclass for different search/optimisation methods'''

    def __init__(self, function=None, inputs=None, state=None):
        self._function = function
        self._inputs = inputs
        self._state = None

    @property
    def function(self):
        '''Return the function associated with this instance of search method'''
        return self._function

    @function.setter
    def function(self, function):
        '''Set the function associated with this instance of search method'''
        self._function = function

    @property
    def inputs(self):
        '''Return the input search parameters for this instance of search method'''
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        '''Set the input search parameters for this instance of search method'''
        self._inputs = inputs

    @property
    def state(self):
        '''Return the xxx for this instance of search method'''
        return self._state

    @state.setter
    def state(self, state):
        '''Set the xxx for this instance of search method'''
        self._state = state


class BruteForce(SearchMethod):
    '''A search method that tests all input options'''

    def __init__(self, function=None, inputs=None, state=None):
        SearchMethod.__init__(self, function=function, inputs=inputs, state=state)

    def run(self):
        ''' perform the search over inputs'''
        self._recurse(self.inputs, [])

    def _recurse(self, inputs, output):
        '''internal recursion routine called by the run method that generates
        all input combinations'''
        if inputs:
            my_input = inputs[0]
            name = my_input.name
            if my_input.state:
                my_options = my_input.options(self.state)
            else:
                my_options = my_input.options
            for option in my_options:
                my_output = list(output)
                my_output.append({name:option})
                self._recurse(inputs[1:], my_output)
        else:
            valid, result = self._function(output)
            print output, valid, result


class Switch(object):
    ''' '''

    def __init__(self, name=None, off=None, on=None):
        self._name = name
        self._off = off
        self._on = on
        self._options = [off, on]

    @property
    def options(self):
        ''' '''
        return self._options

    @property
    def name(self):
        ''' '''
        return self._name


class Choice(object):
    ''' '''

    def __init__(self, name=None, inputs=None):
        self._name = name
        self._options = inputs

    @property
    def options(self):
        ''' '''
        return self._options

    @property
    def name(self):
        ''' '''
        return self._name


class Range(object):
    ''' '''

    def __init__(self, name=None, low=None, high=None, step=None, options=None):
        self._name = name
        self._low = low
        self._high = high
        self._step = step
        self._options = options

    @property
    def options(self):
        ''' '''
        return self._options

    @property
    def name(self):
        ''' '''
        return self._name


class IntRange(Range):
    ''' '''

    def __init__(self, name=None, low=None, high=None, step=None):
        options = [i for i in range(low, high, step)]
        Range.__init__(self, name=name, low=low, high=high, step=step,
                       options=options)


class FloatRange(Range):
    ''' '''

    def __init__(self, name=None, low=None, high=None, step=None):
        from numpy import arange
        options = [f for f in arange(low, high, step)]
        Range.__init__(self, name=name, low=low, high=high, step=step,
                       options=options)


class Subsets(object):
    ''' '''

    def __init__(self, name=None, inputs=None):
        self._name = name
        self._inputs = inputs
        self._options = []
        for k in range(len(inputs)+1):
            self._recurse(inputs, [], depth=0, max_depth=k)
        print "Subsets found {0} options".format(len(self._options))

    def _recurse(self, inputs, output, depth, max_depth):
        ''' '''
        if depth<max_depth:
            for index in range(len(inputs)):
                option = inputs[index]
                my_output = list(output)
                my_output.append(option)
                self._recurse(inputs[index+1:], my_output, depth+1, max_depth)
        else:
            self._options.append(output)

    @property
    def options(self):
        ''' '''
        return self._options

    @property
    def name(self):
        ''' '''
        return self._name
