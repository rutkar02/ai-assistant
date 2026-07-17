from knowledge import list_documents,delete_document,ingest_document
from config import Target_Words
from dataclasses import dataclass

@dataclass
class CommandResult:
    handled: bool
    message: str

def execute_command(command,client):
    if "upload" in command:
        pdf_name = command.split(maxsplit=1)[1]
        if pdf_name == "":
            return CommandResult(
                True,
                "Please provide a pdf path"
            )
        ingest_document(pdf_name,client)
        return CommandResult(
            True,
            f"Uploaded {pdf_name} successfully."
        )
    elif "list" in command:
        documents = list_documents()
        document_strings = "\n".join(f"̇- {doc}" for doc in documents)
        return CommandResult(
            True,
            f"Documents: \n{document_strings}"
        )   
    elif "delete" in command:
        pdf_name = command.split(maxsplit=1)[1]
        delete_document(pdf_name)     
        return CommandResult(
            True,
            f"Deleted {pdf_name}."
        )
    else:
        return CommandResult(
            False,
            "Unknown command."
        )

# ingest_document(command.split("upload")[1],client) is dangerous 
# coz what if upload upload.pdf


def handle_command(user_input,client=None):
    command = user_input.strip().lower().split()
    if command and command[0] in Target_Words:
        return execute_command(user_input,client)
    return CommandResult(
        False,
        ""
    )

