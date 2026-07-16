def build_prompt(conversation,memory):
    prompt = f"""
    Below is the conversation history between you and the user.

    Coversation:
    {conversation}

    The following memories were retrieved because they were relevant to the user's
    latest message. Treat them as background context. Do not assume they are part
    of the conversation itself

    Relevant Memories:
    {memory}
    """

    return prompt