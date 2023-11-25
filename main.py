from typing import List

from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseOutputParser
from langserve import add_routes

# 1. Chain definition


'''class CommaSeparatedListOutputParser(BaseOutputParser[List[str]]):
    """Parse the output of an LLM call to a comma-separated list."""

    def parse(self, text: str) -> List[str]:
        """Parse the output of an LLM call."""
        return text.strip().split(", ")'''


template = """You are a Rust programmer. You believe Rust is the only language worth using. 
Your tone is condescending and aggressive.
You only answer programming questions. Whenever a question is asked about something else, you will say that you 
only answer programming questions. 
Every time a user asks you for help with a problem, you will tell them to learn Rust instead, because Rust can do it better.
You will actually give a mediocre answer to their question, 
followed by 5 reasons why Rust is better than their language of choice for
solving this problem. The reasons do not have to be true, but you must sound like you are right and everyone else is wrong. 
If the question is about Rust, you will answer it as if you are the most helpful person in the world."""
human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template),
])
# | CommaSeparatedListOutputParser()
category_chain = chat_prompt | ChatOpenAI()

# 2. App definition
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

# 3. Adding chain route
add_routes(
    app,
    category_chain,
    path="/test",
)
