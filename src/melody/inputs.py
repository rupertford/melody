''' '''

class Input(object):
    ''' '''

    def __init__(self, name, options, state=False):
        self._state = state
        self._name = name
        self._options = options

    @property
    def state(self):
        ''' '''
        return self._state

    @property
    def name(self):
        ''' '''
        return self._name

    @property
    def options(self):
        ''' '''
        return self._options


class Fixed(Input):
    ''' '''

    def __init__(self, name=None, value=None):
        options = [value]
        Input.__init__(self, name, options)


class Switch(Input):
    ''' '''

    def __init__(self, name=None, off=None, on=None):
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
    ''' '''

    def __init__(self, name=None, pre=None, inputs=None):
        options = []
        for value in inputs:
            if pre:
                options.append(pre+value)
            else:
                options.append(value)
        Input.__init__(self, name, options)


class Range(Input):
    ''' '''

    def __init__(self, name=None, low=None, high=None, step=None, options=None):
        self._low = low
        self._high = high
        self._step = step
        Input.__init__(self, name, options)


class IntRange(Range):
    ''' '''

    def __init__(self, name=None, low=None, high=None, step=None):
        options = [i for i in range(low, high, step)]
        Range.__init__(self, name=name, low=low, high=high, step=step,
                       options=options)


class FloatRange(Range):
    ''' '''

    def __init__(self, name=None, low=None, high=None, step=None):
        from numpy import arange
        options = [f for f in arange(low, high, step)]
        Range.__init__(self, name=name, low=low, high=high, step=step,
                       options=options)


class Subsets(Input):
    ''' '''

    def __init__(self, name=None, inputs=None):
        self._inputs = inputs
        self._options = []
        for k in range(len(inputs)+1):
            self._recurse(inputs, [], depth=0, max_depth=k)
        Input.__init__(self, name, self._options)

    def _recurse(self, inputs, output, depth, max_depth):
        ''' '''
        if depth<max_depth:
            for index in range(len(inputs)):
                option = inputs[index]
                my_output = list(output)
                my_output.append(option)
                self._recurse(inputs[index+1:], my_output, depth+1, max_depth)
        else:
            self._options.append(output)


def create_input(option, template_name, template_location = "template"):

    '''create an input file using jinja2 by filling a template
    with the values from the option variable passed in.'''

    # restructure option list into jinja2 input format
    jinja2_input = {}
    for item in option:
        jinja2_input.update(item)

    # load the template and fill it with the option variable contents
    import jinja2
    templateLoader = jinja2.FileSystemLoader( searchpath=template_location )
    templateEnv = jinja2.Environment( loader=templateLoader )
    template = templateEnv.get_template( template_name )
    outputText = template.render( jinja2_input )

    # return the particular input file as a string
    return outputText
