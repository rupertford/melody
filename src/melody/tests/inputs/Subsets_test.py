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
'''pytest tests for the Subsets class in the inputs.py melody file'''

import pytest
from melody.inputs import Subsets

@pytest.mark.xfail(reason="bug : inputs==None causes TypeError")
def test_subsets_class_vanilla():
    '''check that initial values are set appropriately if they are not
    provided'''
    subsets = Subsets()
    assert len(subsets.options) == 0
    assert subsets.name == None

def test_subsets_class_value_inputs():
    '''check that the Subsets class returns the expected inputs'''
    test_values = ["a", "b", "c"]
    expected_values = [[], ["a"], ["b"], ["c"], ["a", "b"],
                       ["a", "c"], ["b", "c"], ["a", "b", "c"]]
    subsets = Subsets(inputs=test_values)
    assert len(subsets.options) == len(expected_values)
    for value in expected_values:
        assert value in subsets.options

@pytest.mark.xfail(reason="bug : inputs==None causes TypeError")
def test_subsets_class_name():
    '''check that the subsets class returns the specified name'''
    test_name = "dad"
    subsets = Subsets(name=test_name)
    assert subsets.name == test_name
