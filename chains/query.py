from langchain.chains.base import Chain
from langchain_openai import ChatOpenAI
from langchain.chains import GraphCypherQAChain
import textwrap
# 1. Class 4: NER Chain


class GraphCypherQA(Chain):
    llm: GraphCypherQAChain

    @property
    def input_keys(self):
        return ["exact_question"]

    @property
    def output_keys(self):
        return ["answer"]

    def _call(self, inputs: dict) -> dict:
        answer = self.llm.invoke(inputs['exact_question'])
        return {"answer": answer['result']}
