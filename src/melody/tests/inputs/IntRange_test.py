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
'''pytest tests for the IntRange class in the inputs.py melody file'''

import pytest
from melody.inputs import IntRange

@pytest.mark.xfail(reason="bug : (low, high, step)==None causes TypeError")
def test_intrange_class_vanilla():
    '''check that initial values are set appropriately if they are not
    provided'''
    int_range = IntRange()
    assert len(int_range.options) == 0
    assert int_range.name == None

def test_intrange_class_value_inputs():
    '''check that the IntRange class returns the specified inputs'''
    low = 0
    high = 10
    step = 1
    expected = [i for i in range(low, high, step)]
    int_range = IntRange(low=low, high=high, step=step)
    assert len(int_range.options) == len(expected)
    for idx, value in enumerate(expected):
        assert int_range.options[idx] == expected[idx]

@pytest.mark.xfail(reason="bug : (low, high, step)==None causes TypeError")
def test_intrange_class_name():
    '''check that the IntRange class returns the specified name'''
    test_name = "daughter"
    int_range = IntRange(name=test_name)
    assert int_range.name == test_name
