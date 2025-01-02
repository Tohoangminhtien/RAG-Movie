from langchain.chains.base import Chain
from underthesea import ner

# 1. Class 1: NER Chain


class NameEntityRecognition(Chain):

    @property
    def input_keys(self):
        return ["question"]

    @property
    def output_keys(self):
        return ["ner", "history"]

    def named_entity_recognition(self, text) -> list:
        entities = ner(text)
        person = ' '.join(
            [entity[0] for entity in entities if entity[3] in ['B-PER', 'I-PER']])
        location = ' '.join(
            [entity[0] for entity in entities if entity[3] in ['B-LOC', 'I-LOC']])
        organization = ' '.join(
            [entity[0] for entity in entities if entity[3] in ['B-ORG', 'I-ORG']])
        name = []
        for i in [person, location, organization]:
            if i != '':
                name.append(i)
        return name

    def _call(self, inputs: dict) -> dict:
        name = self.named_entity_recognition(inputs["question"])
        print('> Entering new Extract Chains...')
        print(f'{inputs["question"]} -> Extract -> {name}')
        print('\n')
        
        return {"ner": name, "history": inputs["question"]}
