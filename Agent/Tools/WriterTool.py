from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI


def write(query: str, verbose=False):
    """Write a document according to user requirements."""
    template = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "You are a professional document writer. You write a document based on client requests. "),
            HumanMessagePromptTemplate.from_template("{query}"),
        ]
    )

    chain = {"query": RunnablePassthrough()} | template | ChatOpenAI() | StrOutputParser()

    return chain.invoke(query)


if __name__ == "__main__":
    print(write("Write an email to James with the content: Hello, I am James II"))
