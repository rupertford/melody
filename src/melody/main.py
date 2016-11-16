'''melody is a simple generic tuning library primarily designed for
the optimisation of software on hpc architectures'''


class Melody(object):
    ''' The main class '''

    def __init__(self, function=None, method=None, inputs=None):
        self._function = function
        self._method = method
        self._inputs = inputs

    @property
    def function(self):
        '''Return the function associated with this instance of melody'''
        return self._function

    @function.setter
    def function(self, function):
        '''Set the function associated with this instance of melody'''
        self._function = function

    @property
    def method(self):
        '''Return the optimisation/search method associated with this instance
of melody'''
        return self._method

    @method.setter
    def method(self, method):
        '''Set the optimisation/search method associated with this instance of
melody'''
        self._method = method

    @property
    def inputs(self):
        '''Return the input search parameters for the associated function'''
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        '''Set the input search parameters for the associated function'''
        self._inputs = inputs

    def search(self):
        '''Start the optimisation/search using the supplied optimisation
        method with the supplied inputs for the supplied function'''
        search = self._method()
        search.inputs = self._inputs
        search.function = self._function
        search.run()
