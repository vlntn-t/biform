import argparse
import json
import os
import asyncio
import datetime

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
    if not os.path.exists('biforms'):
        os.mkdir('biforms')
    else:
        print('./biforms folder already exists')

    if not os.path.exists('biforms/state.json'):
        with open('biforms/state.json', 'w') as f:
            json.dump({
                'version': 1
            }, f, indent=2)
    else:
        print('state.json already exists')

    if not os.path.exists('biforms/apps.json'):
        config = {
            'APP_IDS': ['YOUR_APP_ID_1', 'YOUR_APP_ID_2']
        }

        with open('biforms/apps.json', 'w') as f:
            json.dump(config, f, indent=2)
    else:
        print('apps.json already exists')


def pull_project():
    print('Are you sure you want to pull the project?')
    print('This will overwrite the all configurations such as master measures, dimensions, variables and script in all defined QS apps')
    print('Type "yes" to continue')
    confirmation = input()
    if confirmation != 'yes':
        print('Exiting...')
        exit()

    with open('biforms/apps.json', 'r') as f:
        config = json.load(f)

    for app_id in config['APP_IDS']:

        app_name = os.popen(f'qlik app get {app_id}').read()
        app_name = json.loads(app_name)["attributes"]["name"]
        print(f'Pulling app {app_name} | {app_id}')

        app_name_mod = app_name.replace(' ', '_')

        if os.path.exists(f'biforms/{app_name_mod} | {app_id}'):
            if os.name == 'nt':
                os.system(f'cd biforms && rmdir /s /q "{app_name_mod} | {app_id}" && cd ..')
            elif os.name == 'posix':
                os.system(f'cd biforms && rm -rf "{app_name_mod} | {app_id}" && cd ..')
            else:
                print('OS not supported')
                exit()

        if not os.path.exists(f'biforms/{app_name_mod} | {app_id}'):
            os.mkdir(f'biforms/{app_name_mod} | {app_id}')
        
        if os.name == 'nt':
            os.system(
                f'qlik app export {app_id} --NoData > biforms/"{app_name_mod} | {app_id}"/{app_name_mod}.qvf && qlik app unbuild --app {app_id} --dir "biforms/{app_name_mod} | {app_id}/"')
        elif os.name == 'posix':
            os.system(
                f'qlik app export {app_id} --NoData > biforms/"{app_name_mod} | {app_id}"/{app_name_mod}.qvf && qlik app unbuild --app {app_id} --dir "biforms/{app_name_mod} | {app_id}/"')
        else:
            print('OS not supported')
            exit()

    # Update state.json with the timestamp of the last pull and increase the version number by 1
    with open('biforms/state.json', 'r') as f:
        state = json.load(f)
    state['last_pull'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state['version'] += 1
    with open('biforms/state.json', 'w') as f:
        json.dump(state, f, indent=2)


def plan_project():
    print('Not implemented yet. You can contribute to this project at: https://github.com/vlntn-t/biform')


def apply_project():
    print('Are you sure you want to apply the project?')
    print('This will overwrite the master measures, dimensions, variables and script in all defined QS apps')
    print('Type "yes" to continue')
    confirmation = input()
    if confirmation != 'yes':
        print('Exiting...')
        exit()

    with open('biforms/apps.json', 'r') as f:
        config = json.load(f)

    for app_id in config['APP_IDS']:

        app_name = os.popen(f'qlik app get {app_id}').read()
        app_name = json.loads(app_name)["attributes"]["name"]
        print(f'Applying changes to {app_name} | {app_id}')

        app_name_mod = app_name.replace(' ', '_')

        os.system(
            f'cd biforms/"{app_name_mod} | {app_id}" && qlik app build --app {app_id} --connections ./connections.yml --dimensions ./dimensions.json --measures ./measures.json --variables ./variables.json --script ./script.qvs')


init_parser.set_defaults(func=init_project)
pull_parser.set_defaults(func=pull_project)
plan_parser.set_defaults(func=plan_project)
apply_parser.set_defaults(func=apply_project)

args = parser.parse_args()
if args.command:
    loop = asyncio.get_event_loop()
    if asyncio.iscoroutinefunction(args.func):
        loop.run_until_complete(args.func())
    else:
        args.func()
