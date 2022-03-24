#############################
#   Imports and Contants    #
#############################

# Python modules
from enum import Enum
import os
import json

class Curiosity_Type(Enum):
    DIY = 'diy'
    RECIPE = 'recipe'


#############################
#   Files Managment         #
#############################

def create_directory(output_dir):
    # Create output directory if needed
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except FileExistsError as _:
            return


def write_dict_2_json_file(json_object, filename, store_dir='.'):
    create_directory(store_dir)
    with open(f'{store_dir}/{filename}.json', 'w', encoding='utf-8') as file:
        json.dump(json_object, file, ensure_ascii=False, indent=4)


def read_json_file_2_dict(filename, store_dir='.'):
    with open(f'{store_dir}/{filename}.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def read_jsonl_file_2_dict(filename, store_dir='.'):
    recipes = []
    with open(f'{store_dir}/{filename}.jsonl', 'r', encoding='utf-8') as file:
        for line in file:
            recipes.append(json.loads(line))
        return recipes
