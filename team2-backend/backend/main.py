from fastapi import FastAPI, UploadFile, File
import os
import uuid

app = FastAPI(
    title="Voice Deepfake Detection API",
    description="Backend API for AI-generated voice detection",
    version="1.0"
)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Voice Deepfake Detection API is running"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Check file type
    allowed_types = [
        "audio/wav",
        "audio/x-wav",
        "audio/flac",
        "audio/mpeg"
    ]

    if file.content_type not in allowed_types:
        return {
            "error": "Unsupported audio format"
        }

    # Create unique filename
    extension = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{extension}"

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Save uploaded audio
    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    # Temporary dummy prediction
    label = "AI_GENERATED"
    confidence = 0.91

    # Risk calculation
    if confidence >= 0.80:
        risk = "HIGH"
    elif confidence >= 0.60:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "label": label,
        "confidence": confidence,
        "risk": risk
    }