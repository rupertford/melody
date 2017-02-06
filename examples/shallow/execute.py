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
''' '''

from melody.inputs import create_input

def execute(option):
    ''' xxx '''

    namelist_option = []
    makefile_option = []
    flags = ""
    for entry in option:
        key = entry.keys()[0]
        if key == "Problem Size":
            namelist_option.append({"SIZE":entry[key]})
        elif key == "F90":
            makefile_option.append(entry)
        else:
            flags += entry[key] + " "
    makefile_option.append({"F90FLAGS":flags})
            
    namelist = create_input(namelist_option, "namelist", template_location="templates")

    makefile_include = create_input(makefile_option, "Makefile.include", template_location="templates")

    benchmark_base = "/home/rupert/proj/GOcean/shallow_benchmark"

    # save the input files in the appropriate place
    location = benchmark_base + "/original/namelist"
    f = open(location, 'w')
    f.write(namelist)
    f.flush()

    location = benchmark_base + "/common/Makefile.include"
    f = open(location, 'w')
    f.write(makefile_include)
    f.flush()

    # compile shallow if required
    #import os
    #os.chdir("/home/rupert/proj/GOcean/shallow_benchmark/original")
    import subprocess
    make_process = subprocess.Popen(["make", "clean"], cwd="/home/rupert/proj/GOcean/shallow_benchmark/original",  stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if make_process.wait() != 0:
        return False, []

    make_process = subprocess.Popen(["make"], cwd="/home/rupert/proj/GOcean/shallow_benchmark/original", stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if make_process.wait() != 0:
        return False, []

    # run shallow
    make_process = subprocess.Popen(["./shallow_base"], cwd="/home/rupert/proj/GOcean/shallow_benchmark/original", stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if make_process.wait() != 0:
        return False, []
    stderr = make_process.stderr.read()
    stdout = make_process.stdout.read()

    # determine if the results are correct. We will need to look at
    # the results from stdout but for the moment we assume they are
    # correct

    # extract the required outputs
    for line in stdout.split("\n"):
        if "Time-stepping" in line:
            total_time = line.split()[2]

    return True, total_time
