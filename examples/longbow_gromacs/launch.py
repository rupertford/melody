'''The launch function in this file is called by Melody for each
particular configuration.'''

def launch(option):
    '''Set the gromacs input data using the supplied input options, run
    gromacs and extract and return the required outputs.'''

    input_file = create_input(option)
    print input_file

    # save the input file in the appropriate place and launch gromacs using longbow
    # ...

    # determine if the run was successful
    success = True

    results = None
    if success:
        # extract the required outputs
        results = []

    return success, results

def create_input(option, template_location = "template", template_name = "input.mdp"):
    '''create a gromacs input file using jinja2 by filling a template
    with the values from the option variable passed in.'''

    # restructure option list into jinja2 input format
    jinja2_input = {}
    for item in option:
        jinja2_input.update(item)

    # load the gromacs template and fill it with the option variable contents
    import jinja2
    templateLoader = jinja2.FileSystemLoader( searchpath=template_location )
    templateEnv = jinja2.Environment( loader=templateLoader )
    template = templateEnv.get_template( template_name )
    outputText = template.render( jinja2_input )

    # return the particular gromacs input file as a string
    return outputText
