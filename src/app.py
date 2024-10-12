import serial
import time
import tkinter as tk
from PIL import ImageTk, Image
import threading
import numpy as np

from tkinter import scrolledtext
from datetime import datetime


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.width = 900
        self.height = 600
        self.minsize(self.width, self.height)
        self.title("Bisbille des Galaxies")
        self.frame = Window(self)
        self.frame.grid(column=0, row=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

class Window(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.n_players = 5

        # Configure the rows and columns for proper centering
        master.grid_rowconfigure(0, weight=1)  # Top space
        master.grid_rowconfigure(1, weight=0)  # Button row (centered)
        master.grid_rowconfigure(2, weight=1)  # Bottom space
        master.grid_columnconfigure(0, weight=1)  # Left space
        master.grid_columnconfigure(1, weight=0)  # Center space
        master.grid_columnconfigure(2, weight=1)  # Center space

        # Load background image and panel
        self.image = Image.open("src/engine/textures/floor_test.png")
        self.background_image = ImageTk.PhotoImage(self.image)
        self.panel = tk.Label(master, image=self.background_image)
        self.panel.grid(column=0, row=0, sticky="nsew")
        self.panel.lower()

        # Create a frame for buttons to manage their layout
        button_frame = tk.Frame(self, bg="black")
        button_frame.grid(column=0, row=1, columnspan=5, sticky="nsew")

        # Configure the button frame to stretch
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        button_frame.rowconfigure(0, weight=1)
        button_frame.rowconfigure(1, weight=1)

        # Buttons: they will now stay centered
        self.decrease_button = tk.Button(button_frame, text="-", font=("menlo", 35), command=self.decrease_players)
        self.decrease_button.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 10))
        
        self.n_players_label = tk.Label(button_frame, text=self.n_players, font=("menlo", 35), bg="black")
        self.n_players_label.grid(column=1, row=0, sticky="nsew", padx=(10, 10), pady=(10, 10))
        
        self.increase_button = tk.Button(button_frame, text="+", font=("menlo", 35), command=self.increase_players)
        self.increase_button.grid(column=2, row=0, sticky="nsew", padx=(10, 10), pady=(10, 10))

        self.start_button = tk.Button(button_frame, text="START", font=("menlo", 35), command=self.start)
        self.start_button.grid(column=0, row=1, columnspan=3, sticky="nsew", padx=(10, 10), pady=(10, 10))
        
        # Initialize a variable to track resizing
        self.is_resizing = False
        self.master.bind("<Configure>", self.resize_background)

    def increase_players(self):
        self.n_players += 1
        self.update_print_button_label()  # Update the label immediately

    def decrease_players(self):
        self.n_players = max(1, self.n_players - 1)
        self.update_print_button_label()  # Update the label immediately

    def update_print_button_label(self):
        self.n_players_label.config(text=self.n_players)

    def resize_background(self, event):
        if self.is_resizing:
            return  # Avoid unnecessary calls

        self.is_resizing = True
        new_width = event.width
        new_height = event.height

        # Only resize if the dimensions have changed
        if self.panel.winfo_width() != new_width or self.panel.winfo_height() != new_height:
            resized_image = self.image.resize((new_width, new_height), Image.ANTIALIAS)
            self.background_image = ImageTk.PhotoImage(resized_image)
            self.panel.config(image=self.background_image)
            self.panel.image = self.background_image  # Keep a reference to avoid garbage collection

        self.is_resizing = False

    def start(self):
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()
