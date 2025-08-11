import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain import hub
from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from langchain_core.runnables import (
    RunnablePassthrough,
)

load_dotenv()

def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])
if __name__=="__main__":
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=os.getenv("OPENAI_API_KEY"))
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    pinecone_index_name = os.getenv("INDEX_NAME")
    # Create PineconeVectorStore instance
    vectorstore = PineconeVectorStore(
        embedding=embeddings,
        index_name=pinecone_index_name,
    )
    
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")  # Pull the retrieval prompt from LangChain Hub
    
    combine_docs_chain = create_stuff_documents_chain(
    llm, retrieval_qa_chat_prompt
    ) 
    
    retrieval_chain = create_retrieval_chain(vectorstore.as_retriever(), combine_docs_chain) #retrieves the documents and combines them in the prompt
    query = "What is the vector database?"
    
    # result = retrieval_chain.invoke(input={"input": query})
    
    # print(result.get("answer", "No answer found."))  # Print the final answer

    template = """
    Use the following pieces of context to answer the question at the end. If you don't know the answer, 
    just say that you don't know, don't try to make up an answer.
    Use three sentences to answer the question and keep the answer concise.
    Always say thank you at the end of your answer.
    
    Context:
    {context}
    
    Question: {question}
    
    Helpful Answer:
    """
    
    custom_prompt = PromptTemplate.from_template(template=template)
    
    rag_chain = {"question": RunnablePassthrough(), "context": vectorstore.as_retriever() | format_docs} |custom_prompt | llm
    
    response = rag_chain.invoke("What is vector database?")
    print(response.content)     
    
