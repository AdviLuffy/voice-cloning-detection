import os
import random
import shutil
import subprocess

# =========================
# SETTINGS
# =========================

FFMPEG = r"C:\Users\Adithya g\Downloads\ffmpeg-9.0.1-full_build-shared\ffmpeg-9.0.1-full_build-shared\bin\ffmpeg.exe"

SOURCE = "dataset/raw"

SPLITS = {
    "train": 0.70,
    "validation": 0.15,
    "test": 0.15
}

SEED = 42

# =========================
# SETUP
# =========================

random.seed(SEED)

labels = ["real", "fake"]

for split in SPLITS:
    for label in labels:
        os.makedirs(
            os.path.join("dataset", split, label),
            exist_ok=True
        )

# =========================
# PROCESS DATA
# =========================

for label in labels:

    source_folder = os.path.join(SOURCE, label)

    files = [
        f for f in os.listdir(source_folder)
        if f.lower().endswith(".flac")
    ]

    random.shuffle(files)

    total = len(files)

    train_end = int(total * 0.70)
    val_end = train_end + int(total * 0.15)

    split_files = {
        "train": files[:train_end],
        "validation": files[train_end:val_end],
        "test": files[val_end:]
    }

    print(f"\nProcessing {label.upper()}...")
    print("Total:", total)

    for split, split_list in split_files.items():

        output_folder = os.path.join(
            "dataset",
            split,
            label
        )

        for i, filename in enumerate(split_list, 1):

            input_file = os.path.join(
                source_folder,
                filename
            )

            output_name = os.path.splitext(filename)[0] + ".wav"

            output_file = os.path.join(
                output_folder,
                output_name
            )

            command = [
                FFMPEG,
                "-y",
                "-i",
                input_file,
                "-ac", "1",
                "-ar", "16000",
                "-sample_fmt", "s16",
                output_file
            ]

            result = subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode != 0:
                print("ERROR:", filename)
                print(result.stderr)
                continue

            print(
                f"{label.upper()} | "
                f"{split} | "
                f"{i}/{len(split_list)} | "
                f"{output_name}"
            )

print("\n==============================")
print("PREPROCESSING COMPLETE")
print("==============================")