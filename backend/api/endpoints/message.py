from fastapi import APIRouter, Depends, HTTPException, UploadFile
from pydantic import BaseModel
import clients.ollama as ollama_internal_client
from api import deps
from io import BytesIO
from PIL import Image
from ml import ocr
from markdown import markdown
from loguru import logger

router = APIRouter()

class MessageCreate(BaseModel):
    prompt: str

class MessageResponse(BaseModel):
    prediction: str

@router.post("/message", response_model=MessageResponse)
async def create_message(
    *,
    authorization: bool = Depends(deps.authorize),
    message: MessageCreate
):
    """
    Accepts unformatted text from the patient, and returns a clean SOAP note in HTML format.
    HTML format is used because the frontend is rendering it in Tiptap.

    Arguments:
    - prompt: The intake form filled out by the patient.

    Returns:
    - {"prediction": formatted_text}
    """
    
    system_prompt = """System: You are an expert physician assistant. Take the history provided by the patient and summarize it in a SOAP note format. The format should take the following form:
- brief statement of the patient's problem
- details of the problem. These include onset, duration, location, quality, aggravating or relieving factors, and associated symptoms. Each bullet point should be no more than a few words.
- PMHx:
- PSHx:
- Meds:
- Allergies:
- Soc:
- If a medication isn't explainable by the PMHx or PSHx, put a star (*) next to it.
"""
    sample_patient_prompt = """### Patient: 
What problem brought you in today? headache. It's on the left side of my head. It's a sharp pain. It's worse when I move my head. Nausea, sensitive to bright light.
How long have you had this problem? since yesterday
Do you have any medical problems? high blood pressure, arthritis, asthma
Have you had any surgeries? knee replacement right, appendix surgery
Do you take any medications? linopril, advil, ventolin, crestor
Do you have any allergies? penicillin, peanuts
Do you use tobacco? yes
If you use tobacco, how long and how much do you use? since 16, not much
Do you use alcohol? no
Do you use recreational drugs? no
"""

    sample_assistant_prompt = """### Assistant:
- headache since yesterday
- left side, sharp pain, worse with movement
- nausea, light sensitivity
- PMHx: HTN, arthritis, asthma, crestor*
- PSHx: RKR, appendectomy
- Meds: lisinopril, advil, ventolin, crestor
- Allergies: penicillin, peanuts
- Soc: tobacco since 16, not much. No alcohol. No recreational drugs
"""

    final_system_prompt = f"{system_prompt}\n\nExample Case:\n{sample_patient_prompt}\n{sample_assistant_prompt}"

    prediction = await ollama_internal_client.agenerate([
        { "role": "system", "content": final_system_prompt },
        { "role": "user", "content": message.prompt },
    ])

    prediction = markdown(prediction)

    return { "prediction": prediction }

@router.post("/upload", response_model=MessageResponse)
async def create_upload(
    *,
    authorization: bool = Depends(deps.authorize),
    files: list[UploadFile],
    #prompt: str = "Transcribe the text from the image. Do not write anything other than the text."
):
    """
    Accepts a list of images containing handwritten text, and returns the transcribed text.

    Arguments:
    - files: A list of image files.

    Returns:
    - {"prediction": prediction}
    """

    prompt: str = "Transcribe the text from the image. Do not write anything other than the text."

    prediction = ""

    for file in files:
        # Read the file as bytes
        file_bytes = await file.read()

        # Convert the bytes to a stream
        file_bytes_stream = BytesIO(file_bytes)

        # Convert the stream to a PIL image object
        image = Image.open(file_bytes_stream).convert("RGB")

        model = ocr.load_model()

        tokenizer = ocr.load_tokenizer()

        try:
            msgs = [{'role': 'user', 'content': prompt}]

            chunk = model.chat(
                image=image,
                msgs=msgs,
                tokenizer=tokenizer,
                sampling=True,  # to use beam_search, set sampling=False
                temperature=0.7,
                device=ocr.settings.DEVICE
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Model inference failed: {str(e)}"
            )

        prediction += chunk

    return { "prediction": prediction }

