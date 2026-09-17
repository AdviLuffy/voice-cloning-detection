import os
import subprocess

folders = {
    "REAL": "dataset/raw/real",
    "FAKE": "dataset/raw/fake"
}

for label, folder in folders.items():

    print(f"\nChecking {label} audio...")

    files = [
        f for f in os.listdir(folder)
        if f.lower().endswith(".flac")
    ]

    print("FLAC files found:", len(files))

    valid = 0
    invalid = 0

    for filename in files:

        filepath = os.path.join(folder, filename)

        result = subprocess.run(
            [
                r"C:\Users\Adithya g\Downloads\ffmpeg-9.0.1-full_build-shared\ffmpeg-9.0.1-full_build-shared\bin\ffmpeg.exe",
                "-v", "error",
                "-i", filepath,
                "-f", "null",
                "-"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode == 0:
            valid += 1
        else:
            invalid += 1
            print("INVALID:", filename)

    print("Valid:", valid)
    print("Invalid:", invalid)

print("\nAudio check complete!")