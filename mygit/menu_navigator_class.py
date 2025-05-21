# Класс Меню навигатор для управления перемещения по пунктам меню.
from typing import Dict
from .validator import Validator
from .show_class import Show
from mygit.action_class import Action
from mygit.data_class import Data
from mygit.choice_class import Choice

class MenuNavigator:

    def __init__(self,min_value):
        # Минимальное значение с которого начинается нумерация меню
        self.min_value = min_value
        self.select = min_value
        self.validator = Validator()
        self.action = Action()
        self.data_cls = Data()
        self. choice_cls = Choice()


    def navigator(self,menu:Dict):
        for index, values in enumerate(menu):
            data =  menu[values]
            max_value = self.__get_number_menu_items(data)
            for ind, value in enumerate(data, start=self.min_value):
                # Выведем меню на экран
                if not Show.show_menu(value,ind,max_value) :
                    if isinstance(value, dict):
                        self.select = self.navigation_logic(values,value, max_value, data)
                        if not self.select is None:
                            return self.navigator(data[self.select - 1])
        return None


    def navigation_logic(self,name_menu:str,value:dict[str,str],max_value:int,data:list[dict[str,str]]) -> int|None:
        """
        Метод содержащий логику перемещения по пунктам меню.
        :param name_menu: Название меню в котором находится пользователь main_menu/sub_menu ....
        :param value: Словарь с пунктами меню.
        :param max_value: Количество пунктов меню
        :param data: Список со словарями пунктов меню
        :return:
        """
        action = self.validator.get_value_dict(value, 'action')
        data_type = self.validator.get_value_dict(value, 'data_type')
        title = self.validator.get_value_dict(value, 'title')
        choice = self.validator.get_value_dict(value, "choice")
        input_method = self.validator.get_value_dict(value, "input_method")
        create_field = self.validator.get_value_dict(value,"create_field")
        requirement = self.validator.get_value_dict(value,"requirement")
        if choice :
            self.choice_cls.get_choice(choice)
        if question := self.validator.get_value_dict(value, 'question'):
            self.select = self.validator.select(question)
            if title :
                self.select = self.validator.validator_select(name_menu, data, self.select, self.min_value)
            else:
                self.select = self.validator.validator_input(name_menu,question,requirement,data_type,input_method,action,
                                                             self.select, data,self.min_value,max_value)
            if  action :
                if create_field :
                    self.action.action(action,[self.select,create_field,requirement])
                else:
                    self.action.action(action, self.select)
                return None  # Остаемся в том же пункте меню main_menu
        elif action :
            if data_type :
                self.select = self.validator.validator_input(name_menu,question,requirement,data_type,
                                         input_method,action,self.select, data,self.min_value,max_value)
                if create_field:
                    self.action.action(action, [self.select, create_field,requirement])
                else:

                    self.action.action(action, self.select)
            return None  # Остаемся в том же пункте меню main_menu
        # select - триггер, что нужно оставаться в этом меню, своего рода авто выбор нужного меню
        elif select := self.validator.get_value_dict(value, 'select') :
            return int(select)
        if self.select == '' :
            self.validator.makes_exit()
        if self.select is None :
            return self.select
        else:
            return int(self.select)


    def __get_number_menu_items(self,data:list) -> int:
        """
        Метод для подсчета количества пунктов main_menu/sub_menu
        :param data: Данные части main_menu/sub_menu для которых нужно посчитать количество пунктов
        :return: количество пунктов выбранного main_menu/sub_menu
        """
        number_menu_items = self.min_value - 1
        for value in data:
            if "title" in value:
                number_menu_items += 1
        return number_menu_items








