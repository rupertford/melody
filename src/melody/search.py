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
'''This module provides the internally supported Melody search
methods. A search method is expected to conform to the SearchMethod
base class'''


class SearchMethod(object):
    '''A utility baseclass for different search/optimisation methods'''

    def __init__(self, function=None, inputs=None, state=None):
        self._function = function
        self._inputs = inputs
        self._state = state

    def run(self):
        '''Ensure that any subclass implements this method'''
        raise NotImplementedError("Run method should be implemented")

    @property
    def function(self):
        '''Return the function associated with this instance of search
        method'''
        return self._function

    @function.setter
    def function(self, function):
        '''Set the function associated with this instance of search method'''
        self._function = function

    @property
    def inputs(self):
        '''Return the input search parameters for this instance of search
        method'''
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        '''Set the input search parameters for this instance of search
        method'''
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
        SearchMethod.__init__(self, function=function, inputs=inputs,
                              state=state)

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
                my_output.append({name: option})
                self._recurse(inputs[1:], my_output)
        else:
            valid, result = self._function(output)
            print output, valid, result
