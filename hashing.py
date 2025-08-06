import tlsh
import os


# Function to compute the actual fuzzy hash of the file

def compute_tlsh_hash(file_path):

    # Checks if the file exists

    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return None

    # Checks if the file is big enough or too small
    size = os.path.getsize(file_path)
    if size < 50:
        print(f"File too small for TLSH (size={size} bytes): {file_path}")
        return None


    # Opens and reads the file in bits
    with open(file_path, 'rb') as f:
        data = f.read()

    # Hashing the file
    h = tlsh.Tlsh()
    h.update(data)
    h.final()

    # Checks if the hash is valid and returns the hash, else returns an error
    if h.is_valid:
        return h.hexdigest()
    else:
        return None


# Main function
def main():
    # Defining file names
    file1 = "./1"
    file2 = "./2"

    # Calling hashing function to get the files' hashes
    hash1 = compute_tlsh_hash(file1)
    hash2 = compute_tlsh_hash(file2)

    # Prints if the file is too small and file was not hashed
    if hash1 is None or hash2 is None:
        print(f"File too small or invalid for TLSH comparison.")
        return

    # Calculates percent difference (delta) between files
    score = tlsh.diff(hash1, hash2) # Method for getting the difference score between two hashes on a scale that I don't know
    similarity = max(0, min(100, 150 - score)) # Converts the difference score into a percentage
    print("TLSH score:", score) # Prints the score
    print("Similarity (0-100):", similarity) # Prints the percentage

if __name__ == "__main__":
    main()
