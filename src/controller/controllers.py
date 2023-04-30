import sys

from src.model.models import DataModel
from src.view.views import *


class MainController:
    model: DataModel
    view: App
    main_frame: MainFrame = None
    setup_frame: SetupFrame = None
    char_select_frame: CharSelectFrame = None

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
        self.main_frame.pack_forget()
        self.setup_frame = SetupFrame(master=self.view)
        self.setup_frame.init_checkboxes(self.model.get_settings())
        self.setup_frame.init_entries(self.model.get_player_numbers())
        self.setup_frame.bind("<<OnBack>>", lambda _: self.show_main_frame())
        self.setup_frame.bind("<<OnContinue>>", lambda _: self.show_char_select_frame())
        self.view.set_setup_frame(self.setup_frame)

    def setup_char_select(self):
        self.setup_frame.pack_forget()
        self.char_select_frame = CharSelectFrame(master=self.view)
        self.char_select_frame.bind("<<OnBack>>", lambda _: self.show_setup_frame())
        self.view.set_char_select_frame(self.char_select_frame)

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
            self.setup_char_select()
        else:
            self.forget_visible()
            self.view.set_char_select_frame(self.char_select_frame)

    def forget_visible(self):
        visible_frame = self.view.get_visible_frame()
        if visible_frame:
            visible_frame.pack_forget()

