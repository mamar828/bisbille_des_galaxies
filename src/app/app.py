import time
import numpy as np
from datetime import datetime
import tkinter as tk
from PIL import ImageTk, Image, ImageFont, ImageDraw
from tkinter import filedialog
from datetime import datetime
from random import sample
from os.path import isfile
from itertools import cycle
from typing import Literal

from src.engine.engine import Engine
from src.worlds.world import available_worlds
from src.engine.material_loader import MaterialLoader
from src.app.language import localization


class App(tk.Tk):
    def __init__(self, language: Literal["fr"] | Literal["en"]="fr"):
        tk.Tk.__init__(self)
        self.minsize(1072, 603)
        self.title("Bisbille des Galaxies")
        self.grid_propagate(False)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.language = localization[language]

        self.beamage_filename = ""
        self.score_foldername = ""
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        self.mode_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.language["file_menu"], menu=self.mode_menu)
        self.mode_menu.add_command(label=self.language["select_beamage"], command=self.select_beamage_file)
        self.mode_menu.add_command(label=self.language["show_beamage"], command=self.print_beamage_file)
        self.mode_menu.entryconfig(self.language["show_beamage"], state=tk.DISABLED)
        self.mode_menu.add_command(label=self.language["select_score_folder"], command=self.select_score_folder)
        self.mode_menu.add_command(label=self.language["show_score_folder"], command=self.print_score_folder)
        self.mode_menu.entryconfig(self.language["show_score_folder"], state=tk.DISABLED)

        info_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.language["about_menu"], menu=info_menu)
        info_menu.add_command(label="Version", command=lambda: tk.messagebox.showinfo(title="Version", 
                message=self.language["version_info"]))
        info_menu.add_command(
            label=self.language["thanks"],
            command=lambda: tk.messagebox.showinfo(
                title=self.language["thanks"], 
                message=self.language["thanks_info"]
            )
        )

    def select_beamage_file(self):
        self.beamage_filename = filedialog.askopenfilename(initialdir="/", title=self.language["select_beamage"],
            filetypes = (("Fichiers texte", "*.txt"), ("Tout fichiers", "*.*")))
        self.frame.focus_force()
        if self.beamage_filename == "":
            self.mode_menu.entryconfig(self.language["show_beamage"], state=tk.DISABLED)
        else:
            self.mode_menu.entryconfig(self.language["show_beamage"], state=tk.NORMAL)

    def print_beamage_file(self):
        tk.messagebox.showinfo(title=self.language["beamage_file"], message=f"{self.beamage_filename}")

    def select_score_folder(self):
        self.score_foldername = filedialog.askdirectory(initialdir="/", title=self.language["select_score_folder"])
        self.frame.focus_force()
        if self.score_foldername == "":
            self.mode_menu.entryconfig(self.language["show_score_folder"], state=tk.DISABLED)
        else:
            self.mode_menu.entryconfig(self.language["show_score_folder"], state=tk.NORMAL)

    def print_score_folder(self):
        tk.messagebox.showinfo(title=self.language["score_folder"], message=f"{self.score_foldername}")


