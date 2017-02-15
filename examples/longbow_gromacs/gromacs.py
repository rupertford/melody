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
from melody.inputs import create_input
from melody.main import Melody
from melody.search import BruteForce


def launch(option):
    '''Launcher method for the gromacs example.

    Set the gromacs input data using the supplied input options, run
    gromacs and extract and return the required outputs.'''
    results = None
    success = None

    filestructure = create_input(option, template_name="input.mdp")
    instanceid = "".join(["%s" % randint(0, 9) for _ in range(0, 5)])

    try:

        # Create input file for this run.
        _saveinputfile(instanceid, filestructure)

        # Run grompp preprocessor.
        print("Handing configuration file 'gmx%s.mdp' off to grompp..." %
              instanceid)

        # Try the v5.x.x first.
        gromppout = _grompp(instanceid)

        if gromppout[0] == 0:

            print "grompp ran successfully."

        else:

            raise OSError("grompp step failed.")

        # Launch a remote job using Longbow.
        print "Handing simulation off to Longbow for execution..."

        longbowout = _remotemdrun(instanceid)

        if longbowout[0] == 0:

            print "Remote simulation completed. All files are staged."
            success = True

        else:

            raise OSError("The Longbow instance went into error, check the "
                          "longbow.xx.log file for details.")

    except OSError:

        success = False

    # Extract the required outputs.
    if success:

        results = _extractresults(instanceid, results)

    return success, results


def _extractresults(instanceid, results):
    '''Extract the resulting performance figure.'''

    results = {"id": {"value": instanceid}}
    resfile = open("run" + instanceid + ".log", "r").readlines()

    for line in resfile:

        if "Performance:" in line:

            results["nspd"] = {"value": line.split()[1], "units": "ns/day"}
            break

    return results


def _grompp(instanceid):
    '''Launch grompp preprocessor.'''
    # In gromacs v5+ this should be gmx grompp .....
    cmd = ("gmx grompp"
           " -f gmx" + instanceid + ".mdp" +
           " -p setup.top"
           " -c setup.gro"
           " -po _gmx" + instanceid + ".mdp" +
           " -o run" + instanceid + ".tpr")

    state, stdout, stderr = _shelllauncher(cmd)

    return state, stdout, stderr


def _localmdrun(instanceid):
    '''Execute md simulation locally.'''
    # In gromacs v5+ this should be gmx mdrun ....
    cmd = ("gmx mdrun -deffnm run" + instanceid)

    state, stdout, stderr = _shelllauncher(cmd)

    return state, stdout, stderr


def _remotemdrun(instanceid):
    '''Execute md simulation remotely using longbow.'''
    # In gromacs v5+ this should be gmx mdrun ....
    cmd = ("longbow --verbose --log longbow." + instanceid +
           ".log gmx mdrun -deffnm run" + instanceid)

    # TODO: realtime status updates would be a big improvement.
    # TODO: In order to do this full integration with longbow is necessary
    # rather than a naive shell launcher.
    # TODO: Need to set up a logger before integrating fully, otherwise
    # Longbow will be silent.
    state, stdout, stderr = _shelllauncher(cmd)

    return state, stdout, stderr


def _saveinputfile(instanceid, filestructure):
    '''Save out an input file.'''
    inputfile = open("gmx" + instanceid + ".mdp", "w")
    inputfile.write(filestructure)
    inputfile.close()


def _shelllauncher(cmd):
    '''Spawn a shell to execute a Linux command.'''
    # Launch a shell, so that commands can be string format and not list
    # (careful with user input).
    handle = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, shell=True)
    stdout, stderr = handle.communicate()
    state = handle.returncode

    return state, stdout, stderr

INPUTS = [Choice(name="tcoupl", inputs=["Berendsen", "Nose-Hoover"]),
          FloatRange(name="rcoulomb", low=1.1, high=1.6, step=0.1)]

MELODY = Melody(inputs=INPUTS, function=launch, method=BruteForce)
MELODY.search()
