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
    #print namelist

    makefile_include = create_input(makefile_option, "Makefile.include", template_location="templates")
    #print makefile_include

    # save the input files in the appropriate place

    # compile shallow if required

    # run shallow

    # determine if the run was successful
    success = True

    results = None
    if success:
        # extract the required outputs
        results = [10]

    return success, results
