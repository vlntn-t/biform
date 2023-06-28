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
        # Get the apps name (qlik app get {app_id})
        app_name = os.popen(f'qlik app get {app_id}').read()
        app_name = json.loads(app_name)["attributes"]["name"]
        print(f'Pulling app {app_name} | {app_id}')

        # Remove the app folder if it exists
        if os.path.exists(f'biforms/{app_id}'):
            if os.name == 'nt':
                os.system(f'cd biforms && rmdir /s /q {app_id} && cd ..')
            elif os.name == 'posix':
                os.system(f'cd biforms && rm -rf {app_id} && cd ..')
            else:
                print('OS not supported')
                exit()

        if not os.path.exists(f'biforms/{app_id}'):
            os.mkdir(f'biforms/{app_id}')

        # Get the apps folder name
        app_name_mod = app_name.lower()
        app_name_mod = app_name_mod.replace(' ', '-').replace('.', '-')
        folder_name = app_name_mod + '-unbuild'

        # check which os is used and move the folder to the app folder
        if os.name == 'nt':
            os.system(
                f'qlik app export {app_id} --NoData > biforms/{app_id}/{app_id}.qvf && qlik app unbuild --app {app_id} && move {folder_name} biforms/{app_id}')
        elif os.name == 'posix':
            os.system(
                f'qlik app export {app_id} --NoData > biforms/{app_id}/{app_id}.qvf && qlik app unbuild --app {app_id} && mv {folder_name} biforms/{app_id}')
        else:
            print('OS not supported')
            exit()


def plan_project():
    print('Not implemented yet. You can contribute to this project at: https://github.com/vlntn-t/biform')

    # for app_id in config['APP_IDS']:
    #     # Get the JSON data for all measures
    #     with open(f'biforms/{app_id}/frontend/measures.json', 'r') as f:
    #         measures = json.load(f)
    #     # Pull the measure JSON from the app in Qlik Sense
    #     measures_qlik = os.popen(
    #         f'qlik app measure ls --app {app_id} --json').read()


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
