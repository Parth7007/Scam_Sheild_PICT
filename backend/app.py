from fastapi import FastAPI
from pydantic import BaseModel
from modules.detection import ScamDetectionAI
from modules.faiss import ScamFAISS

app = FastAPI()

# Initialize AI modules
scam_ai = ScamDetectionAI(api_key="AIzaSyAZAiZLYC5-qgHff-il4vh2mKf_dhwkkNs")
scam_faiss = ScamFAISS()
scam_faiss.load_data("D:\\Scam_shield_PICT\\backend\\modules\\cleaned_scam_data.csv")  # Ensure data is loaded
scam_faiss.create_faiss_index()

# Load FAISS scam data
scam_faiss.load_faiss_index()

class ScamRequest(BaseModel):
    text: str

@app.post("/detect_scam/")
async def detect_scam(request: ScamRequest):
    """
    Receive text input, retrieve similar scam cases using FAISS, 
    and detect scams using Gemini AI.
    """
    try:
        # Retrieve similar scam cases using FAISS
        similar_texts = scam_faiss.search_similar_text(request.text, top_k=3)

        # Pass text and FAISS results to Gemini AI
        scam_result = scam_ai.detect_scam_with_gemini(request.text, similar_texts)

        return {
            "input_text": request.text,
            "similar_scam_cases": similar_texts,
            "scam_result": scam_result
        }

    except Exception as e:
        return {"error": str(e)}
