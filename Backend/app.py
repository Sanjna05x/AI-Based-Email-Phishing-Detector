from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from model_utils import predict_email, rule_based_checks

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-email")
async def analyze_email(email_text: str = Form(...)):
    ml_pred, confidence = predict_email(email_text)
    rule_reasons = rule_based_checks(email_text)

    result = {
        "prediction": "Phishing" if ml_pred == 1 else "Safe",
        "confidence": f"{confidence}%",
        "reasons": rule_reasons
    }
    return result

@app.get("/")
async def root():
    return {"message": "Email Phishing Detection API Running!"}

