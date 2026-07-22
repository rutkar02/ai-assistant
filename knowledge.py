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


def ingest_text(text,metadata,client):
    document_name = metadata["document_name"]
    chunks = create_chunks(text,Chunk_Size)
    embeddings = []
    documents = []
    ids = []

    for i, chunk in enumerate(chunks, start = 1):  # starts i from 1
        embedding = create_embedding(chunk,client)
        embeddings.append(embedding)
        documents.append(chunk)
        ids.append(f"{document_name}_{i}")
        i+=1

    knowledge_collection.add(
        ids = ids,
        documents=documents,
        embeddings=embeddings,
        metadatas= [{"document_name":document_name} for _ in range(len(documents))]
    )
    return f"""
    Stored {document_name}
    {len(chunks)} chunks
    {len(embeddings)} embeddings
    Knowledge base updated
    """

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text+=page_text + "\n"
    return text        

def ingest_document(pdf_path,client):
    text = extract_text_from_pdf(pdf_path)
    return ingest_text(
        text=text,
        metadata={"document_name": Path(pdf_path).stem},
        client = client)
    
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
    return text

def delete_document():
    pass
def list_documents():
    pass