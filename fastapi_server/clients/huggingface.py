import requests
from core.config import settings
from loguru import logger

def query(payload: dict[str, str]) -> str:
    """
    Example:
        generated_text = query({ "inputs": "How are you?" })
        generated_text => "How are you?\n\nI'm fine, thank you."
    """

    BASE_API_URL = "https://api-inference.huggingface.co/models/"
    API_URL = f"{BASE_API_URL}{settings.HUGGING_FACE_MODEL}"
    headers = {"Authorization": f"Bearer {settings.HUGGING_FACE_SERVERLESS_INFERENCE_API_KEY}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    generated_text = response.json()[0]["generated_text"]
    return generated_text

def predict(prompt: str) -> str:
    """
    Example:
        formatted_text = predict("How are you?")
        formatted_text => "I'm fine, thank you."
    """

    # input_prompt = f"<s> [INST] {prompt} [/INST] Model answer</s> [INST] Follow-up instruction [/INST]"
    input_prompt = f"<s>[INST] {prompt} [/INST]"
    generated_text = query({ "inputs": input_prompt })

    # CURRENT PROBLEMS:
    # - The assistant's response gets cut off.
    logger.debug(f"generated_text: {generated_text}")

    formatted_text = generated_text.replace(input_prompt, "").strip()
    return formatted_text

