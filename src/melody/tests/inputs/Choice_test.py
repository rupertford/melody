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
'''pytest tests for the Name class in the inputs.py melody file'''

import pytest
from melody.inputs import Choice


@pytest.mark.xfail(reason="bug : inputs==None causes TypeError")
def test_choice_class_vanilla():
    '''check that initial values are set appropriately if they are not
    provided'''
    choice = Choice()
    assert len(choice.options) == 0
    assert choice.name is None


def test_choice_class_value_inputs():
    '''check that the Choice class returns the specified inputs'''
    test_values = ["test1", "test2", "test3"]
    choice = Choice(inputs=test_values)
    assert len(choice.options) == len(test_values)
    for idx, _ in enumerate(test_values):
        assert choice.options[idx] == test_values[idx]


def test_choice_class_value_pre():
    '''check that the Choice class returns the specified inputs modified
    by the pre value if it is provided'''
    test_values = ["test1", "test2", "test3"]
    pre_value = "pre_"
    choice = Choice(pre=pre_value, inputs=test_values)
    assert len(choice.options) == len(test_values)
    for idx, _ in enumerate(test_values):
        assert choice.options[idx] == pre_value+test_values[idx]


@pytest.mark.xfail(reason="bug : inputs==None causes TypeError")
def test_choice_class_name():
    '''check that the choice class returns the specified name'''
    test_name = "wife"
    choice = Choice(name=test_name)
    assert choice.name == test_name
