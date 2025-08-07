# AI made this entire file, I don't take credit, I only asked for testing


import os
import random

BASE_TEXT = (
    "The quick brown fox jumps over the lazy dog. "
    "This sentence is used for typing practice. "
    "It contains every letter in the alphabet."
)

VARIATIONS = [
    ("quick", ["fast", "swift", "speedy"]),
    ("brown", ["dark", "chocolate", "umber"]),
    ("jumps", ["leaps", "hops", "bounds"]),
    ("lazy", ["sleepy", "sluggish", "inactive"]),
    ("dog", ["hound", "canine", "puppy"]),
    ("typing practice", ["typing tests", "keyboard training", "text input practice"]),
    ("alphabet", ["English alphabet", "ABCs", "letter set"]),
]

def apply_variations(text):
    for original, variants in VARIATIONS:
        if random.random() < 0.7:  # 70% chance to replace
            variant = random.choice(variants)
            text = text.replace(original, variant, 1)
    # Maybe shuffle some sentences
    if random.random() < 0.5:
        sentences = text.split(". ")
        random.shuffle(sentences)
        text = ". ".join(sentences)
    return text.strip()

# Create output directory
os.makedirs("test_files", exist_ok=True)

# Generate 20 files
for i in range(1, 21):
    content = apply_variations(BASE_TEXT)
    with open(f"test_files/file_{i:02d}.txt", "w") as f:
        f.write(content + "\n")
