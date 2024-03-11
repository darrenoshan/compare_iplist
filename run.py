#!/usr/bin/python3

import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
import subprocess
import os

class FileComparerGUI:
    def __init__(self, master):
        self.master = master
        master.title("File Comparer")
        master.geometry("1200x600")  # سایز پنجره

        # اسم فایل ها 
        self.entry_reference_file = tk.Entry(master, state="readonly", width=100)
        self.entry_file2 = tk.Entry(master, state="readonly", width=100)

        # دکمه ها
        self.button_open_reference_file = tk.Button(master, text="Open Reference File", command=self.open_reference_file)
        self.button_open_file2 = tk.Button(master, text="Open IP-List File", command=self.open_file2)
        self.button_compare = tk.Button(master, text="Compare", command=self.compare_files)

        # textbox to display output
        self.output_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=10)
        self.output_text.insert(tk.END, "")

        # Place Entry widgets, buttons, and text widget on the window
        self.entry_reference_file.grid(row=0, column=1, pady=10)
        self.button_open_reference_file.grid(row=0, column=0, pady=10)
        self.entry_file2.grid(row=1, column=1, pady=10)
        self.button_open_file2.grid(row=1, column=0, pady=10)
        self.button_compare.grid(row=2, column=0, columnspan=2, pady=20)
        self.output_text.grid(row=3, column=0, columnspan=2, pady=20, padx=20, sticky="nsew")
        self.master.grid_rowconfigure(3, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Variables to store file paths
        self.reference_file_path = ""
        self.file2_path = ""

    def open_reference_file(self):
        file_types = (("Text files", "*.txt"), ("All files", "*.*"))
        initial_dir = os.getcwd()  # Set the initial directory to the current working directory
        self.reference_file_path = filedialog.askopenfilename(
            title="Open Reference File",
            initialdir=initial_dir,
            filetypes=file_types
        )
        self.entry_reference_file.config(state="normal")
        self.entry_reference_file.delete(0, tk.END)
        self.entry_reference_file.insert(0, self.reference_file_path)
        self.entry_reference_file.config(state="readonly")

    def open_file2(self):
        file_types = (("Text files", "*.txt"), ("All files", "*.*"))
        self.file2_path = filedialog.askopenfilename(
            title="Open IP-List File",
            filetypes=file_types
        )
        self.entry_file2.config(state="normal")
        self.entry_file2.delete(0, tk.END)
        self.entry_file2.insert(0, self.file2_path)
        self.entry_file2.config(state="readonly")

    def compare_files(self):
        if not (self.reference_file_path and self.file2_path):
            self.update_output("Error: Please select both files before comparing.")
            return

        # Call your main script with file paths
        command = ["/usr/bin/python3", "console.py", self.reference_file_path, self.file2_path]
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            self.update_output(result.stdout + result.stderr)
        except subprocess.CalledProcessError as e:
            self.update_output(f"Error: {e}")

    def update_output(self, text):
        # Clear previous content and update the Text widget
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text)


    def set_rtl_direction(self):
        # Create a tag configuration for right-to-left (RTL) text
        self.output_text.tag_configure("rtl", justify="right")

        # Apply the "rtl" tag to the existing text
        self.output_text.tag_add("rtl", 1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileComparerGUI(root)
    root.mainloop()
