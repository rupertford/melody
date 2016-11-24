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
