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
'''pytest tests for the SearchMethod class in the search.py melody file'''

import pytest
from melody.search import SearchMethod


def test_searchmethod_vanilla():
    '''check that initial required values are stored appropriately if they
    are provided when the class is initialised and that optional
    values are set to None'''
    inputs = "green"
    function = "hello"
    search_method = SearchMethod(inputs=inputs, function=function)
    assert search_method.inputs is inputs
    assert search_method.function is function
    assert search_method.state is None


def test_searchmethod_init_state():
    '''check that state is stored appropriately if it is
    provided when the class is initialised'''
    function = "hello"
    inputs = "green"
    state = "envy"
    search_method = SearchMethod(inputs=inputs, function=function, state=state)
    assert search_method.inputs is inputs
    assert search_method.function is function
    assert search_method.state is state


def test_searchmethod_set_state():
    '''check that state is stored appropriately if it is set '''
    inputs = "green"
    function = "hello"
    state = "envy"
    search_method = SearchMethod(inputs, function)
    search_method.state = state
    assert search_method.inputs is inputs
    assert search_method.function is function
    assert search_method.state is state


def test_searchmethod_run_method():
    '''check that a notimplemented exception is raised if the run method
    is called'''
    inputs = "green"
    function = "hello"
    search_method = SearchMethod(inputs, function)
    with pytest.raises(NotImplementedError) as excinfo:
        search_method.run()
    assert "Run method should be implemented" in str(excinfo.value)
