from fastapi import FastAPI, UploadFile, File
import os
import uuid
import subprocess
import re

from audio_preprocess import preprocess_audio


app = FastAPI(
    title="Voice Deepfake Detection API",
    description="Backend API for AI-generated voice detection",
    version="1.0"
)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# --------------------------------------------------
# Get audio duration
# --------------------------------------------------

def get_audio_duration(file_path):
    result = subprocess.run(
        [
            r"C:\Users\Adithya g\Downloads\ffmpeg-9.0.1-full_build-shared\ffmpeg-9.0.1-full_build-shared\bin\ffmpeg.exe",
            "-i",
            file_path
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    output = result.stderr

    match = re.search(
        r"Duration: (\d+):(\d+):(\d+\.\d+)",
        output
    )

    if not match:
        raise RuntimeError("Could not determine audio duration")

    hours = int(match.group(1))
    minutes = int(match.group(2))
    seconds = float(match.group(3))

    return hours * 3600 + minutes * 60 + seconds


# --------------------------------------------------
# Home endpoint
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Voice Deepfake Detection API is running"
    }


# --------------------------------------------------
# Prediction endpoint
# --------------------------------------------------

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Maximum upload size: 20 MB
    MAX_FILE_SIZE = 20 * 1024 * 1024

    # --------------------------------------------------
    # Check file type
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Read uploaded file
    # --------------------------------------------------

    file_data = await file.read()

    # --------------------------------------------------
    # Check file size
    # --------------------------------------------------

    if len(file_data) > MAX_FILE_SIZE:
        return {
            "error": "File is too large. Maximum size is 20 MB."
        }

    # --------------------------------------------------
    # Create unique filename for uploaded audio
    # --------------------------------------------------

    extension = os.path.splitext(file.filename)[1]

    original_filename = f"{uuid.uuid4()}{extension}"

    input_path = os.path.join(
        UPLOAD_FOLDER,
        original_filename
    )

    # --------------------------------------------------
    # Create filename for processed WAV
    # --------------------------------------------------

    processed_filename = f"{uuid.uuid4()}.wav"

    processed_path = os.path.join(
        UPLOAD_FOLDER,
        processed_filename
    )

    try:

        # --------------------------------------------------
        # Save uploaded audio
        # --------------------------------------------------

        with open(input_path, "wb") as buffer:
            buffer.write(file_data)

        # --------------------------------------------------
        # Check audio duration
        # --------------------------------------------------

        duration = get_audio_duration(input_path)

        if duration < 1:
            return {
                "error": "Audio is too short. Minimum duration is 1 second."
            }

        if duration > 15:
            return {
                "error": "Audio is too long. Maximum duration is 15 seconds."
            }

        # --------------------------------------------------
        # Preprocess audio
        # WAV/MP3/FLAC
        #      ↓
        # 16 kHz mono WAV
        # --------------------------------------------------

        preprocess_audio(
            input_path,
            processed_path
        )

        # --------------------------------------------------
        # Temporary dummy prediction
        #
        # Team 1 model will replace this later
        # --------------------------------------------------

        label = "AI_GENERATED"
        confidence = 0.91

        # --------------------------------------------------
        # Calculate risk
        # --------------------------------------------------

        if confidence >= 0.80:
            risk = "HIGH"

        elif confidence >= 0.60:
            risk = "MEDIUM"

        else:
            risk = "LOW"

        # --------------------------------------------------
        # Return JSON response
        # --------------------------------------------------

        return {
            "label": label,
            "confidence": confidence,
            "risk": risk,
            "duration": round(duration, 2)
        }

    finally:

        # --------------------------------------------------
        # Delete temporary uploaded file
        # --------------------------------------------------

        if os.path.exists(input_path):
            os.remove(input_path)

        # --------------------------------------------------
        # Delete temporary processed file
        # --------------------------------------------------

        if os.path.exists(processed_path):
            os.remove(processed_path)