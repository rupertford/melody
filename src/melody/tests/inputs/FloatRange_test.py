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
from melody.inputs import FloatRange

@pytest.mark.xfail(reason="bug : (low, high, step)==None causes TypeError")
def test_floatrange_class_vanilla():
    '''check that initial values are set appropriately if they are not
    provided'''
    float_range = FloatRange()
    assert len(float_range.options) == 0
    assert float_range.name == None

def test_floatrange_class_value_inputs():
    '''check that the FloatRange class returns the specified inputs'''
    low = 0.0
    high = 10.0
    step = 1.0
    from numpy import arange
    expected = [i for i in arange(low, high, step)]
    float_range = FloatRange(low=low, high=high, step=step)
    assert len(float_range.options) == len(expected)
    for idx, value in enumerate(expected):
        assert float_range.options[idx] == expected[idx]

@pytest.mark.xfail(reason="bug : (low, high, step)==None causes TypeError")
def test_floatrange_class_name():
    '''check that the FloatRange class returns the specified name'''
    test_name = "son"
    float_range = FloatRange(name=test_name)
    assert float_range.name == test_name
