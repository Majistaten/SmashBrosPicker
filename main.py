from src.controller.controllers import MainController
from src.model.models import DataModel
from src.view.views import App


def main():
    controller = MainController(DataModel(), App())
    controller.start()


if __name__ == "__main__":
    main()
