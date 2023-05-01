import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from src.model.character import Character
from src.model.player import Player
from src.view.character_card import CharacterCard
from src.view.result_card import ResultCard
from src.view.selection_card import SelectionCard

WIDTH = 1800
HEIGHT = 1200

BG_COLOR = "#0D1117"
FG_COLOR = "#C9D1D9"
BUTTON_COLOR = "#21262D"
HOVER_COLOR = "#161B22"
MENU_BUTTON_STYLE = "main.TButton"


class MainFrame(ttk.Frame):
    button_frame: ttk.Frame
    play_button: ttk.Button
    exit_button: ttk.Button

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.__setup_widgets()

    def setup(self):
        self.pack(fill=tk.BOTH, expand=True)

    def __setup_widgets(self):
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(anchor=tk.CENTER, expand=True)

        self.play_button = ttk.Button(self.button_frame,
                                      text="Start",
                                      command=self.__on_start,
                                      style=MENU_BUTTON_STYLE)

        self.exit_button = ttk.Button(self.button_frame,
                                      text="Exit",
                                      command=self.__on_exit,
                                      style=MENU_BUTTON_STYLE)

        self.play_button.pack(side=tk.TOP, padx=5, pady=10)
        self.exit_button.pack(side=tk.BOTTOM, padx=5, pady=10)

    def __on_start(self):
        self.event_generate("<<OnStart>>")

    def __on_exit(self):
        self.event_generate("<<OnExit>>")


