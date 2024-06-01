from fastapi import APIRouter, Depends, File, UploadFile
from pydantic import BaseModel
import clients.ollama as ollama_internal_client
import clients.gradio as gradio_internal_client
from api import deps
import io
from PIL import Image

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
    Accepts unformatted text from the patient, and returns a formatted SOAP note.

    Arguments:
    - prompt: The patient's unformatted text.

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
    sample_patient_prompt = """Patient: 
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

    sample_assistant_prompt = """Assistant:
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

    return { "prediction": prediction }





@router.post("/upload", response_model=MessageResponse)
async def create_upload(
    *,
    authorization: bool = Depends(deps.authorize),
    files: list[UploadFile],
):
    """
    Accepts an image of the patient's intake form, and returns a formatted SOAP note.

    Arguments:
    - file: An image of the patient's intake form.

    Returns:
    - {"prediction": formatted_text}
    """

    for file in files:
        # Read the file as bytes
        file_bytes = await file.read()

        # Convert the bytes to a stream
        file_bytes_stream = io.BytesIO(file_bytes)

        # Convert the stream to a PIL image object
        image = Image.open(file_bytes_stream)

        gradio_internal_client.generate(image)


    prediction = "This is a placeholder for the prediction"

#
#
#
#
#     system_prompt = """System: You are an expert physician assistant. Take the history provided by the patient and summarize it in a SOAP note format. The format should take the following form:
# - brief statement of the patient's problem
# - details of the problem. These include onset, duration, location, quality, aggravating or relieving factors, and associated symptoms. Each bullet point should be no more than a few words.
# - PMHx:
# - PSHx:
# - Meds:
# - Allergies:
# - Soc:
# - If a medication isn't explainable by the PMHx or PSHx, put a star (*) next to it.
# """
#     sample_patient_prompt = """Patient: 
# What problem brought you in today? headache. It's on the left side of my head. It's a sharp pain. It's worse when I move my head. Nausea, sensitive to bright light.
# How long have you had this problem? since yesterday
# Do you have any medical problems? high blood pressure, arthritis, asthma
# Have you had any surgeries? knee replacement right, appendix surgery
# Do you take any medications? linopril, advil, ventolin, crestor
# Do you have any allergies? penicillin, peanuts
# Do you use tobacco? yes
# If you use tobacco, how long and how much do you use? since 16, not much
# Do you use alcohol? no
# Do you use recreational drugs? no
# """
#
#     sample_assistant_prompt = """Assistant:
# - headache since yesterday
# - left side, sharp pain, worse with movement
# - nausea, light sensitivity
# - PMHx: HTN, arthritis, asthma, crestor*
# - PSHx: RKR, appendectomy
# - Meds: lisinopril, advil, ventolin, crestor
# - Allergies: penicillin, peanuts
# - Soc: tobacco since 16, not much. No alcohol. No recreational drugs
# """
#
#     final_system_prompt = f"{system_prompt}\n\nExample Case:\n{sample_patient_prompt}\n{sample_assistant_prompt}"
#
#     prediction = await ollama_internal_client.agenerate([
#         { "role": "system", "content": final_system_prompt },
#         { "role": "user", "content": message.prompt },
#     ])

    return { "prediction": prediction }

