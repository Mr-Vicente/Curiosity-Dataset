
import random
from general_utils import read_json_file_2_dict

from collections import Counter
from enum import Enum

class Sentence_Type(Enum):
    SHORTEST = 'shortest'
    GENERAL = 'general'

class Curiosity_Handler:
    def __init__(self, curiosity_dataset):
        self.curiosity_config = read_json_file_2_dict('curiosity_config')
        self.curiosity_dataset = curiosity_dataset
        self.curiosity_type = curiosity_dataset.curiosity_type

        self.curiosity_phrases = self.curiosity_dataset.curiosity_phrases
        self.curiosity_len_phrases = self.curiosity_dataset.curiosity_len_phrases
        self.keyword_2_curiosityId = self.curiosity_dataset.keyword_2_curiosityId

    def fetch_shortest_phrase(self, keywords):
        return self.fetch_phrase_based_on_criteria(keywords, Sentence_Type.SHORTEST)

    def fetch_any_phrase(self, keywords):
        return self.fetch_phrase_based_on_criteria(keywords, Sentence_Type.GENERAL)

    def fetch_phrase_based_on_criteria(self, keywords, s_type: Sentence_Type):
        if s_type == Sentence_Type.SHORTEST:
            return self._get_phrase_from_best_category(self.keyword_2_curiosityId,
                                                       self.curiosity_phrases,
                                                       self.curiosity_len_phrases,
                                                       keywords)
        elif s_type == Sentence_Type.GENERAL:
            return self._get_any_phrase_from_keywords(self.keyword_2_curiosityId,
                                                       self.curiosity_phrases,
                                                       keywords)

    def _get_phrase(self, curiosity, curiosity_phrases, category):
        phrases_idx = curiosity.get(category, [])
        if not phrases_idx:
            return ""
        phrase_idx = random.sample(phrases_idx, 1)[0]
        return curiosity_phrases[phrase_idx]

    def _get_phrase_from_best_category(self, curiosity, curiosity_phrases,
                                       phrases_len, keywords):
        temp = {}
        for keyword in keywords:
            phrases_idx = curiosity.get(keyword, [])
            if not phrases_idx:
                return ""
            phrase_idx = random.sample(phrases_idx, 1)[0]
            temp[phrase_idx] = phrases_len[phrase_idx]
        idx = min(temp, key=temp.get)
        return curiosity_phrases[idx]

    def _get_any_phrase_from_keywords(self, curiosity, curiosity_phrases, keywords):
        temp = []
        for keyword in keywords:
            phrases_idx = curiosity.get(keyword, [])
            if not phrases_idx:
                return ""
            temp.extend(phrases_idx)
        phrase_idx = random.sample(temp, 1)[0]
        return curiosity_phrases[phrase_idx]

    def build_curiosity(self, curiosity_sentence, intro_curiosity=None):
        curiosity_starters = self.curiosity_config.get("starters", [])
        if not intro_curiosity:
            intro_curiosity = random.sample(curiosity_starters, 1)[0]
        return f'{intro_curiosity}{curiosity_sentence}'