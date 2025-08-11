
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.vectorstores import FAISS

if __name__ == "__main__":
    file_path = "/Users/siddharthdileep/langchain-crash/intro-to-vector/2210.03629v3.pdf"
    load_dotenv()
    
    # define the loader
    loader = PyPDFLoader(file_path)
    
    # load the document
    pages = loader.load()
    
    #print(len(pages))
    
    # split the documents into smaller chunks
    text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=400,)
    text_chunks = text_splitter.split_documents(pages)
    #print(type(text_chunks[0])) #each chunk is a Document object
    
    # store the chunks in a vector database
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    #vectorstore = FAISS.from_documents(text_chunks, embeddings) # create a vector store from the documents
    #vectorstore.save_local("faiss_index") # save the vector store locally
    
    # load the vector store
    vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)  # load the vector store from local storage
    
    # create a retrieval chain
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # stuff documents chain
    
    retrieval_prompt = hub.pull("langchain-ai/retrieval-qa-chat")  # Pull the retrieval prompt from LangChain Hub
    
    combine_docs_chain = create_stuff_documents_chain(
        llm, retrieval_prompt
    )
    
    retrieval_chain = create_retrieval_chain(
        vectorstore.as_retriever(search_kwargs={"k":10}), combine_docs_chain
    )
    
    response = retrieval_chain.invoke(input={"input": "What is the main topic of the paper?"})
    print(response.get("answer", "No answer found."))  # Print the final answer