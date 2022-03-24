
from utils import read_json_file_2_dict, Curiosity_Type
from typing import List, Dict

class Curiosity_Dataset:
    def __init__(self, curiosity_data_path: str, curiosity_type: Curiosity_Type):
        assert curiosity_data_path is not None
        assert curiosity_type is not None
        self.curiosity_data = read_json_file_2_dict(curiosity_data_path)
        self.curiosity_type = curiosity_type

        self.curiosity_phrases = self.curiosity_data.get('curiosity_phrases', [])
        self.curiosity_categories = self.curiosity_data.get('curiosity_tags', [])
        self.curiosity_len_phrases = self.curiosity_data.get('curiosity_len_phrases', [])
        self.keyword_2_curiosityId: Dict[str, List[int]] = self.curiosity_data.get('keyword_2_curiosityId', {})

    def get_number_of_phrases(self) -> int:
        return len(self.curiosity_phrases)

    def get_available_categories(self) -> List[str]:
        return list(self.keyword_2_curiosityId.keys())

