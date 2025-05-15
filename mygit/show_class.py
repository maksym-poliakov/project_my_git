# Класс для вывода данных в консоль
from .validator import Validator
from mygit.files_class import Files


class Show :

    def __init__(self):
        self.files = Files()


    @staticmethod
    def show_menu(data_menu:dict[str,str],index:int,max_value:int) -> bool :
        """
        Метод выводит на экран доступные пункты меню
        :param data_menu: Словарь с пунктами меню
        :param index: Число с которого начинается нумерация пунктов меню
        :param max_value: Длина словаря
        :return: bool
        """
        if  Validator.get_name_key_dict(data_menu,"title") :
            text_title = Validator.get_value_dict(data_menu, "title").strip()
            text_description = Validator.get_value_dict(data_menu, "description")
            if text_title :
                if max_value > 1:
                    print(f'{index} - {text_title + text_description }')
                else:
                    print(f' -  {text_title + text_description}')
            return True
        return False


    # __print_selection
    def print_selection(self):
        """
        Метод выводит на экран доступные файлы копий.

        """
        for keys, values in self.files.dict_copy().items():
            if len(values) > 0:
                print(f'{keys} : ')
            for key, value in values.items():
                print(key, self.files.delete_path(value))