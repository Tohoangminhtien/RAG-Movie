# 1. Import thư việnviện
import warnings
from langchain.chains import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate
from langchain_community.graphs import Neo4jGraph
import textwrap
import openai
import os
from dotenv import load_dotenv
import streamlit as st
from chains.extract import NameEntityRecognition
from chains.mapping import LLMClassify
from chains.matching import FuzzyMatching
from chains.query import GraphCypherQA
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate


class ChatbotAI:

    def __init__(self, open_ai_key, neo4j_url, user_name, password, database):
        llm = ChatOpenAI(temperature=0, openai_api_key=open_ai_key,
                         model='gpt-4o-mini')
        llm_prompt = self.load_prompt('prompt/mapping.txt')
        prompt = PromptTemplate(
            input_variables=["question"], template=llm_prompt)

        self.chain1 = NameEntityRecognition()
        self.chain2 = LLMClassify(llm=llm, prompt=prompt)
        self.chain3 = FuzzyMatching()

        CYPHER_GENERATION_TEMPLATE = self.load_prompt('prompt/query.txt')

        CYPHER_GENERATION_PROMPT = PromptTemplate(
            input_variables=["schema", "question"],
            template=CYPHER_GENERATION_TEMPLATE
        )

        kg = Neo4jGraph(
            url=neo4j_url,
            username=user_name,
            password=password,
            database=database
        )

        cypherChain = GraphCypherQAChain.from_llm(
            llm,
            graph=kg,
            verbose=True,
            cypher_prompt=CYPHER_GENERATION_PROMPT,
            allow_dangerous_requests=True
        )

        self.chain4 = GraphCypherQA(llm=cypherChain)

    def load_prompt(self, file_path) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            template = file.read()
        return template

    def chat(self, question: str):
        pipeline = self.chain1 | self.chain2 | self.chain3 | self.chain4
        result = pipeline.invoke({'question': question})
        return result['answer']
