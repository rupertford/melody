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
from melody.inputs import Switch

def test_switch_class_vanilla():
    '''check that initial values are set appropriately if they are not
    provided'''
    switch = Switch()
    assert len(switch.options) == 2
    assert switch.options[0] == ""
    assert switch.options[1] == ""
    assert switch.name == None

def test_switch_class_value_off():
    '''check that the Switch class returns the specified value for off'''
    test_value = "test"
    switch = Switch(off=test_value)
    assert len(switch.options) == 2
    assert switch.options[0] == test_value
    assert switch.options[1] == ""

def test_switch_class_value_on():
    '''check that the Switch class returns the specified value for on'''
    test_value = "test"
    switch = Switch(on=test_value)
    assert len(switch.options) == 2
    assert switch.options[0] == ""
    assert switch.options[1] == test_value

def test_switch_class_value_offon():
    '''check that the Switch class returns the specified values for off and
    on if they are both set'''
    test_off_value = "off"
    test_on_value = "on"
    switch = Switch(off=test_off_value, on=test_on_value)
    assert len(switch.options) == 2
    assert switch.options[0] == test_off_value
    assert switch.options[1] == test_on_value

def test_switch_class_name():
    '''check that the switch class returns the specified name'''
    test_name = "wife"
    switch = Switch(name=test_name)
    assert switch.name == test_name
