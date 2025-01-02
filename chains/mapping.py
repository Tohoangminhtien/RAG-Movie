from langchain.chains.base import Chain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
# 1. Class 2: Classify Chain


class LLMClassify(Chain):
    llm: ChatOpenAI
    prompt: PromptTemplate

    @property
    def input_keys(self):
        return ["ner", "history"]

    @property
    def output_keys(self):
        return ["classify", "history"]

    def _call(self, inputs: dict) -> dict:
        ner = inputs['ner']
        prompt_text = self.prompt.format(question=ner)
        text = self.llm.invoke(prompt_text).content
        print('> Entering new Mapping Chains...')
        print(f'{ner} -> Mapping -> {text}')
        print('\n')
        return {"classify": text, "history": inputs['history']}