class Window(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.images = [Image.open(f"src/engine/textures/title_screen_{i}.png") for i in [1,2]] 
        self.image_iter = cycle(self.images)
        # Initialize with the first image
        self.image_label = tk.Label(self, bg="black")
        self.image_label.grid(column=0, row=0, columnspan=3, rowspan=3, sticky="nsew")
        self.update_background()
        self.bind("<Configure>", self.resize_background)

    def update_background(self):
        self.original_image = next(self.image_iter)
        self.resize_background()
        self.after(1000, self.update_background)

    def resize_background(self, *args):
        window_width = self.master.winfo_width()
        window_height = self.master.winfo_height()

        img_width, img_height = self.original_image.size
        img_aspect_ratio = img_width / img_height
        window_aspect_ratio = window_width / window_height

        if window_aspect_ratio > img_aspect_ratio:
            # Window is wider than the image
            new_height = window_height
            new_width = int(new_height * img_aspect_ratio)
        else:
            # Window is taller than the image
            new_width = window_width
            new_height = int(new_width / img_aspect_ratio)

        # Resize the image and update the label
        resized_image = self.original_image.resize((max(new_width, 1), max(new_height, 1)), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=self.background_image)
        self.image_label.image = self.background_image  # Keep a reference to avoid garbage collection


class WindowJeuxPhotoniques(Window):
    def __init__(self, master):
        super().__init__(master)
        self.n_players = 4
        self.team_number = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        # Create a frame for buttons to manage their layout
        button_frame = tk.Frame(self, bg="black")
        button_frame.grid(column=1, row=1, sticky="nsew")

        # Configure the button frame to stretch
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1, minsize=100)
        button_frame.columnconfigure(2, weight=1)
        button_frame.rowconfigure(0, weight=1)
        button_frame.rowconfigure(1, weight=1)
        button_frame.rowconfigure(2, weight=1)

        # Buttons: they will now stay centered
        self.decrease_button = tk.Button(
            button_frame, text="-", font=("menlo", 35), bg="white", fg="black", command=self.decrease_players
        )
        self.decrease_button.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 10))
        
        self.increase_button = tk.Button(
            button_frame, text="+", font=("menlo", 35), bg="white", fg="black", command=self.increase_players
        )
        self.increase_button.grid(column=2, row=0, sticky="nsew", padx=(10, 10), pady=(10, 10))
        
        self.n_players_label = tk.Label(button_frame, text=self.n_players, font=("menlo", 35), bg="white", fg="black")
        self.n_players_label.grid(column=1, row=0, sticky="nsew", padx=(10, 10), pady=(10, 10))
        
        self.start_button = tk.Button(button_frame, text="START", font=("menlo", 35), bg="white", fg="black",
                                      command=self.start)
        self.start_button.grid(column=0, row=1, columnspan=3, sticky="nsew", padx=(10, 10), pady=(10, 10))
        
        self.team_number_label = tk.Label(button_frame, text="Équipe #", font=("menlo", 35), bg="white", fg="black")
        self.team_number_label.grid(column=0, row=2, columnspan=2, sticky="nsew", padx=(10, 10), pady=(10, 10))

        self.team_number = tk.Entry(
            button_frame, font=("menlo", 35), bg="white", fg="black", justify="right", width=2, validate="key",
            validatecommand=(self.master.register(WindowJeuxPhotoniques.validate_team_number_entry), "%P")
        )
        self.team_number.grid(column=2, row=2, sticky="nse", padx=(10, 10), pady=(10, 10))

    @staticmethod
    def validate_team_number_entry(value):
        if len(value) <= 2 and value.isdigit() or len(value) == 0:
            return True
        else:
            return False

    def increase_players(self):
        if self.n_players < len(self.master.worlds):
            self.n_players += 1
            self.update_n_players_label()

    def decrease_players(self):
        self.n_players = max(1, self.n_players - 1)
        self.update_n_players_label()

    def update_n_players_label(self):
        self.n_players_label.config(text=self.n_players)

    def start(self):
        if self.master.beamage_filename == "":
            tk.messagebox.showwarning(title="Error", message=self.master.language["error_no_beamage"])
        elif self.master.score_foldername == "":
            tk.messagebox.showwarning(title="Error", message=self.master.language["error_no_score"])
        elif self.team_number.get() == "":
            tk.messagebox.showwarning(title="Error", message=self.master.language["error_no_team"])
        else:
            score_filename = f"{self.master.score_foldername}/bisbille_scores.csv"
            if not isfile(score_filename):
                with open(score_filename, "w") as f:
                    f.write("equipe,nombre de joueurs,temps total (s),temps par joueur (s),temps de debut\n")

            engine = Engine(
                beamage_filename=self.master.beamage_filename,
                dev_mode=True,#False,
                material_loader=self.master.material_loader
            )
            chosen_worlds = sample(self.master.worlds, self.n_players)
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            total_time = []
            for world in chosen_worlds:
                engine.set_world(world())
                start = time.time()
                engine.run()
                stop = time.time()
                total_time.append(stop - start)

            engine.quit()
            with open(score_filename, "a") as f:
                total = sum(total_time)
                line = \
                    f"{self.team_number.get()},{self.n_players},{total:.2f},{total/self.n_players:.2f},{start_time}\n"
                print(line, end="")
                f.write(line)

            tk.messagebox.showinfo(
                title=self.master.language["result"],
                message=f"{self.master.language['total_time']} {total:.1f}s"
            )
            self.focus_force()


