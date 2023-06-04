# TODO: add python3 biform.py apply
# should delete all objects (measures, dimensions, variables, etc.) in the app and apply the items from the JSON files

import argparse
import json
import os
import asyncio

# Initialize the parser
parser = argparse.ArgumentParser(
    prog='BIForm CLI', description='Your CLI tool for programmatically managing BI apps')
subparsers = parser.add_subparsers(dest='command')

# Add "init" command
init_parser = subparsers.add_parser('init', help='Initialize the project')

# Add "pull" command
pull_parser = subparsers.add_parser(
    'pull', help='Pull all metadata for specified apps from Qlik Sense API')


def init_project():
    # TODO: check which OS the user is running
    if os.system('brew -v') != 0:
        os.system(
            '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
    else:
        print('brew is already installed')
        print(' ')

    if os.system('qlik version') != 0:
        os.system('brew tap qlik-oss/taps && brew install qlik-cli')
    else:
        print('qlik cli is already installed')
        print(' ')

    # qlik context init to set up the context
    os.system('qlik context init')
    # TODO: check if context is already set up
    # TODO: get tenant and api key from user input and store in config.json

    # qlik context ls
    os.system('qlik context ls')

    # Create biforms folder
    os.mkdir('biforms')
    # Create state.json
    with open('biforms/state.json', 'w') as f:
        json.dump({
            'version': 1
        }, f, indent=4)

    # Create README.md
    with open('biforms/README.md', 'w') as f:
        f.write("# Project Title\n\nProject description")

    # Create config.json with placeholders
    config = {
        'TENANT': 'https://<tenant>.<region>.qlikcloud.com',
        'API_KEY': 'YOUR_API_KEY',
        'APP_IDS': ['YOUR_APP_ID_1', 'YOUR_APP_ID_2']
    }
    with open('biforms/config.json', 'w') as f:
        json.dump(config, f, indent=4)


def pull_metadata():
    # Read config.json
    with open('biforms/config.json', 'r') as f:
        config = json.load(f)

    # Pull all measures for each app
    for app_id in config['APP_IDS']:
        print(f'Pulling master measures for app {app_id}')
        # Create a folder for each app if it doesn't exist
        if not os.path.exists(f'biforms/{app_id}'):
            os.mkdir(f'biforms/{app_id}')

        # qlik app measure ls --app <appid/app_name> and store the table in a variable
        measures = os.popen(
            f'qlik app measure ls --app {app_id} --json').read()

        # Parse the JSON response
        measures = json.loads(measures)

        # Create a list to store all measure properties
        all_measure_properties = []

        # Extract the measure ids from the JSON
        measure_ids = [item["qId"] for item in measures]

        # Get the measure properties for each measure id and append to the list
        for measure_id in measure_ids:
            measure_properties = os.popen(
                f'qlik app measure properties {measure_id} --app {app_id} --json').read()
            # print(measure_properties)
            measure_properties_json = json.loads(measure_properties)
            all_measure_properties.append(measure_properties_json)

        # Save all measure properties in a JSON file
        with open(f'biforms/{app_id}/measures.json', 'w') as f:
            json.dump(all_measure_properties, f, indent=4)

        # Pull all dimensions for each app
        print(f'Pulling master dimensions for app {app_id}')
        # qlik app dimensions ls --app <appid/app_name> and store the table in a variable
        dimensions = os.popen(
            f'qlik app dimension ls --app {app_id} --json').read()

        # Parse the JSON response
        dimensions = json.loads(dimensions)

        # Create a list to store all dimension properties
        all_dimension_properties = []

        # Extract the dimension ids from the JSON
        dimension_ids = [item["qId"] for item in dimensions]

        # Get the dimension properties for each dimension id and append to the list
        for dimension_id in dimension_ids:
            dimension_properties = os.popen(
                f'qlik app dimension properties {dimension_id} --app {app_id} --json').read()
            # print(dimension_properties)
            dimension_properties_json = json.loads(dimension_properties)
            all_dimension_properties.append(dimension_properties_json)

        # Save all dimension properties in a JSON file
        with open(f'biforms/{app_id}/dimensions.json', 'w') as f:
            json.dump(all_dimension_properties, f, indent=4)

        # Pull all variables for each app
        print(f'Pulling variables for app {app_id}')
        # qlik app variable ls --app <appid/app_name> and store the table in a variable
        variables = os.popen(
            f'qlik app variable ls --app {app_id} --json').read()

        # Parse the JSON response
        variables = json.loads(variables)

        # Create a list to store all variable properties
        all_variable_properties = []

        # Extract the variable title from the JSON
        variable_titles = [item["title"] for item in variables]

        # Get the variable properties for each variable title and append to the list
        for variable_title in variable_titles:
            variable_properties = os.popen(
                f'qlik app variable properties {variable_title} --app {app_id} --json').read()
            variable_properties_json = json.loads(variable_properties)
            all_variable_properties.append(variable_properties_json)

        # Save all variable properties in a JSON file
        with open(f'biforms/{app_id}/variables.json', 'w') as f:
            json.dump(all_variable_properties, f, indent=4)

        # Pull all sheets for each app
        print(f'Pulling sheets for app {app_id}')
        # qlik app object ls --app <appid/app_name> and store the table in a variable
        objects = os.popen(
            f'qlik app object ls --app {app_id} --json').read()
        # print(objects)

        # Parse the JSON response
        objects = json.loads(objects)

        # Create a list to store all sheet properties
        all_sheet_properties = []

        # Extract the object ids from the JSON where qType is "sheet"
        sheet_ids = [item["qId"]
                     for item in objects if item["qType"] == "sheet"]

        # Get the sheet properties for each object id and append to the list
        for sheet_id in sheet_ids:
            sheet_properties = os.popen(
                f'qlik app object properties {sheet_id} --app {app_id} --json').read()
            sheet_properties_json = json.loads(sheet_properties)
            all_sheet_properties.append(sheet_properties_json)

        # Save all sheet properties in a JSON file
        with open(f'biforms/{app_id}/sheets.json', 'w') as f:
            json.dump(all_sheet_properties, f, indent=4)


            # Map the functions to the commands
init_parser.set_defaults(func=init_project)
pull_parser.set_defaults(func=pull_metadata)

# Parse the arguments
args = parser.parse_args()
if args.command:
    loop = asyncio.get_event_loop()
    if asyncio.iscoroutinefunction(args.func):
        loop.run_until_complete(args.func())
    else:
        args.func()
