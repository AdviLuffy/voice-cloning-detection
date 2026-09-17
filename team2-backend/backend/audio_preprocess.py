import subprocess


FFMPEG = r"C:\Users\Adithya g\Downloads\ffmpeg-9.0.1-full_build-shared\ffmpeg-9.0.1-full_build-shared\bin\ffmpeg.exe"


def preprocess_audio(input_file, output_file):

    command = [
        FFMPEG,
        "-y",
        "-i", input_file,
        "-ac", "1",
        "-ar", "16000",
        "-c:a", "pcm_s16le",
        output_file
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Audio preprocessing failed:\n{result.stderr}"
        )

    return output_file