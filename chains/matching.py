from langchain.chains.base import Chain
from rapidfuzz import process, fuzz
from pathlib import Path
import json
import pickle
# 1. Class 3: Matching Chain


class FuzzyMatching(Chain):

    @property
    def input_keys(self):
        return ["classify", "history"]

    @property
    def output_keys(self):
        return ["exact_question"]

    def fuzzy_search(self, query: dict) -> dict:
        # Can toi uu
        path = Path(__file__).resolve().parent.parent / \
            'metadata' / 'my_dict.pkl'
        with open(path, 'rb') as f:
            loaded_dict = pickle.load(f)
        dictionary = loaded_dict

        nodes = query.keys()
        new_query = {}
        for node in nodes:
            retrieval = process.extract(
                query[node], dictionary[node], scorer=fuzz.ratio, limit=1)
            new_query[node] = retrieval[0][0]
        return new_query

    def _call(self, inputs: dict) -> dict:
        str_data = inputs['classify']
        history = inputs['history']

        query_data = json.loads(str_data)
        exact_name = self.fuzzy_search(query_data)

        for k in exact_name.keys():
            history = history.replace(query_data[k], exact_name[k])

        print('> Entering new Matching Chains...')
        print(f'{str_data} -> Matching -> {exact_name}')
        print('\n')
        return {"exact_question": history}
