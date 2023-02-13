import os
import json
import sys

from InquirerPy import inquirer
from InquirerPy.utils import patched_print
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from InquirerPy.validator import EmptyInputValidator, NumberValidator, PathValidator


BASEDIR = os.path.abspath(os.path.dirname(__file__))
symbols = [
    "!",
    "@",
    "#",
    "$",
    "%",
    "&",
    "*",
    "+",
    "=",
    "?",
    ":",
    ";",
    Separator(),
    Choice(name="Exit", value=False)
]


def new_config():
    config_dict = {}
    prefix_decision = inquirer.select(
        message="Select a prefix character for bot commands >>> ",
        choices=symbols
    ).execute()
    
    if not prefix_decision:
        sys.exit("Quitting...")
        
    config_dict['prefix'] = prefix_decision
    
    token_input = inquirer.text(
        message="Copy and paste your bot's secret token here >>> "
    ).execute()
    
    config_dict['token'] = token_input
    
    perm_int = inquirer.number(
        message="Enter the permissions integer your bot requires >>> ",
        min_allowed=0,
        max_allowed=10,
        validate=EmptyInputValidator(),
        invalid_message="Cannot be empty!"
    ).execute()
    
    config_dict['permissions'] = perm_int
    
    app_id_input = inquirer.text(
        message="Copy and paste your application's ID here >>> ",
        validate=NumberValidator(),
        invalid_message="Application ID should be a long string of numbers!"
    ).execute()
    
    config_dict['application_id'] = app_id_input
    
    sync_globally = False
    
    sync_globally = inquirer.confirm(
        message="Sync commands globally?",
        default=True
    ).execute()
    
    config_dict['sync_commands_globally'] = sync_globally
    
    owners = []
    adding = True
    while adding:
        owner_id_input = inquirer.text(
            message="Copy and paste user IDs of bot owners >>> ",
            validate=NumberValidator(),
            invalid_message="Invalid user id!"
        ).execute()
        
        owners.append(owner_id_input)
        
        adding = inquirer.confirm(
            message="Continue adding to owner's list?",
            default=True
        ).execute()
    config_dict['owners'] = owners
    
    destination_path = inquirer.filepath(
        message="Enter destination path to save config.json file to >>> ",
        default=os.path.join(BASEDIR, 'config.json'),
        validate=PathValidator(message="Input is not a path!")
    ).execute()
    
    if not os.path.isfile(destination_path):
        destination_path = os.path.join(destination_path, 'config.json')
        
    if not destination_path.endswith(".json"):
        filename = destination_path.split("/")[-1]
        without_ext = filename.split(".")[-2]
        new_filename = ".".join(without_ext, 'json')
        destination_path = destination_path.split("/")
        destination_path[-1] = new_filename
        destination_path[0] = "/" + destination_path[0]
        destination_path = "/".join(destination_path)
    
    with open(destination_path, 'w') as file:
        file.write(json.dumps(config_dict))
        
    return config_dict
    
    
def prompt_for_path():
    file_path = inquirer.filepath(
        message="Enter path to config.json file >>> ",
        validate=PathValidator(is_file=True, message="Input is not a path to a file."),
        only_files=True
    ).execute()
    
    return file_path
