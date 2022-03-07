
from curiosity_builder import Curiosity_Builder
from curiosity_dataset import Curiosity_Dataset
from curiosity_handler import Curiosity_Handler

from general_utils import Curiosity_Type

def recipe():
    curiosity_dataset_path = 'dataset/recipes_dataset'
    curiosity_dataset = Curiosity_Dataset(curiosity_dataset_path, Curiosity_Type.RECIPE)
    curiosity_handler = Curiosity_Handler(curiosity_dataset)
    keywords = ['salad', 'bacon']
    curiosity_sentence = curiosity_handler.fetch_any_phrase(keywords)
    curiosity = curiosity_handler.build_curiosity(curiosity_sentence)
    return curiosity

def main():
    curiosity_builder = Curiosity_Builder()
    curiosity_builder.build_dataset()
    curiosity = recipe()
    print('======= Curiosity ========')
    print(curiosity)
    print('==========================')


if __name__ == '__main__':
    main()