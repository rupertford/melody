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
'''pytest tests for the create_input function in the inputs.py melody file'''

import os
import pytest
from melody.inputs import create_input

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(SCRIPT_DIR, "template")
TEMPLATE_NAME = "template.txt"
EXPECTED = "result"
OPTION = [{"KEY": EXPECTED}]

def test_create_input():
    ''' test that we can modify a template file correctly '''
    result = create_input(OPTION, TEMPLATE_NAME, template_location=TEMPLATE_DIR)
    assert EXPECTED in result

@pytest.mark.xfail(reason="bug : incorrect input format error not caught correctly")
def test_option_wrong_format():
    '''check that we raise an exception if the input option is not in the
    expected format'''
    option = [EXPECTED]
    result = create_input(option, TEMPLATE_NAME, template_location=TEMPLATE_DIR)
    assert EXPECTED in result
    
@pytest.mark.xfail(reason="bug : incorrect input value error not caught correctly")
def test_option_wrong_datatype():
    '''test that we raise an exception if the datatype of the data is not
    a string'''
    expected = 7
    option = [{"KEY": expected}]
    result = create_input(option, TEMPLATE_NAME, template_location=TEMPLATE_DIR)
    assert expected in result

@pytest.mark.xfail(reason="bug : template does not exist error not caught correctly")
def test_non_existant_template():
    '''test that we raise an exception if the specified template does not exist'''
    template_name = "invalid.txt"
    result = create_input(OPTION, template_name, template_location=TEMPLATE_DIR)
    assert EXPECTED in result

@pytest.mark.xfail(reason="bug : template does not exist error not caught correctly")
def test_non_existant_template_location():
    '''test that we raise an exception if the specified template location does not exist'''
    template_dir = os.path.join(SCRIPT_DIR, "invalid")
    result = create_input(OPTION, TEMPLATE_NAME, template_location=template_dir)
    assert EXPECTED in result
