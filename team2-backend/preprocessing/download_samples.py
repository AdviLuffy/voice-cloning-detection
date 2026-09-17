from huggingface_hub import list_repo_files, hf_hub_download
import os

REPO = "garystafford/deepfake-audio-detection"
REPO_TYPE = "dataset"

REAL_TARGET = 100
FAKE_TARGET = 100

real_dir = "dataset/raw/real"
fake_dir = "dataset/raw/fake"

os.makedirs(real_dir, exist_ok=True)
os.makedirs(fake_dir, exist_ok=True)

print("Getting file list...")

files = list_repo_files(
    repo_id=REPO,
    repo_type=REPO_TYPE
)

real_files = [
    f for f in files
    if f.startswith("real/") and f.endswith(".flac")
]

fake_files = [
    f for f in files
    if f.startswith("fake/") and f.endswith(".flac")
]

print("Available REAL:", len(real_files))
print("Available FAKE:", len(fake_files))

print("\nDownloading REAL samples...")

for i, file in enumerate(real_files[:REAL_TARGET], 1):

    filename = os.path.basename(file)

    output = hf_hub_download(
        repo_id=REPO,
        filename=file,
        repo_type=REPO_TYPE,
        local_dir=real_dir
    )

    # Move from nested real/ folder if necessary
    downloaded = os.path.join(real_dir, file)

    final_path = os.path.join(real_dir, filename)

    if os.path.exists(downloaded) and downloaded != final_path:
        os.replace(downloaded, final_path)

    print(f"REAL {i}/{REAL_TARGET}: {filename}")


print("\nDownloading FAKE samples...")

for i, file in enumerate(fake_files[:FAKE_TARGET], 1):

    filename = os.path.basename(file)

    output = hf_hub_download(
        repo_id=REPO,
        filename=file,
        repo_type=REPO_TYPE,
        local_dir=fake_dir
    )

    downloaded = os.path.join(fake_dir, file)

    final_path = os.path.join(fake_dir, filename)

    if os.path.exists(downloaded) and downloaded != final_path:
        os.replace(downloaded, final_path)

    print(f"FAKE {i}/{FAKE_TARGET}: {filename}")


print("\n==============================")
print("DOWNLOAD COMPLETE")
print("==============================")
print("REAL:", len(os.listdir(real_dir)))
print("FAKE:", len(os.listdir(fake_dir)))