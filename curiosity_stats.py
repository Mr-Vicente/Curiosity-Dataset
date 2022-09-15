
#############################
#   Imports and Contants
#############################

# Python modules
from typing import List
from enum import Enum

# Remote modules
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Local modules
import utils
from curiosity_dataset import Curiosity_Dataset
from utils import Curiosity_Type

#############################
#           Stuff
#############################

class STATS_OPERATION(Enum):
    MEAN = 0
    MEDIAN = 1

class SENTENCE_LENGTH(Enum):
    CHARACTER = 0
    WORD = 1

class Curiosity_Stats:
    def __init__(self, curiosities, tags):
        self.curiosities: List[str] = curiosities
        self.tags: List[List[str]] = tags

    def size_of_curiosity(self, length_type:SENTENCE_LENGTH, curiosity:str):
        if  length_type==SENTENCE_LENGTH.CHARACTER:
            size_of_curiosity = lambda c: len(c)
        elif length_type==SENTENCE_LENGTH.WORD:
            size_of_curiosity = lambda c: len(c.split(' '))
        else:
            size_of_curiosity = lambda c: len(c)
        return size_of_curiosity(curiosity)

    def stats_operation(self, op:STATS_OPERATION, li:List):
        if op == STATS_OPERATION.MEAN:
            operation = lambda l: np.mean(l)
        elif op==STATS_OPERATION.MEDIAN:
            operation = lambda l: np.median(l)
        else:
            operation = lambda l: np.mean(l)
        return operation(li)

    def obtain_stats_length_of_curiosities(self, length_type:SENTENCE_LENGTH, op:STATS_OPERATION):
        """
        :param length_type:     length_type==0 -> sentence length by characters
                                length_type==1 -> sentence length by words
        :return: int (mean length)
        """

        total_size = []
        for curiosity in self.curiosities:
            total_size.append(self.size_of_curiosity(length_type, curiosity))

        value = self.stats_operation(op, total_size)
        return value

    def create_simple_curiosity_length_dataframe(self, length_type: SENTENCE_LENGTH):
        total_size = []
        for curiosity in self.curiosities:
            total_size.append(self.size_of_curiosity(length_type, curiosity))
        df = pd.DataFrame({
            'recipes': total_size
        })
        return df

    def draw_stats(self):
        sns.set_theme(style="whitegrid")
        df = self.create_simple_curiosity_length_dataframe(SENTENCE_LENGTH.WORD)
        self.create_phrase_length_violin_plot(df)

    @classmethod
    def create_phrase_length_violin_plot(cls, df: pd.DataFrame):
        ax = sns.violinplot(y=df['len'], inner="quartile")
        plt.savefig("stats/curiosities_length_destribution.png",
                    format='png', dpi=150)

    @classmethod
    def create_mixture_phrase_length_violin_plot(cls, df: pd.DataFrame):
        store_dir = './stats'
        utils.create_directory(store_dir)
        plt.title('Curiosities Length Per Domain Area')
        ax = sns.violinplot(x=df['Curiosity Type'], y=df['Length (Nºwords)'], inner="quartile", scale="count")
        plt.savefig(f"{store_dir}/curiosities_length_destribution.png",
                    format='png', dpi=150)

    @classmethod
    def create_mixed_curiosity_length_dataframe(cls, length_type: SENTENCE_LENGTH,
                                                recipes_curiosities: List[str],
                                                diy_curiosities: List[str]):
        recipes_curios_lenght, diy_curios_length = [], []
        for curiosity in recipes_curiosities:
            recipes_curios_lenght.append(('Recipe',
                                          cls.size_of_curiosity(cls,length_type, curiosity)))
        for curiosity in diy_curiosities:
            diy_curios_length.append(('DIY',
                                      cls.size_of_curiosity(cls, length_type, curiosity)))
        total = recipes_curios_lenght + diy_curios_length
        df = pd.DataFrame({
            'Curiosity Type': [t[0] for t in total],
            'Length (Nºwords)': [t[1] for t in total]
        })
        return df

    @classmethod
    def general_draw_stats(cls, r_curios, d_curios):
        #sns.set_theme(style="whitegrid")
        sns.set_theme()
        df = cls.create_mixed_curiosity_length_dataframe(SENTENCE_LENGTH.WORD, r_curios, d_curios)
        cls.create_mixture_phrase_length_violin_plot(df)


if __name__ == '__main__':
    curiosity_dataset_path = 'dataset/recipes_dataset'
    curiosity_dataset = Curiosity_Dataset(curiosity_dataset_path, Curiosity_Type.RECIPE)
    c_recipes_stats = Curiosity_Stats(curiosity_dataset.curiosity_phrases, curiosity_dataset.curiosity_categories)

    cuisine_dataset_size = curiosity_dataset.get_number_of_phrases()

    print('[Recipe] dataset size: ', cuisine_dataset_size)

    print('[Recipe] Char mean size: ', c_recipes_stats.obtain_stats_length_of_curiosities(SENTENCE_LENGTH.CHARACTER,
                                                                                  STATS_OPERATION.MEAN))
    print('[Recipe] Word mean size: ', c_recipes_stats.obtain_stats_length_of_curiosities(SENTENCE_LENGTH.WORD,
                                                                                  STATS_OPERATION.MEAN))

    print('[Recipe] Char median size: ', c_recipes_stats.obtain_stats_length_of_curiosities(SENTENCE_LENGTH.CHARACTER,
                                                                                    STATS_OPERATION.MEDIAN))
    print('[Recipe] Word median size: ', c_recipes_stats.obtain_stats_length_of_curiosities(SENTENCE_LENGTH.WORD,
                                                                                    STATS_OPERATION.MEDIAN))

    #c_recipes_stats.draw_stats()

    curiosity_dataset_path = 'dataset/diys_dataset'
    curiosity_dataset = Curiosity_Dataset(curiosity_dataset_path, Curiosity_Type.DIY)
    c_diys_stats = Curiosity_Stats(curiosity_dataset.curiosity_phrases, curiosity_dataset.curiosity_categories)

    print('\n=======================\n')

    wikihow_dataset_size = curiosity_dataset.get_number_of_phrases()

    print('[Wikihow] dataset size: ', wikihow_dataset_size)

    print('[Wikihow] Char mean size: ', c_diys_stats.obtain_stats_length_of_curiosities(SENTENCE_LENGTH.CHARACTER,
                                                                                  STATS_OPERATION.MEAN))
    print('[Wikihow] Word mean size: ', c_diys_stats.obtain_stats_length_of_curiosities(SENTENCE_LENGTH.WORD,
                                                                                  STATS_OPERATION.MEAN))

    print('[Wikihow] Char median size: ', c_diys_stats.obtain_stats_length_of_curiosities(SENTENCE_LENGTH.CHARACTER,
                                                                                    STATS_OPERATION.MEDIAN))
    print('[Wikihow] Word median size: ', c_diys_stats.obtain_stats_length_of_curiosities(SENTENCE_LENGTH.WORD,
                                                                                    STATS_OPERATION.MEDIAN))

    total_dataset_size = cuisine_dataset_size + wikihow_dataset_size
    print('\n[Total] dataset size: ', total_dataset_size)

    Curiosity_Stats.general_draw_stats(c_recipes_stats.curiosities, c_diys_stats.curiosities)

