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

    def __init__(self, inputs, function, state=None):
        self._inputs = inputs
        self._check_inputs()
        self._function = function
        self._check_function()
        self._state = state

    def _check_inputs(self):
        ''' make some basic checks on the inputs to make sure they are valid'''
        try:
            _ = self._inputs[0]
        except TypeError:
            raise RuntimeError(
                "inputs should be iterable but found type='{0}', value="
                "'{1}'".format(type(self._inputs), str(self._inputs)))
        from melody.inputs import Input
        for check_input in self._inputs:
            if not isinstance(check_input, Input):
                raise RuntimeError(
                    "input should be a subclass of the Input class but "
                    "found type='{0}', value='{1}'".format(type(check_input),
                                                           str(check_input)))

    def _check_function(self):
        ''' make some basic checks on the function to make sure it is valid'''
        # note, callable is valid for Python 2 and Python 3.2 onwards but
        # not inbetween
        if not callable(self._function):
            raise RuntimeError(
                "provided function '{0}' is not callable".
                format(str(self._function)))
        from inspect import getargspec
        arg_info = getargspec(self._function)
        if len(arg_info.args) != 1:
            print str(arg_info)
            raise RuntimeError(
                "provided function should have one argument but found "
                "{0}".format(len(arg_info.args)))
        # I don't think I can statically determine how many arguments
        # a function will return so will have to check after calling
        # the function

    def run(self):
        '''Ensure that any subclass implements this method'''
        raise NotImplementedError("Run method should be implemented")

    @property
    def function(self):
        '''Return the function associated with this instance of search
        method'''
        return self._function

    @property
    def inputs(self):
        '''Return the input search parameters for this instance of search
        method'''
        return self._inputs

    @property
    def state(self):
        '''Return the state for this instance of search method'''
        return self._state

    @state.setter
    def state(self, state):
        '''Set the state for this instance of search method'''
        self._state = state


class BruteForce(SearchMethod):
    '''A search method that tests all input options'''

    def __init__(self, inputs, function, state=None):
        SearchMethod.__init__(self, inputs, function, state=state)

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
            try:
                valid, result = self._function(output)
            except ValueError:
                raise RuntimeError("function must return 2 values")
            print output, valid, result
