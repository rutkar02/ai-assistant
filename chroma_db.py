import chromadb

chroma_client = chromadb.Client()
memory_collection = chroma_client.get_or_create_collection("memory_collection")
knowledge_collection = chroma_client.get_or_create_collection("knowledge_collection")

def storing_data():
    pass