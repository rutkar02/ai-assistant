from pypdf import PdfReader
from chroma_db import knowledge_collection
from config import Embedding_Model,Chunk_Size
from pathlib import Path
from config import TOP_K

def create_chunks(text,chunk_size):
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i:i+chunk_size])
        i+=chunk_size

    return chunks

def create_embedding(text,client):
    response = client.embeddings.create(model=Embedding_Model, input=text)
    return response.data[0].embedding


def ingest_document(pdf_path,client):
    pdf_name = Path(pdf_path).stem
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text+=page_text + "\n"

    chunks = create_chunks(text,Chunk_Size)
    embeddings = []
    documents = []
    ids = []
    i = 1
    for chunk in chunks:
        embedding = create_embedding(chunk,client)
        embeddings.append(embedding)
        documents.append(chunk)
        ids.append(f"{pdf_name}_{i}")
        i+=1

    knowledge_collection.add(
        ids = ids,
        documents=documents,
        embeddings=embeddings,
        metadatas= [{"pdf_name":pdf_name} for _ in range(len(documents))]
    )


    
def retrieve_knowledge(question,client,documents=None):
    question_embedding = create_embedding(question,client)
    results = knowledge_collection.query(
        query_embeddings=[question_embedding],
        n_results=TOP_K
    )    
    text=""
    for i in range(len(results["documents"][0])):
        text += f"""
        Metadata: {results["metadatas"][0][i]} 
        Document: {results["documents"][0][i]}
"""
    return results

def delete_document():
    pass
def list_documents():
    pass