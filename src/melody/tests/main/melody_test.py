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
'''pytest tests for the Melody class in the main.py melody file'''

from melody.main import Melody


def test_melody_vanilla():
    '''check that initial values are set to None if they are not
    provided'''
    melody = Melody()
    assert melody.function is None
    assert melody.inputs is None
    assert melody.method is None
    assert melody._state is None


def test_melody_initial_values():
    '''check that values are stored correctly if provided at initialisation'''
    function = "function"
    method = "method"
    state = "state"
    inputs = "inputs"
    melody = Melody(function=function, method=method, state=state,
                    inputs=inputs)
    assert melody.function == function
    assert melody.inputs == inputs
    assert melody.method == method
    assert melody._state == state


def test_melody_set_values():
    '''check that values are stored correctly if directly set'''
    function = "function"
    method = "method"
    inputs = "inputs"
    melody = Melody()
    melody.function = function
    melody.method = method
    melody.inputs = inputs
    assert melody.function == function
    assert melody.inputs == inputs
    assert melody.method == method


def test_melody_search(capsys):
    '''check that melody search runs when we provide a valid set of inputs'''
    from melody.inputs import Choice
    from melody.search import BruteForce
    inputs = [Choice(name="c",
                     inputs=["c1", "c2"])]

    def function(input_var):
        '''test function'''
        return 0, input_var
    search_method = BruteForce
    melody = Melody(method=search_method, inputs=inputs, function=function)
    melody.search()
    out, _ = capsys.readouterr()
    assert "[{'c': 'c1'}] 0 [{'c': 'c1'}]" in out
    assert "[{'c': 'c2'}] 0 [{'c': 'c2'}]" in out
