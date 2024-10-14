import serial
import time
import tkinter as tk
from PIL import ImageTk, Image
import threading
import numpy as np

from tkinter import scrolledtext
from tkinter import filedialog
from datetime import datetime


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("600x600")
        self.minsize(600, 600)
        self.title("Bisbille des Galaxies")
        self.grid_propagate(False)
        self.frame = Window(self)
        self.frame.grid(column=0, row=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        menubar = tk.Menu(self)
        self.config(menu=menubar)
        self.mode_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=self.mode_menu)
        self.mode_menu.add_command(label="Select Beamage file", command=self.select_beamage_file)
        self.mode_menu.add_command(label="Print Beamage file", command=self.print_beamage_file)
        self.mode_menu.entryconfig("Print Beamage file", state=tk.DISABLED)

    def select_beamage_file(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select Beamage file",
            filetypes = (("Text files", "*.txt"), ("All files", "*.*")))
        self.frame.focus_force()
        if self.filename == "":
            self.mode_menu.entryconfig("Print Beamage file", state=tk.DISABLED)
        else:
            self.mode_menu.entryconfig("Print Beamage file", state=tk.NORMAL)

    def print_beamage_file(self):
        tk.messagebox.showinfo(
            title="Beamage file",
            message=f"filename :\n{self.filename}"
        )

class Window(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.n_players = 5

        # Configure the rows and columns for proper centering
        self.grid_rowconfigure(0, weight=1)  # Top space
        self.grid_rowconfigure(1, weight=0)  # Button row (centered)
        self.grid_rowconfigure(2, weight=1)  # Bottom space
        self.grid_columnconfigure(0, weight=1)  # Left space
        self.grid_columnconfigure(1, weight=0)  # Center space
        self.grid_columnconfigure(2, weight=1)  # Center space

        # Load background image and set up panel
        self.image = Image.open("src/engine/textures/floor_test.png")
        self.image_copy= self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = tk.Label(self, image=self.background_image)
        self.background.grid(column=0, row=0, columnspan=3, rowspan=3, sticky="nsew")
        self.bind("<Configure>", self._resize_image)
        self.background.lower()

        # Create a frame for buttons to manage their layout
        button_frame = tk.Frame(self, bg="black")
        button_frame.grid(column=1, row=1, sticky="nsew")

        # Configure the button frame to stretch
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1, minsize=70)
        button_frame.columnconfigure(2, weight=1)

        # Buttons: they will now stay centered
        self.decrease_button = tk.Button(
            button_frame, text="-", font=("menlo", 35), bg="black", command=self.decrease_players
        )
        self.decrease_button.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 10))
        
        self.increase_button = tk.Button(
            button_frame, text="+", font=("menlo", 35), bg="black", command=self.increase_players
        )
        self.increase_button.grid(column=2, row=0, sticky="nsew", padx=(10, 10), pady=(10, 10))
        
        self.n_players_label = tk.Label(
            button_frame, text=self.n_players, font=("menlo", 35), bg="black"
        )
        self.n_players_label.grid(column=1, row=0, sticky="nsew", padx=(10, 10), pady=(10, 10))

    def increase_players(self):
        self.n_players += 1
        self.update_n_players_label()  # Update the label immediately

    def decrease_players(self):
        self.n_players = max(1, self.n_players - 1)
        self.update_n_players_label()  # Update the label immediately

    def update_n_players_label(self):
        self.n_players_label.config(text=self.n_players)

    def _resize_image(self, event):
        # Get the new dimensions of the window
        new_width = event.width
        new_height = event.height

        # Resize the background image to match the new window size
        self.image = self.image_copy.resize((new_width, new_height))
        self.background_image = ImageTk.PhotoImage(self.image)

        # Update the label with the resized background image
        self.background.configure(image=self.background_image)


if __name__ == "__main__":
    app = App()
    app.mainloop()
