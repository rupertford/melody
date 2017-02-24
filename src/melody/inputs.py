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
'''This file contains a set of input classes that users can use to
define the space they want to search. These classes can also be
specialised for particular scenarios.'''


class Input(object):
    '''This is the base class for all types of input class.'''

    def __init__(self, name, options, state=None):
        self._state = state
        self._name = name
        self._options = options

    @property
    def state(self):
        '''Returns the state variable. This is 'None' by default.'''
        return self._state

    @property
    def name(self):
        '''Returns the name of the input class. All classes are expected to
        define a name'''
        return self._name

    @property
    def options(self):
        '''Returns the particular set of options that are valid for the
        instance of the input'''
        return self._options


class Fixed(Input):
    '''This class simply returns a single fixed value. It therefore does
    not add to the search space. Rather it is a convenience class.'''

    def __init__(self, name, value):
        options = [value]
        Input.__init__(self, name, options)


class Switch(Input):
    '''This class allows the user to specify two options where only one is
    valid at a time. It could be considered to be a special case of
    Choice, but it is so common that a separate class makes sense.'''

    def __init__(self, name, off=None, on=None):
        if not off and not on:
            raise RuntimeError(
                "A value must be provided for at least one of 'off' or 'on'")
        options = []
        if off:
            options.append(off)
        else:
            options.append("")
        if on:
            options.append(on)
        else:
            options.append("")
        Input.__init__(self, name, options)


class Choice(Input):
    '''This class allows the user to specify an unlimited number of
    options, where only one option is valid at a time.

    '''

    def __init__(self, name, inputs, pre=None):
        options = []
        for value in inputs:
            if pre:
                options.append(pre + value)
            else:
                options.append(value)
        Input.__init__(self, name, options)


class IntRange(Input):
    '''This class implements the integer version of the Range class,
    allowing a set of integer inputs to be defined by a low, high and
    step.'''

    def __init__(self, name, low, high, step):
        options = [i for i in range(low, high, step)]
        Input.__init__(self, name, options)


class FloatRange(Input):
    '''This class implements a range of floating point values,
    which are set by low, high and step values.'''

    def __init__(self, name, low, high, step):
        from numpy import arange
        options = [f for f in arange(low, high, step)]
        Input.__init__(self, name, options)


class Subsets(Input):
    '''This class allows all combinations of a particular set of values to
    be chosen, including, no values, individual values, pairs of values,
    triplets of values etc.'''

    def __init__(self, name, inputs):
        self._inputs = inputs
        self._options = []
        for k in range(len(inputs) + 1):
            self._recurse(inputs, [], depth=0, max_depth=k)
        Input.__init__(self, name, self._options)

    def _recurse(self, inputs, output, depth, max_depth):
        '''We work out all combinations using this internal recursion method'''
        if depth < max_depth:
            for index, option in enumerate(inputs):
                my_output = list(output)
                my_output.append(option)
                self._recurse(inputs[index + 1:], my_output, depth + 1,
                              max_depth)
        else:
            self._options.append(output)


def create_input(option, template_name, template_location="template"):

    '''create an input file using jinja2 by filling a template
    with the values from the option variable passed in.'''

    # restructure option list into jinja2 input format
    jinja2_input = {}
    for item in option:
        try:
            jinja2_input.update(item)
        except ValueError:
            raise RuntimeError(
                ("inputs.py, create_input : format of item '{0}' is not "
                 "supported. Expecting a dictionary.".format(str(item))))

    # load the template and fill it with the option variable contents
    import jinja2
    try:
        template_loader = jinja2.FileSystemLoader(searchpath=template_location)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(template_name)
        output_text = template.render(jinja2_input)
    except jinja2.TemplateNotFound:
        raise RuntimeError("template '{0}' not found".format(template_name))
    # return the particular input file as a string
    return output_text
