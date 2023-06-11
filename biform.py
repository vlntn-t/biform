# TODO: add python3 biform.py apply
# should delete all objects (measures, dimensions, variables, etc.) in the app and apply the items from the JSON files
# TODO: add python3 biform.py plan
# should show a diff between the current state and the desired state

import argparse
import json
import os
import asyncio

# Initialize the parser
parser = argparse.ArgumentParser(
    prog='BIForm CLI', description='Your CLI tool for programmatically managing BI apps')
subparsers = parser.add_subparsers(dest='command')

# Add "init" command
init_parser = subparsers.add_parser(
    'init', help='Initialize the project')

# Add "pull" command
pull_parser = subparsers.add_parser(
    'pull', help='Pull all metadata for specified apps from Qlik Sense API')

# Add "apply" command
apply_parser = subparsers.add_parser(
    'apply', help='Apply all metadata from JSON files to specified apps')


def init_project():
    if os.name == 'posix':  # macOS or Linux
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

        # chekc if qlik context is already set up
        if os.system('qlik context ls') != 0:
            # qlik context init to set up the context
            os.system('qlik context init')
        else:
            print('qlik context is already set up')
            print(' ')
            # qlik context ls
            os.system('qlik context ls')

        # Create biforms folder
        if not os.path.exists('biforms'):
            os.mkdir('biforms')
        else:
            print('biforms folder already exists')

        # Create state.json
        if not os.path.exists('biforms/state.json'):
            with open('biforms/state.json', 'w') as f:
                json.dump({
                    'version': 1
                }, f, indent=2)
        else:
            print('state.json already exists')

        # Create README.md for documentation purposes
        if not os.path.exists('biforms/README.md'):
            with open('biforms/README.md', 'w') as f:
                f.write("# Project Title\n\nProject description")
        else:
            print('README.md already exists')

        # Create config.json with placeholders if it doesn't exist
        config = {
            'TENANT': 'https://<tenant>.<region>.qlikcloud.com',
            'API_KEY': 'YOUR_API_KEY',
            'APP_IDS': ['YOUR_APP_ID_1', 'YOUR_APP_ID_2']
        }

        if not os.path.exists('biforms/config.json'):
            with open('biforms/config.json', 'w') as f:
                json.dump(config, f, indent=2)
        else:
            print('config.json already exists')

    elif os.name == 'nt':  # Windows
        # check if qlik cli is installed
        if os.system('qlik version') != 0:
            # qlik context init to set up the context
            os.system('qlik context init')
            # qlik context ls
            os.system('qlik context ls')
            # Create biforms folder
            if not os.path.exists('biforms'):
                os.mkdir('biforms')
            else:
                print('biforms folder already exists')
            # Create state.json
            if not os.path.exists('biforms/state.json'):
                with open('biforms/state.json', 'w') as f:
                    json.dump({
                        'version': 1
                    }, f, indent=2)
            else:
                print('state.json already exists')

            # Create README.md for documentation purposes
            if not os.path.exists('biforms/README.md'):
                with open('biforms/README.md', 'w') as f:
                    f.write("# Project Title\n\nProject description")
            else:
                print('README.md already exists')

            # Create config.json with placeholders
            if not os.path.exists('biforms/config.json'):
                config = {
                    'TENANT': 'https://<tenant>.<region>.qlikcloud.com',
                    'API_KEY': 'YOUR_API_KEY',
                    'APP_IDS': ['YOUR_APP_ID_1', 'YOUR_APP_ID_2']
                }
                with open('biforms/config.json', 'w') as f:
                    json.dump(config, f, indent=2)
            else:
                print('config.json already exists')

        else:
            print('Qlik CLI is not installed. Please install it from https://github.com/qlik-oss/qlik-cli/releases')


