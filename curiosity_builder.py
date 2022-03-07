#############################
#   Imports
#############################

# Python modules
import os

# Remote modules

# Local modules
from general_utils import (read_json_file_2_dict,
                        write_dict_2_json_file,
                       Curiosity_Type)

#############################
#   Constants
#############################

SEPERATION_TOKEN = '<sep>'

#############################
#   Stuff
#############################

class Curiosity_Builder:
    def __init__(self, seperation_token: str = SEPERATION_TOKEN):
        self.seperation_token = seperation_token

    def load_curiosity_files(self,
            recipe_curiosity_dir: str   ="dataset/recipe",
            diy_curiosity_dir: str      ="dataset/diy"
            ):
        recipes_curiosities = self.load_data(recipe_curiosity_dir)
        diys_curiosities = self.load_data(diy_curiosity_dir)
        return (recipes_curiosities, Curiosity_Type.RECIPE),\
                (diys_curiosities, Curiosity_Type.DIY)

    def load_unwanted_curiosities (self,
               filter_out_recipe_curiosity_dir: str = "dataset/filter_out_recipe",
               filter_out_diy_curiosity_dir: str = "dataset/filter_out_diy"
            ):
        unwanted_recipes_curiosities = self.load_unwanted_data(filter_out_recipe_curiosity_dir)
        unwanted_diys_curiosities = self.load_unwanted_data(filter_out_diy_curiosity_dir)
        return unwanted_recipes_curiosities, unwanted_diys_curiosities

    def _extract_data_of_dataset(self, dataset):
        return dataset.split('\n\n')[:-1]

    def load_data(self, curiosity_dir:str):
        curiosity_dataset_lines = []
        for curiosity_filename in os.listdir(curiosity_dir):
            with open(f'{curiosity_dir}/{curiosity_filename}') as f:
                dataset_text = f.read()
                curiosity_lines = self._extract_data_of_dataset(dataset_text)
                curiosity_dataset_lines.extend(curiosity_lines)
        return curiosity_dataset_lines

    def load_unwanted_data(self, curiosity_dir:str):
        unwanted_dataset_lines = []
        for curiosity_filename in os.listdir(curiosity_dir):
            with open(f'{curiosity_dir}/{curiosity_filename}') as f:
                unwanted_dataset_lines.extend([c.replace('\n','') for c in f.readlines()])
        return unwanted_dataset_lines

    def _process_line(self, curiosity_line):
        curiosity = curiosity_line.split(self.seperation_token)
        curiosity_phrase = curiosity[0]
        categories = curiosity[1:]
        return curiosity_phrase, categories

    def _process_categories(self, curiosity, index, categories):
        for category in categories:
            category_phrases_id = curiosity.get(category, [])
            category_phrases_id.append(index)
            curiosity[category] = category_phrases_id

    def _categories_tranformer(self, curiosity_info, categories):
        new_categories = []
        if categories == ['']:
            return ['ALL'], 'ALL'
        print(categories)
        for category in categories:
            # Normal category
            if category[0] != SEPERATION_TOKEN[0] and category[-1] != SEPERATION_TOKEN[-1]:
                new_categories.append(category)
                continue
            # Special category
            cat = category[1:-1]
            category_keywords = cat.split(' ')
            print(category_keywords)
            binding = {}
            for keyword in category_keywords:
                obj = binding.get(keyword, curiosity_info.get(keyword))
                if isinstance(obj, dict):
                    binding = obj
                else:
                    print("obj: ", obj)
                    assert isinstance(obj, list), 'should be list!'
                    storing_category = cat.replace('_', ' ').strip()
                    obj.append(storing_category)
                    new_categories.extend(obj)
        new_categories = set(new_categories)
        categories_in_text = f'{SEPERATION_TOKEN}'.join(new_categories)
        return new_categories, categories_in_text

    def map_curiosity_2_dict(self, curiosity_lines:[str], curiosity_type: Curiosity_Type):
        curiosity_phrases, curiosity_len_phrases, curiosity_tags = [], [], []
        curiosity = {}
        curiosity_info_filename = f"{curiosity_type.value}s_info"
        curiosity_dict = read_json_file_2_dict(filename=curiosity_info_filename, store_dir='./dataset')
        for index, curiosity_line in enumerate(curiosity_lines):
            curiosity_phrase, categories = self._process_line(curiosity_line)
            print(curiosity_phrase)
            categories, _ = self._categories_tranformer(curiosity_dict, categories)
            self._process_categories(curiosity, index, categories)
            curiosity_phrases.append(curiosity_phrase)
            curiosity_tags.append(list(categories))
            curiosity_len_phrases.append(len(curiosity_phrase.split()))
        return curiosity_phrases, curiosity_tags, curiosity_len_phrases, curiosity

    def filter_wanted_curiosities(self, curiosity_lines, unwanted_curiosities):
        return [curio_line for curio_line in curiosity_lines
                if self._process_line(curio_line)[0] not in unwanted_curiosities]

    def build_dataset(self,
                      recipe_curiosity_dir: str = "dataset/recipe",
                      diy_curiosity_dir: str = "dataset/diy",
                      filter_out_recipe_curiosity_dir: str = "dataset/filter_out_recipe",
                      filter_out_diy_curiosity_dir: str = "dataset/filter_out_diy"
                      ):
        set_curiosities = self.load_curiosity_files(recipe_curiosity_dir, diy_curiosity_dir)
        unwanted_curiosities = self.load_unwanted_curiosities(filter_out_recipe_curiosity_dir,
                                                             filter_out_diy_curiosity_dir)
        for curiosity_data, unwanted_curiosity_data in zip(set_curiosities,unwanted_curiosities):
            curiosities, curiosities_type = curiosity_data
            curiosities = self.filter_wanted_curiosities(curiosities, unwanted_curiosity_data)
            curiosity_phrases, curiosity_tags, curiosity_len_phrases, curiosity = self.map_curiosity_2_dict(curiosities, curiosities_type)
            self.store_in_json(curiosity_phrases, curiosity_tags, curiosity_len_phrases, curiosity, curiosities_type)

    def store_in_json(self, curiosity_phrases,
                      curiosity_tags,
                      curiosity_len_phrases,
                      curiosity,
                      curiosities_type,
                      store_dir='./dataset',
                      filename=None):
        dataset = {
            'curiosity_phrases': curiosity_phrases,
            'curiosity_tags': curiosity_tags,
            'curiosity_len_phrases': curiosity_len_phrases,
            'keyword_2_curiosityId': curiosity
        }
        if filename is None:
            filename = f'{curiosities_type.value}s_dataset'
        write_dict_2_json_file(json_object=dataset, filename=filename, store_dir=store_dir)

    @staticmethod
    def store_dataset_format_2_standard_csv(curiosity_filename='dataset/recipe/curiosity_recipes_data.txt'):
        with open(curiosity_filename) as f_in:
            text = f_in.read()
            text = text.replace('<sep>', ',')
            text = text.replace('\n\n', '\n')
            with open(curiosity_filename[:-4] + '.csv', 'w') as f_out:
                f_out.write(text)

