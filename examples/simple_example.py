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
'''A first example showing how to initialise and run melody. The
different input types are shown, along with a dummy test function,
using a brute force search'''

from melody.inputs import Switch, Choice, IntRange, FloatRange, Subsets
from melody.search import BruteForce
from melody.main import Melody

def test_function(option):
    '''A dummy test function. The function takes a list of inputs as an
    argument and returns whether the execution was successful (in our
    case we always return True) followed by the target output (in our
    case we simply output a fixed value'''
    return True, {"value": 10}

INPUTS = [
    Switch(name="Debug Flag", off="", on="-g"),
    Choice(name="Opt Flags", inputs=["-O", "-O2", "-O3"]),
    IntRange(name="Segment Size", low=0, high=20, step=10),
    FloatRange(name="Tolerance", low=0.0, high=1.0, step=0.5),
    Subsets(name="Silly", inputs=["-fast", "-great", "-super"])]

MELODY = Melody(inputs=INPUTS, function=test_function, method=BruteForce)
MELODY.search()
