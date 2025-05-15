from .show_class import Show

class Choice :
    def __init__(self):
        self.show_cls = Show()


    def get_choice(self,choice:str) -> None:
        """

        :param choice: Меню выбора
        :return:
        """
        if choice == "choice_list_copies" or choice == "delete_copies":
            self.show_cls.print_selection()
