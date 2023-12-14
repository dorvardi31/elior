import tkinter as tk
from tkinter import filedialog
import data_processing

def upload_and_process_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        print(f"Processing file: {filepath}")
        data_processing.process_file(filepath)

root = tk.Tk()
root.title("File Upload for Processing")

upload_button = tk.Button(root, text="Upload File", command=upload_and_process_file)
upload_button.pack(pady=20)

root.mainloop()
