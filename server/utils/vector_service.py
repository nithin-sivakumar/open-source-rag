from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from core.config import settings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# vector_store = InMemoryVectorStore(embeddings)
client = MongoClient(settings.MONGODB_URL)

collection = client["rag-test"]["test"]

vector_store = MongoDBAtlasVectorSearch(collection=collection, embedding=embeddings)
