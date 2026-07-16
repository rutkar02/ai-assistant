from knowledge import list_documents,delete_document,ingest_document
from config import Target_Words

def execute_command(command,client):
    if "upload" in command:
        ingest_document(command.split(maxsplit=1)[1],client)
    elif "list" in command:
        list_documents()   
    elif "delete" in command:
         delete_document(command.split(maxsplit=1)[1])     

# ingest_document(command.split("upload")[1],client) is dangerous 
# coz what if upload upload.pdf


def handle_command(user_input,client=None):
    command = user_input.strip().lower().split()
    if command and command[0] in Target_Words:
        execute_command(user_input,client)
        return True
    return False