def pull_project():
    # Read config.json
    with open('biforms/config.json', 'r') as f:
        config = json.load(f)

    for app_id in config['APP_IDS']:
        # Create a folder for each app if it doesn't exist
        if not os.path.exists(f'biforms/{app_id}'):
            os.mkdir(f'biforms/{app_id}')
            os.mkdir(f'biforms/{app_id}/frontend')
            os.mkdir(f'biforms/{app_id}/backend')

        # Export the QS apps to respective folders
        # qlik app export <appId> [flags]
        print(f'Pulling app {app_id}')
        os.system(
            f'cd biforms/{app_id} && qlik app export {app_id} > {app_id}.qvf')

        print(f'Pulling master measures for app {app_id}')
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
        with open(f'biforms/{app_id}/frontend/measures.json', 'w') as f:
            json.dump(all_measure_properties, f, indent=2)

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
        with open(f'biforms/{app_id}/frontend/dimensions.json', 'w') as f:
            json.dump(all_dimension_properties, f, indent=2)

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
        with open(f'biforms/{app_id}/frontend/variables.json', 'w') as f:
            json.dump(all_variable_properties, f, indent=2)

        # Pull the script for each app (qlik app script get --app <appid/app_name>)
        print(f'Pulling script for app {app_id}')
        script = os.popen(
            f'qlik app script get --app {app_id}').read()

        # Save the script in a txt file
        with open(f'biforms/{app_id}/backend/script.qvs', 'w') as f:
            f.write(script)


def apply_project():
    # Read config.json
    with open('biforms/config.json', 'r') as f:
        config = json.load(f)

    for app_id in config['APP_IDS']:
        # Remove all measures for each app before applying the master measures (qlik app measure rm ID-1 ID-2)
        print('Removing all measures for each app')
        # get all measure ids
        measures = os.popen(
            f'qlik app measure ls --app {app_id} --json').read()
        # Parse the JSON response
        measures = json.loads(measures)
        # Extract the measure ids from the JSON
        measure_ids = [item["qId"] for item in measures]
        # Remove all measures
        for measure_id in measure_ids:
            os.system(
                f'qlik app measure rm {measure_id} --app {app_id}')

        # Remove all dimensions for each app before applying the master dimensions (qlik app dimension rm ID-1 ID-2)
        print('Removing all dimensions for each app')
        # get all dimension ids
        dimensions = os.popen(
            f'qlik app dimension ls --app {app_id} --json').read()
        # Parse the JSON response
        dimensions = json.loads(dimensions)
        # Extract the dimension ids from the JSON
        dimension_ids = [item["qId"] for item in dimensions]
        # Remove all dimensions
        for dimension_id in dimension_ids:
            os.system(
                f'qlik app dimension rm {dimension_id} --app {app_id}')

        # Remove all variables for each app before applying the master variables (qlik app variable rm ID-1 ID-2)
        print('Removing all variables for each app')
        # get all variable ids
        variables = os.popen(
            f'qlik app variable ls --app {app_id} --json').read()
        # Parse the JSON response
        variables = json.loads(variables)
        # Extract the variable title from the JSON
        variable_titles = [item["title"]
                           for item in variables]
        # Remove all variables
        for variable_title in variable_titles:
            os.system(
                f'qlik app variable rm {variable_title} --app {app_id}')

        # Apply all measures for each app
        print(f'Applying master measures for app {app_id}')

        # qlik app measure set ./my-measures-glob-path.json
        os.system(
            f'qlik app measure set ./biforms/{app_id}/frontend/measures.json --app {app_id}')

        # Apply all dimensions for each app
        print(f'Applying master dimensions for app {app_id}')

        # qlik app dimension set ./my-dimensions-glob-path.json
        os.system(
            f'qlik app dimension set ./biforms/{app_id}/frontend//dimensions.json --app {app_id}')

        # Apply all variables for each app
        print(f'Applying variables for app {app_id}')

        # qlik app variable set ./my-variables-glob-path.json
        os.system(
            f'qlik app variable set ./biforms/{app_id}/frontend//variables.json --app {app_id}')

        # Apply the script for each app
        print(f'Applying script for app {app_id}')

        # qlik app script set ./my-script-glob-path.qvs (qlik app script set <path-to-script-file.qvs>)
        os.system(
            f'qlik app script set ./biforms/{app_id}/backend//script.qvs --app {app_id}')


init_parser.set_defaults(func=init_project)
pull_parser.set_defaults(func=pull_project)
apply_parser.set_defaults(func=apply_project)

# Parse the arguments
args = parser.parse_args()
if args.command:
    loop = asyncio.get_event_loop()
    if asyncio.iscoroutinefunction(args.func):
        loop.run_until_complete(args.func())
    else:
        args.func()
