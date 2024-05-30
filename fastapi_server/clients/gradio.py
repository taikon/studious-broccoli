from gradio_client import Client, file
from core.config import settings

gradio_client = Client(settings.GRADIO_API_ENDPOINT)

def generate(image_path: str) -> str:
    """
    Extracts text from an image.

    Arguments:
    - image_path: The path to the image.
    """
    load_image_response = client.predict(
      image=file(image_path),
      _chatbot=[],
      api_name="/upload_img"
    )

    user_prompt = "Transcribe the text from the image. Do not write anything other than the text."

    assistant_prompt = "Image uploaded successfully, you can talk to me now"

    start_transcribe_job_response = client.predict(
      _question=user_prompt,
      _chat_bot=[["",assistant_prompt]],
      api_name="/request",
    )

    response = client.predict(
      #_chat_bot=[["","Image uploaded successfully, you can talk to me now"],["Transcribe the text from the image. Do not write anything other than the text.",None]],
      _chat_bot=[["",assistant_prompt],[user_prompt,None]],
      params_form="Sampling",
      num_beams=3
      repetition_penalty=1.2,
      top_p=0.8,
      top_k=100,
      temperature=0.1,
      repetition_penalty_2=1.05,
      api_name="/respond"
    )

    # Clear response - Don't think this is needed, but if it gives weird results, then try uncommenting this.
    # client.predict(
    #   _question="",
    #   _chat_bot=[],
    #   _bt_pic={"sts":None,"ctx":None,"img":None},
    #   api_name="/clear_button_clicked"
    # )

    return response[1][1]

