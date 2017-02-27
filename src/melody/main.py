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
'''melody is a simple generic tuning library primarily designed for
the optimisation of software on hpc architectures'''


class Melody(object):
    ''' The main class '''

    def __init__(self, function=None, method=None, state=None, inputs=None):
        self._function = function
        self._method = method
        self._state = state
        self._inputs = inputs

    @property
    def function(self):
        '''Return the function associated with this instance of melody'''
        return self._function

    @function.setter
    def function(self, function):
        '''Set the function associated with this instance of melody'''
        self._function = function

    @property
    def method(self):
        '''Return the optimisation/search method associated with this instance
        of melody'''
        return self._method

    @method.setter
    def method(self, method):
        '''Set the optimisation/search method associated with this instance of
melody'''
        self._method = method

    @property
    def inputs(self):
        '''Return the input search parameters for the associated function'''
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        '''Set the input search parameters for the associated function'''
        self._inputs = inputs

    def search(self):
        '''Start the optimisation/search using the supplied optimisation
        method with the supplied inputs for the supplied function'''
        search = self._method(inputs=self._inputs, function=self._function,
                              state=self._state)
        search.run()