class WindowGentec(Window):
    def __init__(self, master):
        super().__init__(master)
        self.player_name = ""

        fonts = "1up.ttf", "Jersey10-Regular.ttf"
        self.fonts = [ImageFont.truetype(f"src/app/fonts/{font}", x)
                      for font, x in [(fonts[0], 45), (fonts[1], 35), (fonts[1], 30)]]

        self.grid_rowconfigure(0, weight=1, uniform="fred")
        self.grid_rowconfigure(1, weight=2, uniform="fred")
        self.grid_rowconfigure(2, weight=1, uniform="fred")
        self.grid_columnconfigure(0, weight=2, uniform="fred")
        self.grid_columnconfigure(1, weight=3, uniform="fred")
        self.grid_columnconfigure(2, weight=2, uniform="fred")

        self.high_scores_title, self._high_scores_title_photo = self.create_custom_font_label(
            "HIGH SCORES", self.fonts[0], (0, 255, 0), 400, 60
        )
        self.high_scores_title.grid(column=1, row=0)

        self.high_scores_list_names, self._high_scores_list_names_photo = None, None
        self.high_scores_list_times, self._high_scores_list_times_photo = None, None

        self.player_name_label, self._player_name_label_photo = self.create_custom_font_label(
            "PLAYER NAME:", self.fonts[1], (0, 255, 0), 165, 25, text_vertical_offset=-7
        )
        self.player_name_label.grid(column=0, row=2, padx=(100,0))

        self.player_name_entry = tk.Entry(
            self, font=("Courier", 20), bg="white", fg="black", justify="left", width=70, validate="key",
            validatecommand=(self.master.register(WindowGentec.validate_player_name_entry), "%P")
        )
        self.player_name_entry.grid(column=1, row=2, padx=(10, 10), pady=(10, 10))

        self.start_button = tk.Button(self, text="START", font=("menlo", 35), bg="white", fg="black",
                                      command=self.start)
        self.start_button.grid(column=2, row=2, padx=(10, 10), pady=(10, 10))

        # Load JP logo
        logo_image = ImageTk.PhotoImage(Image.open("src/app/images/jp_logo.png").resize((240,125)))
        label = tk.Label(self, image=logo_image, bg="black")
        label.image = logo_image                # keep a reference!
        label.grid(column=2, row=0, sticky="ne", padx=(0,30), pady=(30,0))

    def create_custom_font_label(
            self,
            text: str,
            font: ImageFont.FreeTypeFont,
            color: tuple[int, int, int],
            width: int,
            height: int,
            text_horizontal_offset: int=0,
            text_vertical_offset: int=0,
    ) -> tuple[tk.Label, ImageTk.PhotoImage]:
        # The returned type is a tuple as the PhotoImage must be assigned to a variable to prevent garbage collection
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.text((text_horizontal_offset, text_vertical_offset), text, font=font, fill=color)
        
        # Convert PIL Image to Tkinter PhotoImage
        photo = ImageTk.PhotoImage(image)

        # Use the photo as the label's image
        return tk.Label(self, image=photo, bg="black"), photo

    def update_high_scores_list(self):
        score_filename = f"{self.master.score_foldername}/bisbille_scores.csv"
        if isfile(score_filename):
            with open(f"{self.master.score_foldername}/bisbille_scores.csv", "r") as f:
                lines = f.readlines()
            if len(lines) > 1:
                lines = [line.strip().split(",") for line in lines[1:]]
                lines = sorted(lines, key=lambda x: float(x[1]))

                # Only show the top 10 scores
                names = [f"{f'{i}.'} {line[0]}" for i, line in enumerate(lines[:10], start=1)]
                times = [f"{float(line[1]):.2f} s" for line in lines[:10]]
                self.high_scores_list_names, self.high_scores_list_names_photo = self.create_custom_font_label(
                    "\n".join(names), self.fonts[2], (250, 0, 250), 350, len(names) * 29
                )
                self.high_scores_list_times, self.high_scores_list_times_photo = self.create_custom_font_label(
                    "\n".join(times), self.fonts[2], (250, 0, 250), 70, len(names) * 29, text_horizontal_offset=0
                )
                self.high_scores_list_names.grid(column=1, row=1, sticky="w")
                self.high_scores_list_times.grid(column=1, row=1, sticky="e")

    @staticmethod
    def validate_player_name_entry(value):
        if len(value) <= 35 or len(value) == 0:
            return True
        else:
            return False

    def start(self):
        if self.master.beamage_filename == "":
            tk.messagebox.showwarning(title="Error", message=self.master.language["error_no_beamage"])
        elif self.master.score_foldername == "":
            tk.messagebox.showwarning(title="Error", message=self.master.language["error_no_score"])
        elif self.player_name_entry.get() == "":
            tk.messagebox.showwarning(title="Error", message=self.master.language["error_no_player"])
        else:
            score_filename = f"{self.master.score_foldername}/bisbille_scores.csv"
            if not isfile(score_filename):
                with open(score_filename, "w") as f:
                    f.write("player name,time (s),game started at\n")

            engine = Engine(
                beamage_filename=self.master.beamage_filename,
                dev_mode=True,#False,
                material_loader=self.master.material_loader
            )
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            engine.set_world(self.master.worlds())
            start = time.time()
            engine.run()
            stop = time.time()

            total = stop - start
            engine.quit()
            with open(score_filename, "a") as f:
                line = f"{self.player_name_entry.get()},{total:.2f},{start_time}\n"
                print(line, end="")
                f.write(line)

            tk.messagebox.showinfo(
                title=self.master.language["result"],
                message=f"{self.master.language['total_time']} {total:.2f}s"
            )
            self.focus_force()
            self.update_high_scores_list()
            self.player_name_entry.delete(0, "end")


class AppJeuxPhotoniques(App):
    def __init__(self):
        super().__init__(language="fr")
        self.material_loader = MaterialLoader()
        self.worlds = available_worlds
        self.frame = WindowJeuxPhotoniques(self)
        self.frame.grid(column=0, row=0, sticky="nsew")


class AppGentec(App):
    def __init__(self, world_index: int):
        super().__init__(language="en")
        self.material_loader = MaterialLoader(world_index)
        self.worlds = available_worlds[world_index]
        self.frame = WindowGentec(self)
        self.frame.grid(column=0, row=0, sticky="nsew")

    def select_score_folder(self):
        super().select_score_folder()
        self.frame.update_high_scores_list()
