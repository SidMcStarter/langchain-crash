import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
if __name__ == "__main__":
    load_dotenv()
    loader = TextLoader("/Users/siddharthdileep/langchain-crash/intro-to-vector/vector_database_full.txt")
    document = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separator="\n\n")
    texts = text_splitter.split_documents(document)
    print(f"Number of chunks: {len(texts)}")
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"), model="text-embedding-3-small")
    # pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_index_name = os.getenv("INDEX_NAME")
    
    # create pinecone instance
    print("Adding to pinecone instance...")
    # Create PineconeVectorStore instance
    vectorstore = PineconeVectorStore(
        embedding=embeddings,
        index_name=pinecone_index_name
    )

    # Add documents
    vectorstore.add_documents(texts)    
    print("Documents added to Pinecone index successfully.")
