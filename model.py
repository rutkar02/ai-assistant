from config import MODEL

def call_model(messages,previous_response_id,tools,client):
    response = client.responses.create(
        model=MODEL,
        input=messages,
        previous_response_id=previous_response_id,
        tools = tools
    )
    return response
