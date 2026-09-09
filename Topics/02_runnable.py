from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableParallel, RunnablePassthrough
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser

# loading the model
model = ChatOllama(model = 'gemma4:e2b')

# Creating the parser
parser = StrOutputParser()

# Runnable branches options

choice1 = RunnableLambda(lambda x : f"Generate the summary for the topic {x['topic']}")
choice2 = RunnableLambda(lambda x : f"Answer the question for the topic {x['topic']}")


branch = RunnableParallel(
    first = RunnablePassthrough(),
    second = RunnableBranch(
        (
            lambda x: x['type'] =='summary',
            choice1,
        ),  
        choice2,)
    )

chain = branch | RunnableLambda(lambda x: x['second']) | model | parser

response = chain.invoke({
    'type': 'summary',
    'topic': 'AI Agent Calling '
})

print(response)