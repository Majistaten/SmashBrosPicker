import sys

from src.model.models import DataModel
from src.model.player import Player
from src.view.views import *


class MainController:
    model: DataModel
    view: App
    main_frame: MainFrame = None
    setup_frame: SetupFrame = None
    char_select_frame: CharSelectFrame = None
    roll_frame: RollFrame = None
    current_player: Player = None
    liked_mode: bool = False

    def __init__(self, model: DataModel, view: App):
        self.model = model
        self.view = view
        self.setup_main()
        self.model.init_settings()

    def start(self):
        self.view.mainloop()

    def setup_main(self):
        self.main_frame = MainFrame(master=self.view)
        self.main_frame.bind("<<OnStart>>", lambda _: self.show_setup_frame())
        self.main_frame.bind("<<OnExit>>", lambda _: self.on_exit())
        self.view.set_main_frame(self.main_frame)

    def setup_setup(self):
        self.forget_visible()
        self.setup_frame = SetupFrame(master=self.view)
        self.setup_frame.init_checkboxes(self.model.get_settings())
        self.setup_frame.init_entries(self.model.get_player_numbers())
        self.setup_frame.init_scales(self.model.get_like_scale(), self.model.get_dislike_scale())
        self.setup_frame.bind("<<OnBack>>", lambda _: self.show_main_frame())
        self.setup_frame.bind("<<OnContinue>>", lambda _: self.show_char_select_frame())
        self.view.set_setup_frame(self.setup_frame)

    def setup_char_select(self):
        self.forget_visible()
        self.char_select_frame = CharSelectFrame(master=self.view)
        self.char_select_frame.init_character_cards(self.model.get_characters())
        self.char_select_frame.bind("<<OnBack>>", lambda _: self.show_setup_frame())
        self.char_select_frame.bind("<<OnContinueChar>>", lambda _: self.continue_char_selection())
        self.view.set_char_select_frame(self.char_select_frame)

    def setup_roll_frame(self):
        self.forget_visible()
        self.roll_frame = RollFrame(master=self.view)
        self.roll_frame.bind("<<OnRoll>>", lambda _: self.roll_selection())
        self.view.set_roll_frame(self.roll_frame)

    def on_exit(self):
        self.view.quit()
        self.view.destroy()
        sys.exit(0)

    def show_main_frame(self):
        if self.main_frame is None:
            self.setup_main()
        else:
            self.forget_visible()
            self.view.set_main_frame(self.main_frame)

    def show_setup_frame(self):
        if self.setup_frame is None:
            self.setup_setup()
        else:
            self.forget_visible()
            self.view.set_setup_frame(self.setup_frame)

    def show_char_select_frame(self):
        if self.char_select_frame is None:
            player_names = self.setup_frame.get_players()
            self.model.create_players(player_names)
            self.setup_char_select()
        else:
            self.forget_visible()
            self.view.set_char_select_frame(self.char_select_frame)
        self.continue_char_selection()

    def forget_visible(self):
        visible_frame = self.view.get_visible_frame()
        if visible_frame:
            visible_frame.pack_forget()

    def continue_char_selection(self):
        if self.current_player is None:
            pass
        elif self.liked_mode:
            self.current_player.liked_characters = self.char_select_frame.get_selected_characters()
        else:
            self.current_player.disliked_characters = self.char_select_frame.get_selected_characters()

        self.current_player = None

        for player in self.model.get_players():
            if not player.liked_characters and self.model.get_settings()["liked_characters"].get():
                self.current_player = player
                self.char_select_frame.update_frame(self.current_player.name, "liked")
                self.liked_mode = True
                break
            elif not player.disliked_characters and self.model.get_settings()["disliked_characters"].get():
                self.current_player = player
                self.char_select_frame.update_frame(self.current_player.name, "disliked")
                self.liked_mode = False
                break

        if self.current_player is None:
            print("All players have selected their characters")
            self.setup_roll_frame()

    def roll_selection(self):
        pass