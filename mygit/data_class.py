# Класс для сбора данных и обработки данных
from typing import Dict
import re

class Data :

    DIR_IGNOR = []
    FILE_IGNOR = []
    PATTERN_DATA_TIME = r"\d{4}-\d{2}-\d{2} \d{2}-\d{2}"


    @classmethod
    def sorted_data_ignor(cls,data_ignor: list[str]) -> None :
        """
        Метод сортирует по спискам отдельно файлы отдельно папки
        :param data_ignor: Список с игнорируемыми файлами и папками.
        """
        for item in data_ignor:
            if item[0] == '/' :
                item = item[1 :]
                if not item in cls.DIR_IGNOR :
                    cls.DIR_IGNOR.append(item)
            elif item[0] == '*' :
                item = item[1:]
                if not item in cls.FILE_IGNOR:
                    cls.FILE_IGNOR.append(item)


    @staticmethod
    def dict_values(type_menu, data, key:any,min_value:int) -> Dict[any,dict[str,str]]:
        """
        Метод собирает в словарь значения для дальнейшей их об работки
        :param type_menu: Тип меню в котором находится пользователь.
        :param key: Ключ по которому собираем данные.
        :param data: Данные с которых нужно сделать выборку по ключу.
        :param min_value: Минимальное значение с которого начинается нумерация пунктов меню
        :return: Словарь со значениями.
        """
        dict_data = {type_menu: {}}
        for ind, value in enumerate(data, start=min_value):
            if key in value:
                dict_data[type_menu][ind] = value[key]
        return dict_data


    def __words_to_int(self,words:list[str], dict_param:Dict[str,str],key_param:str):
        """
        Метод переводит словарное представления выбранного параметра в числовое
        :param words: Список слов.
        :param dict_param: Словарь с параметрами для сравнения
        :param key_param: Ключ словаря к которому обращаемся
        :return: Список чисел соответствующий выбранным данным из словаря
        """
        list_result = []
        for word in words:
            list_number = []
            for item in word:
                if item in dict_param[key_param].values():
                    for key, value in dict_param[key_param].items():
                        if item == value:
                            list_number.append(str(key))
                else:
                    list_number.append('')
            list_result.append(list_number)

        return self.__clear_list_if_empty(list_result)


    @staticmethod
    def __clear_list_if_empty(lst):
        """
        Метод очищает список от пустых списков
        :param lst: Список списков
        :return: Список с отсутствием вложенных в него списков
        """
        clear = [[] if item == ['', ''] else item for item in lst]
        return [] if all(item == [] for item in clear) else clear


    @staticmethod
    def clear_space(text):
        """
        Метод очистки текста от пробелов.
        :param text: Текст который нужно очистить.
        :return: Текст без пробелов.
        """
        return ''.join(text.strip().split())


    @staticmethod
    def get_data_or_datatime(pattern:str, name_file:str):
        return re.search(pattern, name_file).group()

