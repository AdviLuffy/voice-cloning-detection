from datasets import load_dataset

print("Loading dataset...")

dataset = load_dataset(
    "SpeechAntiSpoofingBenchmarks/ASVspoof2021_DF",
    split="test",
    streaming=True
)

print("Dataset loaded!")

sample = next(iter(dataset))

print("\nKeys:")
print(sample.keys())

print("\nPath:")
print(sample["path"])

print("\nLabel:")
print(sample["label"])

print("\nNotes:")
print(sample["notes"])

print("\nAudio object:")
print(sample["audio"])

print("\nAudio object type:")
print(type(sample["audio"]))

print("\nInspection complete!")