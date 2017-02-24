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
'''pytest tests for the BruteForce class in the search.py melody file'''

import pytest
from melody.search import BruteForce


def test_run(capsys):
    '''check that bruteforce runs when we provide a valid set of inputs'''
    from melody.inputs import Choice
    inputs = [Choice(name="c",
                     inputs=["c1", "c2"])]

    def function(input_var):
        '''test function'''
        return 0, input_var
    search_method = BruteForce(function=function, inputs=inputs)
    search_method.run()
    out, _ = capsys.readouterr()
    assert "[{'c': 'c1'}] 0 [{'c': 'c1'}]" in out
    assert "[{'c': 'c2'}] 0 [{'c': 'c2'}]" in out


@pytest.mark.xfail(reason=("bug : state support is work in progress"))
def test_state_run(capsys, monkeypatch):
    '''check that bruteforce runs when we provide a valid set of inputs
    with state'''
    from melody.inputs import Choice
    choice = Choice(name="c", inputs=["c1", "c2"])
    monkeypatch.setattr(choice, "_state", True)
    inputs = [choice]

    def function(input_var):
        '''test function'''
        return 0, input_var
    state = "state"
    search_method = BruteForce(function=function, inputs=inputs, state=state)
    search_method.run()
    out, _ = capsys.readouterr()
    assert "[{'c': 'c1'}] 0 [{'c': 'c1'}]" in out
    assert "[{'c': 'c2'}] 0 [{'c': 'c2'}]" in out


def test_func_too_few_ret_args():
    '''check that an exception is raised if too few function return
    arguments are provided'''
    from melody.inputs import Choice
    choice = Choice(name="c", inputs=["c1", "c2"])
    inputs = [choice]
    def function(inputs):
        '''test function'''
        return inputs
    search_method = BruteForce(inputs, function)
    with pytest.raises(RuntimeError) as excinfo:
        search_method.run()
    assert "function must return 2 values" in str(excinfo.value)


def test_func_too_many_ret_args():
    '''check that an exception is raised if too many function return
    arguments are provided'''
    from melody.inputs import Choice
    choice = Choice(name="c", inputs=["c1", "c2"])
    inputs = [choice]
    def function(inputs):
        '''test function'''
        return inputs, 0, 0
    search_method = BruteForce(inputs=inputs, function=function)
    with pytest.raises(RuntimeError) as excinfo:
        search_method.run()
    assert "function must return 2 values" in str(excinfo.value)
