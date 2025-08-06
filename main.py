import customtkinter as Ctk # Importing tkinter
import tlsh # Importing hashing algorithm

# Variables
hashes = dict() # Dictionary of hashes
similars = dict() # Dictionary of similar files
selecteddir = None # Varaible to store the path of the selected directory
scoringsense = int(input("Scoring sense: ")) # Sensitivity of the scoring
mindetection = int(input("Minimum input detection: ")) # The minimum percentage a detection should be to show

# Functions
# Directory selecting function
def directoryselect():
    global selecteddir
    selecteddir = Ctk.filedialog.askdirectory()
    print(selecteddir)

# Function to compute the actual fuzzy hash of the file
def compute_tlsh_hash(file_path):
    global hashes

    # Opens and reads the file in bits
    with open(file_path, 'rb') as f:
        data = f.read()
        filename = f.name

    # Hashing the file
    h = tlsh.Tlsh()
    h.update(data)
    h.final()

    # Checks if the hash is valid or and returns the hash, else returns an error
    if h.is_valid:
        hashes[h.hexdigest()] = filename
        return h.hexdigest()
    else:
        return None

# Make boxes function
def add_boxes():
    global similars, hashes
    for widget in frame.winfo_children(): # Clears all the items in the frame
        widget.destroy()
    for i in range(len(similars.keys())):
        row = i // 4 # 4 boxes per row
        col = i % 4 # 4 boxes per column
        box = Ctk.CTkFrame(frame)
        box.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
    add_boxes()

# Compare hashes function
def compare_hashes():
    global hashes, scoringsense, similars
    for hash1 in list(hashes.keys()):
        for hash2 in list(hashes.keys()):
            if hash2 != hash1 and similars.get(hash2) != hash1: # Makes sure that it isn't comparing against itself
                score = tlsh.diff(hash1, hash2) # Method for getting the difference score between two hashes on a scale that I don't know
                similarity = max(0, min(100, scoringsense - score)) # Converts the difference score into a percentage
                similars[hash1] = hash2 # Pairs up the similar hashed files
                print(f"Similarity (0-100) for {hashes.get(hash1)} and {hashes.get(hash2)} is {similarity}") # Prints the percentage
    add_boxes()

# Tkinter variables
app = Ctk.CTk() # Creating an app object
app.title("Fuzzy Scan") # Title of the window
app.geometry("400x500") # Setting the width and height of the app

# Creating buttons and stuff
frame = Ctk.CTkFrame(app) # Creating a frame for a grid
frame.pack(fill="both", expand=True, side='bottom') # Packing the grid to display

selectdirbtn = Ctk.CTkButton(app, 100, 40, text="Select Directory to Scan", command=directoryselect) # Creating the select directory button
selectdirbtn.pack(side='top', pady=100) # Packing the button to display

# Making columns for boxes expand evenly
for col in range(4):
    frame.grid_columnconfigure(col, weight=1)

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

    compare_hashes()

if __name__ == '__main__':
    main()
    app.mainloop()
