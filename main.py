import tlsh
import os

def compute_tlsh_hash(file_path):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return None

    size = os.path.getsize(file_path)
    if size < 50:
        print(f"File too small for TLSH (size={size} bytes): {file_path}")
        return None

    with open(file_path, 'rb') as f:
        data = f.read()

    h = tlsh.Tlsh()
    h.update(data)
    h.final()

    if h.is_valid:
        return h.hexdigest()
    else:
        print(f"Invalid TLSH hash for file: {file_path}")
        return None

def main():
    file1 = "./1"
    file2 = "./2"

    hash1 = compute_tlsh_hash(file1)
    hash2 = compute_tlsh_hash(file2)

    if hash1 is None or hash2 is None:
        print(f"File too small or invalid for TLSH comparison.")
        return

    score = tlsh.diff(hash1, hash2)
    similarity = max(0, min(100, 150 - score))
    print("TLSH score:", score)
    print("Similarity (0-100):", similarity)

if __name__ == "__main__":
    main()
