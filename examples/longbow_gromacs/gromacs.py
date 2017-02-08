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
'''A demonstration of how to search some gromacs options. We will use
jinja2 to set input values, Longbow to run gromacs and some text
processing to extract the required results. However, we do not yet do
so.'''

import subprocess
from random import randint

from melody.inputs import Choice, FloatRange
from melody.main import Melody
from melody.search import BruteForce


def launch(option):
    '''Launcher method for the gromacs example.

    Set the gromacs input data using the supplied input options, run
    gromacs and extract and return the required outputs.'''
    from melody.inputs import create_input
    inputfile = create_input(option, template_name="input.mdp")
    results = None
    success = None

    # Create directory structure for jobs.
    identifier = "".join(["%s" % randint(0, 9) for _ in range(0, 5)])
    infile = "gmx" + identifier + ".mdp"

    outfile = open(infile, "w")
    outfile.write(inputfile)
    outfile.close()

    try:

        # Run grompp preprocessor.
        print "handing configuration file '%s' off to grompp..." % infile

        # In gromacs v5+ this should be gmx grompp .....
        gromppcmdl = ("grompp"
                      " -f " + infile +
                      " -p setup.top"
                      " -c setup.gro"
                      " -po _" + infile +
                      " -o run" + identifier + ".tpr")

        handle = subprocess.Popen(gromppcmdl, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=True)
        gromppout, grompperr = handle.communicate()
        setuperrstate = handle.returncode

        # TODO: probably should look at using a log file and log the outputs.
        if setuperrstate != 0:

            raise OSError

        print "grompp ran successfully."

        # Fire off run with Longbow.
        print "handing simulation off to Longbow for execution..."

        # In gromacs v5+ this should be gmx mdrun ....
        longbowcmdl = ("longbow --verbose mdrun -deffnm run" + identifier)

        # TODO: realtime status updates by capturing stdout in real time is
        # better.
        #handle = subprocess.Popen(longbowcmdl, stdout=subprocess.PIPE,
        #                          stderr=subprocess.PIPE, shell=True)
        #longbowout, longbowerr = handle.communicate()
        #runerrstate = handle.returncode

        # Determine if the run was successful
        #if runerrstate != 0:

        #    raise OSError

        #else:

            #print "job ran successfully and all results staged back."
            #success = True

    except OSError:

        success = False

    # Extract the required outputs.
    if success:

        results = {"id": {"value": identifier}}
        resfile = open("run" + identifier + ".log", "r").readlines()

        for line in resfile:

            if "Performance:" in line:

                results["nspd"] = {"value": line.split()[1], "units": "ns/day"}
                break

    return success, results

INPUTS = [Choice(name="tcoupl", inputs=["Berendsen", "Nose-Hoover"]),
          FloatRange(name="rcoulomb", low=1.1, high=1.6, step=0.1)]

MELODY = Melody(inputs=INPUTS, function=launch, method=BruteForce)
MELODY.search()
