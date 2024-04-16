from utils.gemini_text import GeminiText

PROMPT = """
Given context and chat history, continue the conversation with the query as the last user message.

Context: {context}
Chat history: {chat_history}
Query: {query}
Response:
"""


def fallback_component(query: str, chat_history: str, context: str) -> str:
    """
    This function is a fallback component that uses the GeminiText model to generate a response to a user query.

    Args:
        query (str): The user's query.
        chat_history (list): A list of previous messages in the conversation.
        context (str): The context of the conversation.

    Returns:
        str: The response generated by the GeminiText model.
    """

    gt = GeminiText()
    response = gt.generate_response(
        PROMPT.format(context=context, chat_history=chat_history, query=query)
    )
    return response