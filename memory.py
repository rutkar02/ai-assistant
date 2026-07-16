from config import TOP_K,Embedding_Model
from chroma_db import memory_collection
from model import call_model
import uuid

def create_embedding(text,client):
    response = client.embeddings.create(model=Embedding_Model, input=text)
    return response.data[0].embedding

def retrieve_memory(question,client):
    question_embedding = create_embedding(question,client)
    result = memory_collection.query(
        query_embeddings=[question_embedding],
        n_results=TOP_K
    )
    return result["documents"][0]

def judge_memory(message,client):
    prompt = f"""
    You are an excellent memory judge whose job is to determine whether the user's message contains
    long term information which would be useful in future conversation.
   
    User message:
    {message}
    Return only one word
    Yes 
    or
    No

"""
    value = call_model(prompt,None,None,client)
    if value.output_text.lower().strip() == "yes":
        return True
    else:
        return False


def extract_memory(message,client):
    prompt = f"""
    extract user's text as user's info like label them as texts related to user

    Examples:
    "I am Rutkar"
    the user's name is rutkar

    "I live in banglore"
    the user lives in banglore

    User Text:
    {message}

    Return only the extracted memory.
    Do not explain anything.
    """
    response = call_model(prompt,None,None,client)
    return response.output_text.strip()

def save_memory(message):
    unique_id = str(uuid.uuid4())
    memory_collection.add(
        documents=[message],
        ids=[unique_id]
    )