class SetupFrame(ttk.Frame):
    bottom_frame: ttk.Frame
    settings_frame: ttk.Frame
    back_button: ttk.Button
    continue_button: ttk.Button
    player_scale: ttk.Scale
    checkboxes: {}
    like_scale: ttk.Scale
    dislike_scale: ttk.Scale
    player_numbers: tk.IntVar
    player_1_name: tk.StringVar
    player_2_name: tk.StringVar
    player_3_name: tk.StringVar
    player_4_name: tk.StringVar

    # TODO: Add possibility to change setting scale for disliked and liked characters

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.checkboxes = {}
        self.settings = {}

        self.player_1_name = tk.StringVar(value="")
        self.player_2_name = tk.StringVar(value="")
        self.player_3_name = tk.StringVar(value="")
        self.player_4_name = tk.StringVar(value="")
        self.__setup_widgets()

    def setup(self):
        self.pack(fill=tk.BOTH, expand=True)

    def __setup_widgets(self):
        self.bottom_frame = ttk.Frame(self)
        self.settings_frame = ttk.Frame(self)
        self.settings_frame.pack(anchor=tk.CENTER, expand=True)

        self.back_button = ttk.Button(self.bottom_frame,
                                      text="Back",
                                      command=self.__on_back)
        self.continue_button = ttk.Button(self.bottom_frame,
                                          text="Continue",
                                          command=self.__on_continue)

        self.back_button.pack(pady=10, padx=10, side=tk.LEFT)
        self.continue_button.pack(pady=10, padx=10, side=tk.RIGHT)
        self.bottom_frame.pack(side=tk.BOTTOM, anchor=tk.CENTER, expand=True)
        self.settings_frame.pack(anchor=tk.CENTER, expand=True)

    def __on_back(self):
        self.event_generate("<<OnBack>>")

    def __on_continue(self):
        self.event_generate("<<OnContinue>>")

    def init_checkboxes(self, settings: dict):
        for index, (key, var) in enumerate(settings.items()):
            self.checkboxes[key] = ttk.Checkbutton(self.settings_frame, text=key.replace('_', ' ').capitalize(),
                                                   variable=var, style="TCheckbutton")
            self.checkboxes[key].grid(row=index // 2, column=index % 2, padx=5, pady=5, sticky=tk.W)

        spacer = ttk.Frame(self.settings_frame, height=25)
        spacer.grid(row=len(self.checkboxes) // 2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)

    def init_scales(self, like_scale: tk.IntVar, dislike_scale: tk.IntVar):
        self.like_scale = tk.Scale(self.settings_frame,
                                   from_=0,
                                   to=100,
                                   orient=tk.HORIZONTAL,
                                   variable=like_scale,
                                   bg=BG_COLOR,
                                   fg=FG_COLOR,
                                   activebackground=HOVER_COLOR,
                                   highlightbackground=BG_COLOR,
                                   highlightcolor=BG_COLOR,
                                   sliderrelief=tk.FLAT,
                                   troughcolor=BUTTON_COLOR,
                                   relief=tk.FLAT,
                                   bd=0)
        self.dislike_scale = tk.Scale(self.settings_frame,
                                      from_=0,
                                      to=100,
                                      orient=tk.HORIZONTAL,
                                      variable=dislike_scale,
                                      bg=BG_COLOR,
                                      fg=FG_COLOR,
                                      activebackground=HOVER_COLOR,
                                      highlightbackground=BG_COLOR,
                                      highlightcolor=BG_COLOR,
                                      sliderrelief=tk.FLAT,
                                      troughcolor=BUTTON_COLOR,
                                      relief=tk.FLAT,
                                      bd=0)
        like_label = ttk.Label(self.settings_frame, text="Like scale: ")
        dislike_label = ttk.Label(self.settings_frame, text="Dislike scale: ")
        like_label.grid(row=len(self.checkboxes) + 0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        dislike_label.grid(row=len(self.checkboxes) + 1, column=0, padx=5, pady=5, sticky=tk.NSEW)
        self.like_scale.grid(row=len(self.checkboxes) + 0, column=1, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)
        self.dislike_scale.grid(row=len(self.checkboxes) + 1, column=1, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)

    def init_entries(self, player_numbers: tk.IntVar):
        self.player_numbers = player_numbers
        scale_label = ttk.Label(self.settings_frame, text="Number of players:")
        scale_label.grid(row=len(self.checkboxes) + 7, column=0, columnspan=2, padx=5, pady=15, sticky=tk.NSEW)
        self.player_scale = tk.Scale(self.settings_frame,
                                     from_=1,
                                     to=4,
                                     orient=tk.HORIZONTAL,
                                     variable=player_numbers,
                                     command=lambda _: self.update_entry_states(),
                                     bg=BG_COLOR,
                                     fg=FG_COLOR,
                                     activebackground=HOVER_COLOR,
                                     highlightbackground=BG_COLOR,
                                     highlightcolor=BG_COLOR,
                                     sliderrelief=tk.FLAT,
                                     troughcolor=BUTTON_COLOR,
                                     relief=tk.FLAT,
                                     bd=0)
        self.player_scale.grid(row=len(self.checkboxes) + 7, column=1, columnspan=2, padx=5, pady=15, sticky=tk.NSEW)

        for i in range(4):
            ttk.Label(self.settings_frame, text=f"Player {i + 1} Name:") \
                .grid(row=len(self.checkboxes) + i + 2, column=0, padx=5, pady=15, sticky=tk.W)
            entry = ttk.Entry(self.settings_frame, textvariable=getattr(self, f"player_{i + 1}_name"))
            entry.grid(row=len(self.checkboxes) + i + 2, column=1, padx=5, pady=15, sticky=tk.W)
            setattr(self, f"player_{i + 1}_entry", entry)

        self.update_entry_states()

    def update_entry_states(self):
        num_players = self.player_numbers.get()
        for i in range(4):
            entry = getattr(self, f"player_{i + 1}_entry")
            if i < num_players:
                entry["state"] = "normal"
            else:
                entry["state"] = "disabled"

    def get_players(self):
        players = []
        for i in range(self.player_numbers.get()):
            name = getattr(self, f"player_{i + 1}_name")
            if name:
                players.append(name)
        return players


class CharSelectFrame(ttk.Frame):
    bottom_frame: ttk.Frame
    char_frame: ttk.Frame
    top_frame: ttk.Frame
    back_button: ttk.Button
    continue_button: ttk.Button
    title_label: ttk.Label
    character_cards = []

    num_columns = 10

    # TODO: insert one frame for each character and insert into char_frame

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.__setup_widgets()

    def setup(self):
        self.pack(fill=tk.BOTH, expand=True)

    def __setup_widgets(self):
        self.top_frame = ttk.Frame(self)
        self.bottom_frame = ttk.Frame(self)
        self.char_frame = ttk.Frame(self)
        self.top_frame.pack(side=tk.TOP, anchor=tk.CENTER, expand=True)
        self.bottom_frame.pack(side=tk.BOTTOM, anchor=tk.CENTER, expand=True)
        self.char_frame.pack(anchor=tk.CENTER, expand=True)

        self.title_label = ttk.Label(self.top_frame, text="Select Characters", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10, padx=10, side=tk.TOP)

        self.back_button = ttk.Button(self.bottom_frame,
                                      text="Exit",
                                      command=self.__on_exit)
        self.back_button.pack(pady=10, padx=10, side=tk.LEFT)
        self.continue_button = ttk.Button(self.bottom_frame,
                                          text="Continue",
                                          command=self.__on_continue)
        self.continue_button.pack(pady=10, padx=10, side=tk.RIGHT)

    def __on_exit(self):
        self.event_generate("<<OnExit>>")

    def __on_continue(self):
        self.event_generate("<<OnContinueChar>>")

    def init_character_cards(self, characters: list[Character]):
        for i, character in enumerate(characters):
            row = i // self.num_columns
            column = i % self.num_columns
            card = CharacterCard(self.char_frame, character)
            card.grid(row=row, column=column)
            self.character_cards.append(card)

    def get_selected_characters(self) -> list[Character]:
        return [card.character for card in self.character_cards if card.selected]

    def update_frame(self, player_name: str, decide: str):
        self.title_label["text"] = f"{player_name}, select {decide} your characters!"
        for card in self.character_cards:
            card.selected = False
            card.reset()


class RollFrame(ttk.Frame):
    bottom_frame: ttk.Frame
    card_frame: ttk.Frame
    roll_button: ttk.Button
    winner_card: ResultCard = None
    loser_card: ResultCard = None
    title_label: ttk.Label
    score_label: ttk.Label
    game_cards = {}

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.__setup_widgets()

    def setup(self):
        self.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER)

    def __setup_widgets(self):
        self.bottom_frame = ttk.Frame(self)
        self.card_frame = ttk.Frame(self)
        self.card_frame.pack(expand=True, anchor=tk.CENTER)
        self.bottom_frame.pack(side=tk.BOTTOM, anchor=tk.CENTER, expand=True)

        self.roll_button = ttk.Button(self.bottom_frame,
                                      text="Roll",
                                      command=self.__on_roll)
        self.roll_button.pack(pady=10, padx=10, side=tk.LEFT)

    def __on_roll(self):
        self.event_generate("<<OnRoll>>")

    def generate_cards(self, players: list[Player]):
        selection_frame_left = ttk.Frame(self.card_frame)
        selection_frame_right = ttk.Frame(self.card_frame)

        for i, player in enumerate(players):
            card = SelectionCard(self.card_frame, player)

            if i < len(players) // 2:
                selection_frame = selection_frame_left
            else:
                selection_frame = selection_frame_right

            card.grid(row=i % (len(players) // 2), column=0, in_=selection_frame)
            self.game_cards[player.name] = card

        selection_frame_left.grid(row=0, column=1, rowspan=2)
        selection_frame_right.grid(row=0, column=2, rowspan=2)

    def insert_winner_card(self, players: list[Player]):
        self.winner_card = ResultCard(self.card_frame, "Winner", players)
        self.winner_card.grid(row=0, column=0, rowspan=2, sticky=tk.W)

    def insert_loser_card(self, players: list[Player]):
        self.loser_card = ResultCard(self.card_frame, "Loser", players)
        self.loser_card.grid(row=0, column=3, rowspan=2, sticky=tk.E)

    def get_winner(self) -> Player:
        if self.winner_card is None:
            return None
        winner = self.winner_card.get_selected_player()
        print("Winner")
        print(winner)
        return winner

    def get_loser(self) -> Player:
        if self.loser_card is None:
            return None
        loser = self.loser_card.get_selected_player()
        print("Loser")
        print(loser)
        return loser

    def update_frame(self, selections: dict[str, Character]):
        if self.winner_card is not None:
            self.winner_card.update_frame(selections)
        if self.loser_card is not None:
            self.loser_card.update_frame(selections)
        for player_name, character in selections.items():
            self.game_cards[player_name].set_character(character)


class App(tk.Tk):
    main_frame: MainFrame
    setup_frame: SetupFrame
    char_select_frame: CharSelectFrame
    roll_frame: RollFrame

    def __init__(self):
        super().__init__()
        self.title("Smash picker")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self["bg"] = BG_COLOR
        set_style()

    def set_main_frame(self, frame: MainFrame):
        self.main_frame = frame
        frame.setup()

    def set_setup_frame(self, frame: SetupFrame):
        self.setup_frame = frame
        frame.setup()

    def set_char_select_frame(self, frame: CharSelectFrame):
        self.char_select_frame = frame
        frame.setup()

    def set_roll_frame(self, frame: RollFrame):
        self.roll_frame = frame
        frame.setup()

    def get_visible_frame(self) -> ttk.Frame:
        for child in self.winfo_children():
            if isinstance(child, (MainFrame, SetupFrame, CharSelectFrame)) and child.winfo_ismapped():
                return child
        return None


def set_style():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame",
                    background=BG_COLOR)
    style.configure(MENU_BUTTON_STYLE,
                    font=("Arial", 20, "bold"),
                    background=BUTTON_COLOR,
                    foreground=FG_COLOR,
                    borderwidth=0,
                    focuscolor=BG_COLOR,
                    padding=35,
                    width=25)
    style.map(MENU_BUTTON_STYLE,
              background=[("active", HOVER_COLOR)],
              foreground=[("active", FG_COLOR)])

    style.configure("TButton", font=("Arial", 12),
                    background=BUTTON_COLOR,
                    foreground=FG_COLOR,
                    borderwidth=0,
                    focuscolor=BG_COLOR,
                    padding=10,
                    width=15)
    style.map("TButton",
              background=[("active", HOVER_COLOR)],
              foreground=[("active", FG_COLOR)])

    style.configure("TLabel", font=("Arial", 12),
                    background=BG_COLOR,
                    foreground=FG_COLOR)
    style.configure("TCheckbutton", font=("Arial", 12),
                    background=BG_COLOR,
                    foreground=FG_COLOR,
                    borderwidth=0,
                    focuscolor=BG_COLOR,
                    padding=5,
                    width=15)
    style.map("TCheckbutton",
              background=[("active", HOVER_COLOR)],
              foreground=[("active", FG_COLOR)])
    style.configure("TRadiobutton", font=("Arial", 12),
                    background=BG_COLOR,
                    foreground=FG_COLOR)
    style.configure("TCombobox", font=("Arial", 12),
                    background=BG_COLOR,
                    foreground=FG_COLOR)
    style.configure("TEntry", font=("Arial", 15, "bold"),
                    background=BG_COLOR,
                    foreground='black',
                    borderwidth=0,
                    insertcolor='white',
                    insertwidth=3,
                    padding=(10, 5),
                    width=15)
    style.configure("TSpinbox", font=("Arial", 12),
                    background=BG_COLOR,
                    foreground=FG_COLOR)
