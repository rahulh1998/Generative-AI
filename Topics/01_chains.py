from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# loading the model
model = ChatOllama(model = 'gemma4:e2b')

# creating the prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert in the field of AI. Answer only if the question belongs to the field of AI and nothing else. If out of scope generate out of scope"),
        ("human", "Explain the {topic}")
    ]
)

chain = prompt | model | StrOutputParser()

response = chain.invoke({'topic':'Skills & MCP in agentic ai'})

print(response)