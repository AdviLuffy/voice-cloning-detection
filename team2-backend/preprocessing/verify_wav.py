import os
import subprocess

FFMPEG = r"C:\Users\Adithya g\Downloads\ffmpeg-9.0.1-full_build-shared\ffmpeg-9.0.1-full_build-shared\bin\ffmpeg.exe"

folders = [
    "dataset/train/real",
    "dataset/train/fake",
    "dataset/validation/real",
    "dataset/validation/fake",
    "dataset/test/real",
    "dataset/test/fake"
]

for folder in folders:

    files = [
        f for f in os.listdir(folder)
        if f.lower().endswith(".wav")
    ]

    print(f"\nChecking: {folder}")
    print("Files:", len(files))

    valid = 0

    for filename in files:

        filepath = os.path.join(folder, filename)

        result = subprocess.run(
            [
                FFMPEG,
                "-i",
                filepath
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        info = result.stderr

        if "16000 Hz" in info and "mono" in info:
            valid += 1
        else:
            print("CHECK FAILED:", filename)

    print("Correct 16kHz mono:", valid)
    print("Incorrect:", len(files) - valid)

print("\nWAV verification complete!")