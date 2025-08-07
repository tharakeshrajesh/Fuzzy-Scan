import customtkinter as Ctk # Importing tkinter
import tlsh # Importing hashing algorithm
from os import listdir, path # Importing listdir and path for file finding

# Variables
hashes = dict() # Dictionary of hashes
similars = dict() # Dictionary of similar files
selecteddir = None # Varaible to store the path of the selected directory
scoringsense = int(input("Scoring sense (150 recommended): ")) # Sensitivity of the scoring
minpercent = int(input("Minimum percentage for detections as a whole number (50 recommended): ")) # The minimum percentage a detection should be to show
minscore = int(input("Minimum score for detections as a whole number (30 recommended): ")) # The minimum score a detection should be to show

# Functions
# Directory selecting function
def directoryselect():
    global selecteddir, hashes, similars

    # Freeing up memory and clearing dictionaries to make sure it resets
    hashes.clear() 
    similars.clear()

    selecteddir = Ctk.filedialog.askdirectory()
    if not selecteddir: return # If no directory is selected, exit the function

    for file in listdir(selecteddir):
        fpath = path.join(selecteddir, file) # Defining the file path
        if not path.isfile(fpath): continue # Checks if the path is a file or else continues
        try:
            hash1 = compute_tlsh_hash(fpath) # Calling hashing function to get the files' hashes
            if not hash1: continue
        except Exception as e:
            print("Error: ", e)

    if hashes: compare_hashes() # Only compare if there are valid hashes

# Function to compute the actual fuzzy hash of the file
def compute_tlsh_hash(file_path):
    global hashes

    # Opens and reads the file in bits
    with open(file_path, 'rb') as f:
        data = f.read()
        filename = path.basename(f.name)

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
    for i, _ in enumerate(similars.keys()):
        row = i // 4 # 4 boxes per row
        col = i % 4 # 4 boxes per column
        box = Ctk.CTkFrame(frame)
        box.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

# Compare hashes function
def compare_hashes():
    global hashes, scoringsense, similars, minpercent, minscore
    compared = set() # Keeps track of already compared pairs to avoid duplicates

    for hash1 in list(hashes.keys()):
        for hash2 in list(hashes.keys()):
            if hash2 != hash1 and (hash1, hash2) not in compared and (hash2, hash1) not in compared: # Makes sure that it isn't comparing against itself
                compared.add((hash1, hash2)) # Marks this pair as compared
                try:
                    score = tlsh.diff(hash1, hash2) # Method for getting the difference score between two hashes on a scale that I don't know
                    similarity = max(0, min(100, scoringsense - score)) # Converts the difference score into a percentage
                    if minpercent >= similarity or minscore >= score: continue # Checks to see if it meets the user set requirements
                    similars.setdefault(hash1, []).append(hash2) # Pairs up the similar hashed files
                    print(f"Similarity (0-100) for {hashes.get(hash1)} and {hashes.get(hash2)} is {str(similarity)}") # Prints the percentage
                except Exception as e:
                    print(f"Error comparing {hash1} and {hash2}: {e}") # Handles any errors from tlsh.diff
    del compared # Freeing up memory

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

if __name__ == '__main__':
    app.mainloop()
