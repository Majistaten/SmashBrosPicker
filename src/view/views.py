import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

WIDTH = 1200
HEIGHT = 800

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
    player_slider: ttk.Scale
    checkboxes: {}
    player_numbers: tk.IntVar
    player_1_name: tk.StringVar
    player_2_name: tk.StringVar
    player_3_name: tk.StringVar
    player_4_name: tk.StringVar

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
        self.event_generate("<<OnSetup>>")

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

    def init_entries(self, player_numbers: tk.IntVar):
        self.player_numbers = player_numbers
        self.player_slider = tk.Scale(self.settings_frame,
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
        self.player_slider.grid(row=len(self.checkboxes) + 5, column=0, columnspan=2, padx=5, pady=15, sticky=tk.NSEW)

        for i in range(4):
            ttk.Label(self.settings_frame, text=f"Player {i + 1} Name:") \
                .grid(row=len(self.checkboxes) + i, column=0, padx=5, pady=15, sticky=tk.W)
            entry = ttk.Entry(self.settings_frame, textvariable=getattr(self, f"player_{i + 1}_name"))
            entry.grid(row=len(self.checkboxes) + i, column=1, padx=5, pady=15, sticky=tk.W)
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


class CharSelectFrame(ttk.Frame):
    bottom_frame: ttk.Frame
    char_frame: ttk.Frame
    back_button: ttk.Button

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.__setup_widgets()

    def setup(self):
        self.pack(fill=tk.BOTH, expand=True)

    def __setup_widgets(self):
        self.bottom_frame = ttk.Frame(self)
        self.char_frame = ttk.Frame(self)
        self.bottom_frame.pack(side=tk.BOTTOM, anchor=tk.CENTER, expand=True)
        self.char_frame.pack(anchor=tk.CENTER, expand=True)

        self.char_frame.columnconfigure(0, weight=1)

        self.back_button = ttk.Button(self.bottom_frame,
                                      text="Back",
                                      command=self.__on_back)
        self.back_button.pack(pady=10, padx=10, side=tk.LEFT)
        self.bottom_frame.pack(side=tk.BOTTOM, anchor=tk.CENTER, expand=True)

    def __on_back(self):
        self.event_generate("<<OnBack>>")


class App(tk.Tk):
    main_frame: MainFrame
    setup_frame: SetupFrame
    char_select_frame: CharSelectFrame

    def __init__(self):
        super().__init__()
        self.title("Smash picker")
        self.geometry(f"{WIDTH}x{HEIGHT}")
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

    def get_visible_frame(self) -> ttk.Frame:
        for child in self.winfo_children():
            if isinstance(child, (MainFrame, SetupFrame, CharSelectFrame)) and child.winfo_ismapped():
                return child
        return None

    def show_message(self, param):
        messagebox.showinfo("Info", param)


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
                    foreground=FG_COLOR)
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
