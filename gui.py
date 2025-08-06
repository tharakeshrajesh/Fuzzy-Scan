import customtkinter as Ctk # Importing tkinter

selecteddir = None

# Functions
def directoryselect(): # Directory selecting function
    global selecteddir
    selecteddir = Ctk.filedialog.askdirectory()
    print(selecteddir)

app = Ctk.CTk() # Creating an app object
app.title("Fuzzy Scan") # Title of the window
app.geometry("400x500") # Setting the width and height of the app

# Creating buttons and stuff
selectdirbtn = Ctk.CTkButton(app, 100, 40, text="Select Directory to Scan", command=directoryselect)
selectdirbtn.pack(side='top', pady=100)

if __name__ == '__main__':
    app.mainloop()
