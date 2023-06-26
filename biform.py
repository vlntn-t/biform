# TODO: add python3 biform.py apply
# should delete all objects (measures, dimensions, variables, etc.) in the app and apply the items from the JSON files
# TODO: add python3 biform.py plan
# should show a diff between the current state and the desired state

import argparse
import json
import os
import asyncio

parser = argparse.ArgumentParser(
    prog='BIForm CLI', description='Your CLI tool for programmatically managing BI apps')
subparsers = parser.add_subparsers(dest='command')

init_parser = subparsers.add_parser(
    'init', help='Initialize the project')

pull_parser = subparsers.add_parser(
    'pull', help='Pull all metadata for specified apps from Qlik Sense API')

apply_parser = subparsers.add_parser(
    'apply', help='Apply all metadata from JSON files to specified apps')

plan_parser = subparsers.add_parser(
    'plan', help='Show a diff between the current state and the desired state')


def init_project():
    # Create biforms folder
    if not os.path.exists('biforms'):
        os.mkdir('biforms')
    else:
        print('./biforms folder already exists')

    # Create state.json
    if not os.path.exists('biforms/state.json'):
        with open('biforms/state.json', 'w') as f:
            json.dump({
                'version': 1
            }, f, indent=2)
    else:
        print('state.json already exists')

    if not os.path.exists('biforms/apps.json'):
        # Create apps.json with placeholders if it doesn't exist
        config = {
            # 'TENANT': 'https://<tenant>.<region>.qlikcloud.com',
            # 'API_KEY': 'YOUR_API_KEY',
            'APP_IDS': ['YOUR_APP_ID_1', 'YOUR_APP_ID_2']
        }

        with open('biforms/apps.json', 'w') as f:
            json.dump(config, f, indent=2)
    else:
        print('apps.json already exists')


def pull_project():
    # prompt user to confirm
    print('Are you sure you want to pull the project?')
    print('This will overwrite the all configurations such as master measures, dimensions, variables and script in all defined QS apps')
    print('Type "yes" to continue')
    confirmation = input()
    if confirmation != 'yes':
        print('Exiting...')
        exit()

    # Read apps.json
    with open('biforms/apps.json', 'r') as f:
        config = json.load(f)

    for app_id in config['APP_IDS']:
        # Remove the app folder if it exists
        if os.path.exists(f'biforms/{app_id}'):
            os.system(f'rm -rf biforms/{app_id}')

        if not os.path.exists(f'biforms/{app_id}'):
            os.mkdir(f'biforms/{app_id}')

        # Export the QS apps to respective folders
        # qlik app export <appId> [flags]
        print(f'Pulling app {app_id}')
        os.system(
            f'cd biforms/{app_id} && qlik app export {app_id} --NoData > {app_id}.qvf && qlik app unbuild --app {app_id}')

        # Get the apps folder name
        app_folder = os.listdir(f'biforms/{app_id}')[1]

        # Remove the '-unbuild' suffix from the folder name
        app_name = app_folder.replace('-unbuild', '')

        # Create README.md for documentation purposes
        if not os.path.exists(f'biforms/{app_id}/README.md'):
            with open(f'biforms/{app_id}//README.md', 'w') as f:
                f.write(
                    F"# {app_name}\n\nYou can write the apps documentation here.")


def plan_project():
    print('Not implemented yet. You can contribute to this project at: https://github.com/vlntn-t/biform')


def apply_project():
    # prompt user to confirm
    print('Are you sure you want to apply the project?')
    print('This will overwrite the master measures, dimensions, variables and script in all defined QS apps')
    print('Type "yes" to continue')
    confirmation = input()
    if confirmation != 'yes':
        print('Exiting...')
        exit()

    # Read apps.json
    with open('biforms/apps.json', 'r') as f:
        config = json.load(f)

    for app_id in config['APP_IDS']:

        # Get the apps folder name
        app_folder = os.listdir(f'biforms/{app_id}')[1]

        # Remove the '-unbuild' suffix from the folder name
        app_name = app_folder.replace('-unbuild', '')

        # Build the app (qlik app build)
        print(f'Building app {app_name} | {app_id}')

        # cd into the app folder and then into the apps *-unbuild folder
        os.system(
            f'cd biforms/{app_id} && cd {app_folder} && qlik app build --app {app_id} --connections ./connections.yml --dimensions ./dimensions.json --measures ./measures.json --variables ./variables.json --script ./script.qvs --objects ')


init_parser.set_defaults(func=init_project)
pull_parser.set_defaults(func=pull_project)
plan_parser.set_defaults(func=plan_project)
apply_parser.set_defaults(func=apply_project)

# Parse the arguments
args = parser.parse_args()
if args.command:
    loop = asyncio.get_event_loop()
    if asyncio.iscoroutinefunction(args.func):
        loop.run_until_complete(args.func())
    else:
        args.func()
