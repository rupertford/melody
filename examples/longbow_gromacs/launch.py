'''The launch function in this file is called by Melody for each
particular configuration.'''

def launch(option):
    '''Set the gromacs input data using the supplied input options, run
    gromacs and extract and return the required outputs.'''

    from melody.inputs import create_input
    input_file = create_input(option, template_name="input.mdp")

    # save the input file in the appropriate place and launch gromacs using longbow
    # ...

    # determine if the run was successful
    success = True

    results = None
    if success:
        # extract the required outputs
        results = {"rate":{"value":35, "units":"ns/day"}, }

    return success, results
