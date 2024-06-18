from ollama import AsyncClient, Client
from core.config import settings

ollama_external_client = Client(
    host=settings.OLLAMA_API_ENDPOINT
)

aollama_external_client = AsyncClient(
    host=settings.OLLAMA_API_ENDPOINT
)

def generate(prompts: list[dict[str, str]]) -> str:
    """
    Generate a non-streaming response.
    `prompts` follows a structure as the `openai` Python library.

    Arguments:
    - messages: A list of messages.

    prompts = [
        { "role": "system", "content": "Answer the patient's questions" },
        { "role": "user", "content": "I have a headache." },
        { "role": "assistant", "content": "Tell me more." },
        { "role": "user", "content": "It's on the right side." },
    ]
        
    """

    response = ollama_external_client.chat(
        model="llama3", 
        messages=prompts, # pyright: ignore [reportGeneralTypeIssues]
    )

    return response['message']['content']


async def agenerate(prompts: list[dict[str, str]]) -> str:
    """
    Generate a non-streaming response asynchronously.
    `prompts` follows a structure as the `openai` Python library.

    Arguments:
    - messages: A list of messages.

    messages = [
        { "role": "system", "content": "Answer the patient's questions" },
        { "role": "user", "content": "I have a headache." },
        { "role": "assistant", "content": "Tell me more." },
        { "role": "user", "content": "It's on the right side." },
    ]
        
    """

    response = await aollama_external_client.chat(
        model="llama3", 
        messages=prompts, # pyright: ignore [reportGeneralTypeIssues]
    )

    return response['message']['content']

