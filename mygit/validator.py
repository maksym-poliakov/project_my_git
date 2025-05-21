# Класс для проверки данных
from mygit.unknownexception import UnknownException
from mygit.files_class import Files
from mygit.action_class import Action
from mygit.data_class import Data
from typing import Dict,List
import time
import re


class Validator:

    PATTERN_WORD_ALL = r'all'
    PATTERN_DIGITS_MINUS = r'(\d+)\s*-\s*(\d+)|(\d+)\s*-\s*|-\s*(\d+)|(?<!\d)-(?=\s|$)'  # Любезно предоставил GPT :)
    PATTERN_DIGITS = r'\d+'

    def __init__(self):
        self.files = Files()
        self.action = Action()
        self.data_cls = Data()


    @staticmethod
    def get_key_to_value(dict_data: dict, value_dict: str) -> str|None:
        """
        Метод извлекает имя ключа по значению
        :param dict_data: Словарь с данными
        :param value_dict: значение чей ключ интересует
        :return: значение ключа или ""
        """
        for key,value in dict_data.items() :
            if value == value_dict :
                return str(key)
        return None


    @staticmethod
    def get_value_dict(dict_data: dict, key: str) -> str:
        """
        Метод проверяет, существует, ли значение для конкретного ключа в словаре
        :param dict_data: Словарь с данными
        :param key: Ключ значение которого интересует
        :return: значение ключа или ""
        """
        if dict_data.get(key) is not None:
            return dict_data.get(key)
        return ""


    @staticmethod
    def get_name_key_dict(dict_data: dict, key: str) -> str | None:
        """
        Метод проверяет, существует, ли ключ в словаре
        :param dict_data: Словарь с данными
        :param key: Ключ который интересует
        :return: Строковое представление ключа
        """
        if key in dict_data:
            return str(key)
        return None


    @staticmethod
    def get_value_key_dict(dict_data: dict, value: str) -> str | None:
        """
        Метод для проверки наличия значения в словаре
        :param dict_data: Словарь со значениями
        :param value: Искомое значение
        :return: None
        """
        if value in dict_data.values():
            return value
        return None


    @staticmethod
    def dict_param(dict_data: dict, key:str) -> Dict[str,str] :
        """
        Метод собирает данные в словарь для дальнейшей проверки значений
        :param dict_data: Словарь откуда нужно собрать данные
        :param key: Ключ по которому нужно собрать данные
        :return: Словарь с данными
        """

        dict_param = {}
        for index,value in  enumerate(dict_data[key].values(),start=1) :
            dict_param[str(index)] = value
        return dict_param


    @staticmethod
    def __isdigit(*args):
        for arg in args:
            if not arg.isdigit():
                return False
        return True


    def get_value_select(self,select:str,min_value:int,max_value:int,data:List[Dict[str,str]]) -> int:
        """
        Метод для текстового представления выбранного пункта меню пользователем
        :param select: Строка с данными введенными пользователем
        :param min_value: Минимально допустимое значение
        :param max_value: Максимально допустимое значение
        :param data: Список словарей с данными.
        :return: Текстовое значение выбранного параметра
        """
        if select.isdigit():
            index = int(select)
            number_select = self.select_number_validator(index,min_value,max_value)
        else:
            number_select = self.select_title_validator(min_value,select,data)
            # print('number_select input text ==== ',number_select)
        return number_select



    def select_number_validator(self,select:int,min_value:int,max_value:int) ->  int :
        """
        Метод проверяет на наличие правильного выбранного диапазона
        :param select: Число введенное пользователем
        :param min_value: Минимально допустимое значение
        :param max_value: Максимально допустимое значение
        :return:
        """
        if min_value <= select <= max_value :
            return select
        while True :
            select = input(f"{self.files.show_translation("select_number_input_start",min_value,"to",max_value,"enter_exit")}")
            print('select = ',select)
            if select == '' :
                self.makes_exit()
            elif select.isdigit():
                return int(select)
            print(f"{self.files.show_translation("enter_exit")}")


    def validator_select(self,name_menu:str,data:list[dict[str,str]],select:str,min_value:int) -> str|None :
        if select is not None :
           if select.isdigit() :
               return select
           else:
               if dict_title_menu := self.data_cls.dict_values(name_menu,data,'title',min_value) :
                   return self.get_key_to_value(dict_title_menu[name_menu],select)
        return None


    def select_title_validator(self,min_value:int,select:str,data:list[Dict[str,str]]) -> int :
        """
         Метод проверяет на правильность введенного текстового выбора пункта меню
        :param select: Строка введенная пользователем
        :param min_value: Минимальное значения начала меню
        :param data: Список словарей с данными.
        :return: Числовое представление выбранного пункта меню
        """

        if isinstance(data,list) :
            for index,values in enumerate(data,start=min_value) :

                if self.get_value_key_dict(values,select) :
                   return index
        raise UnknownException (f"invalid data type : {self.select_title_validator.__name__}")



    def validator_input_path_absolut(self,str_input:str) :
        pass


    def validator_input(self,name_menu:str,question:str,requirement:str,data_type:str,input_method:str,
                        action:str,str_input:str|None,data:list[dict[str,str]],min_value:int,max_value:int) :
        """
        Метод для проверки введены ли корректно данные пользователем
        :param name_menu: Название меню в котором находится пользователь main_menu/sub_menu/.....
        :param question: Текст для поля ввода
        :param requirement: Дополнительное требование к конкретному действию
        :param data_type: Тип данных принимаемых данным пунктом меню
        :param input_method: принимает один из двух параметров one - может быть одно числовое значение для одного ключа,
                        two - может быть несколько значений для одного ключа.
        :param action: Необходимое действие для пункта меню.
        :param str_input: Строка с введенными данными от пользователя
        :param data: Словарь с данными для проверки на соответствие
        :param min_value: Минимально допустимое значение для ввода
        :param max_value: Максимально допустимое значение для ввода
        :return:
        """
        print('*** validator_input ***  ','data_type2 = ',data_type,' str_input2 = ',str_input,' action2 = ',action,' input_method = ',input_method)
        if str_input is not None and str_input.isdigit() :
            str_input = int(str_input)
            str_input = str(self.select_number_validator(str_input,min_value,max_value))
        if data_type == 'int':
            return None
        elif data_type == 'string' and input_method == 'one':
            if action == "save_file_config"  and requirement :
                return self.__checking_absolut_path(str_input,question)
            elif action == "save_file_config" :
                # Exit
                if str_input == '':
                    self.makes_exit()
                return str_input
            elif action == "add_file_config" and requirement :
                return self.__checking_absolut_path(str_input,question)
            elif action == "add_file_config" :
                # Exit
                if str_input == '':
                    self.makes_exit()
                return str_input
            return None
        elif data_type == 'string' and input_method == 'two':
            if action == "save_file_ignor" :
               return self.validator_ignor_add(question,str_input, input_method)
            return None
        elif data_type == 'all' and input_method == 'one':
            # Exit
            if str_input == '':
                self.makes_exit()
                return None
            if action == "modify_file_config" and requirement :
                str_input = self.validator_select(name_menu, data, str_input, min_value)
                return self.data_cls.LIST_LANGUAGE[int(str_input) - 1 ]
            elif action == "modify_file_config" :
                print(f"modify_file_config ")
                pass
            elif action is None or action == '':
                print('action = ', action)
                return self.validator_select(name_menu, data, str_input, min_value)
            return str_input
        elif data_type == 'all' and input_method == 'two':
            if action == "save_file_ignor" :
                return self.validator_ignor_add(question,str_input, input_method)
            elif action == "replace_files" :
                str_input, _ = self.__processed_line(str_input, input_method)
                data_replace = self.validator_replace(self.checking_values(str_input,input_method))
                # print('data_replace ==== ',data_replace)
                return self.check_selection(data_replace,'analysis')
            elif action == "delete_copies":
                str_input, _ = self.__processed_line(str_input, input_method)
                return  self.checking_values(str_input, input_method)
            elif action is None or action == '':
                return self.validator_select(name_menu, data, str_input, min_value)
            return 'заглушка'
        else :
            raise UnknownException (f'unidentified type : {self.validator_input.__name__}')


    def method_add_by_special_character(self,question:str,str_input:str|None) -> list[str]|None:
        """
        Метод для обработки проверки строки на содержание, обязательных спец символов для добавления в файл ignor
        :param question: Текст для поля ввода
        :param str_input: Строка с введенными данными от пользователя
        :return: Список строк для добавления в файл ignor
        """
        while True:
            if list_param_ignor := self.line_processing_ignore(str_input):
                return list_param_ignor
            else:
                # Exit
                if str_input == '' or str_input is None:
                    self.makes_exit()
                print(f"{self.files.show_translation("method_add_print")}")
                str_input = self.select(question)


    def validator_ignor_add(self,question:str,str_input:str|None,input_method:str) -> list[str]|None:
        """
        Метод проверяет корректность введенных данных при добавлении файлов в игнор для различных input_method
        :param question: Текст для поля ввода
        :param str_input: Строка с введенными данными от пользователя
        :param input_method: принимает один из двух параметров one - может быть одно числовое значение для одного ключа,
                        two - может быть несколько значений для одного ключа.
        :return:
        """
        if input_method == 'one' :
           return self.method_add_by_special_character(question,str_input)

        elif input_method == 'two' :
            files_add = []
            # Сначала нужно проверить есть ли в строке ключи типа frontend или backend
            new_str_input, _ = self.__processed_line(str_input, input_method)
            if  dict_param :=self.checking_values(new_str_input, input_method) :
                for keys, values in self.files.dict_copy().items():
                    for key,list_values  in dict_param.items():
                        if key == keys:
                            for value in list_values :
                                files_add.append('*' + self.files.delete_path(values[value]))
                return files_add
            else:
                return self.method_add_by_special_character(question, str_input)

        return None


    @staticmethod
    def select(question: str) -> str:
        """
        Метод для принятия данных от пользователя
        :param question: Текст вопроса который должен отображаться в поле для ввода.
        :return: Строковые данные которые ввел пользователь
        """
        return input(question).strip()


    @staticmethod
    def line_processing_ignore(string_ignore: str|list[str]|None) -> list|None:
        """
        Метод для обработки строки ввода для файла игнор
        :param string_ignore: Строка введенная пользователем
        :return: Список с игнорируемыми файлами и папками
        """
        new_list = []
        pattern = r'([/*](?:\\ |[^/*])+)'
        if isinstance(string_ignore,str) :
            string_ignore = string_ignore.strip()
            list_dir_file = re.findall(pattern,string_ignore )
            if  list_dir_file:
                for value in list_dir_file :
                    # Извлечем первый символ
                    symbol_tmp = value[0]
                    # уберем запятые
                    string_tmp = value[1:].strip().replace(',',' ')
                    # Соберем в список
                    list_tmp = string_tmp.split()
                    # Пробежимся по списку и добавим извлеченный символ
                    for item in list_tmp :
                        new_list.append(symbol_tmp + item)
                return new_list
            else:
                return None
        return string_ignore


    def get_yes_no(self,string:str) -> bool:
        """
        :param string: Строка с вопросом.
        :return: Возвращает True если 'Y' иначе False
        """
        string = str(string).lower().strip()
        while True:
            if string == 'y':
                return True
            elif string == 'n':
                return False
            else:
                string = input(f"{self.files.show_translation("get_yes_no_input")}")


    # переделать этот метод так как не правильно расставляются приоритеты при вводе данных
    def __input_string_processing(self, str_input:str) -> tuple[str,list[int]]:
        """
        Метод обрабатывает строку ввода данных. Расставляет данные в правильном порядке.
        :param str_input: Строка с данными.
        :return: Кортеж с обработанной строкой с данными в правильном порядке и со списком индексов ключей.
        """
        str_tmp = ''
        # К_О_С_Т_Ы_Л_Ь____S_T_A_R_T
        if str_input == 'all' :
            for key in self.files.dict_copy().keys() :
                str_tmp += key + str_input
        # К_О_С_Т_Ы_Л_Ь____E_N_D
        # Установим маркер для поиска нужных комбинаций наименования команд из строки
        marker_end = 'marker_end'
        str_input = str_input + marker_end

        # Добавим маркер в self.copy_folder на последнюю позицию
        tmp_copy_folder = self.files.copy_folder()
        tmp_copy_folder.append(marker_end)
        # Получим список индексов
        list_index = [str_input.find(index_tmp) for index_tmp in tmp_copy_folder if str_input.find(index_tmp) >= 0]

        # Соберем строку заново так как может быть не соблюден порядок ввода ключей.
        for ind in range(len(list_index) - 1):
            for ind_tmp in range(len(list_index)):
                if list_index[ind] >= list_index[ind_tmp]:
                    continue
                elif list_index[ind] < list_index[ind_tmp]:
                    str_tmp += str_input[list_index[ind]: list_index[ind_tmp]]
                    break
                # Получим список индексов снова
        str_input = str_tmp

        list_index = [str_input.find(index_tmp) for index_tmp in self.files.copy_folder() if str_input.find(index_tmp) >= 0]
        list_index.append(len(str_input) + 1)
        # Вернем обработанную строку и список индексов ключей.
        return str_input,list_index


    def __checking_all(self,str_input,input_method) :
        """
        Метод обрабатывает входящую строку с введенными параметрами от пользователя.
        Если в ней присутствует значение 'all', то это значение заменяется числовыми значениями.
        :param str_input: Строка с данными от пользователя.
        :param input_method: Значение two - обозначает что может быть передано несколько значений для одного ключа.
        :return: Возвращает строку с числовыми параметрами для каждого и ключей.
        """

        # Строка в правильном порядке с индексами положения ключей
        str_input,list_index = self.__input_string_processing(str_input)
        string_param_result = str_input
        for index,keys in enumerate(self.__current_folder(str_input)) :
            # Пробуем извлечь строку all если она есть
            string_tmp = re.match(Validator.PATTERN_WORD_ALL, str_input[len(keys) +
                                                               list_index[index]: list_index[index + 1]],re.IGNORECASE)
            if string_tmp is not None:
                if string_tmp.group() =='all' and input_method == 'two' :
                    values = self.files.dict_copy().get(keys)
                    list_param = []
                    for value in values.keys() :
                        list_param.append(str(value))
                    string_param_result = re.sub(keys + string_tmp.group(),keys +
                                                 ' '.join(list_param),string_param_result )

        return string_param_result


    def __current_folder(self,str_input:str) -> list[str]:
        """
        Метод для сбора актуальных ключей из строки ввода по которым, ищем наличие копий.
        :param str_input: Строка с данными от пользователя.
        :return: Список ключей для которых есть хоть одна копия
        """
        list_keys = []
        for keys, values in self.files.dict_copy().items():
            if len(values) > 0 and str_input.find(keys) >= 0:
                list_keys.append(keys)
        return list_keys


    def checking_selection_values(self,key_param,value_param,input_method,ind):
        """
        Метод проверяет чтоб значения не выходили за пределы допустимого диапазона, то есть значение не может быть
        более чем доступное количество копий.
        :param key_param: Ключ для которого сравниваются параметры.
        :param value_param: Числовое значение передаваемого параметра.
        :param input_method: Значение two - обозначает что может быть передано несколько значений для одного ключа.
        :param ind: Не обязательный параметр. Нужен только для input_method = "two".
        :return: Верное значение параметра.
        """
        min_value =  1 # НУЖНО ПОРАБОТАТЬ НАД ЭТИМ зНАЧЕНИЕМ ТАК КАК ОНО ВЯТО С ПОТОЛКА СЕЙЧАС
        int_inp = ''
        # print('input_method === ',input_method)
        # print('key_param = ', key_param)
        # print('value_param = ',value_param)
        len_list_key = len(list(self.files.dict_copy().get(key_param)))
        # print('self.dict_copy() = ',self.files.dict_copy(),' key_param = ',key_param)
        # print('len_list_key = ', len_list_key, ' dict_param ==== ', self.files.dict_copy())
        value_param = int(value_param)
        while min_value > value_param or value_param > len_list_key:
            if input_method == 'one':
                int_inp = input(f"{self.files.show_translation("checking_selection_input_start",key_param,
                                                               "from",min_value,"to",len_list_key,"enter_exit")}")
                int_inp = self.checking_digits(int_inp,min_value,len_list_key)
                if  min_value <= int_inp <= len_list_key :
                    return [int_inp]
            if input_method == 'two':
                # print('value_param = ',value_param)
                int_inp = input(f"{self.files.show_translation("checking_selection_input_start",key_param,
                   "from",min_value,"to",len_list_key,"checking_selection_input_method_two",ind + 1,"enter_exit")}")
                int_inp = self.checking_digits(int_inp,min_value,len_list_key )
            if input_method == 'two' and min_value <= int_inp <=  len_list_key  :
                return int_inp
        return value_param


    def __checking_enumeration(self, str_input, input_method ) :
        """
        Метод обрабатывает входящую строку с введенными параметрами от пользователя.
        Если в ней присутствует значение '-', то проверяются значения, которые находятся до и после символа '-'.
        Если перед символом '-' нет числа, а после есть, то берется диапазон от 0 до значения которое указанно
        после символа '-'.
        Если перед символом '-' есть число, а после нет, то берём диапазон от числа перед символом '-' до конца.
        Размер диапазона динамический и рассчитывается в зависимости от доступного числа копий для той или иной папки.
        :param str_input: Строка с данными от пользователя.
        :param input_method: Значение two - обозначает что может быть передано несколько значений для одного ключа.
        :return: Возвращает строку с числовыми параметрами для каждого и ключей.
        """
        # Строка в правильном порядке с индексами положения ключей
        str_input, list_index = self.__input_string_processing(str_input)
        string_param_result = str_input
        for index,keys in enumerate(self.__current_folder(str_input)) :
            list_tmp = []
            # Пробуем извлечь строку, с '-' если она есть
            string_tmp = re.match(Validator.PATTERN_DIGITS_MINUS, str_input[len(keys)  +
                                                         list_index[index]: list_index[index + 1]],re.IGNORECASE)
            if string_tmp is not None :
                if '-' in string_tmp.group()  and input_method == 'two':
                    tmp_param = string_tmp.group().split('-')
                    values = self.files.dict_copy().get(keys)
                    for ind ,value in enumerate(values,start=1) :
                        value = str(value)
                        if self.__isdigit(tmp_param[0]) and int(tmp_param[0]) > len(values) - 1:
                            tmp_param[0] = str(self.checking_selection_values(keys, tmp_param[0], input_method, 0))
                        if self.__isdigit(tmp_param[1]) and int(tmp_param[1]) > len(values) - 1:
                            tmp_param[1] = str(self.checking_selection_values(keys, tmp_param[1], input_method, 1))
                        # Оба пустые значения.
                        if not tmp_param[0] and not tmp_param[1] :
                            # print('Оба пустые значения.')
                            list_tmp.append(value)
                            continue
                        # Первое пустое второе нет
                        elif not tmp_param[0] and tmp_param[1] :
                            if self.__isdigit(tmp_param[1]) and ind <= int(tmp_param[1]):
                                list_tmp.append(value)
                                # print('Первое пустое второе нет.')
                                continue
                        # Первое не пустое второе пустое
                        elif tmp_param[0] and not tmp_param[1] :
                            # print('Первое не пустое второе пустое.',' ind = ',ind,' tmp_param[0] = ',tmp_param[0])
                            if self.__isdigit(tmp_param[0])  and  ind >= int(tmp_param[0]):
                                list_tmp.append(value)
                                continue
                        # Первое не пустое и второе не пустое
                        elif tmp_param[0] and  tmp_param[1] :
                            if self.__isdigit(tmp_param[0], tmp_param[1]) and int(tmp_param[0]) <= ind <= int(tmp_param[1]) :
                                # print('Первое не пустое и второе не пустое.')
                                list_tmp.append(value)
                                continue
                string_param_result = re.sub(keys + string_tmp.group(),keys + ' '.join(list_tmp),string_param_result)

        return string_param_result


    def checking_digits(self,number, min_value:int,max_value:int):
        if number.isdigit():
            number = int(number)
        else:
            while True:
                number = input(f"{self.files.show_translation("checking_digits_input_start",
                                                              min_value,"to",max_value," : ")}")
                if number.isdigit():
                    number = int(number)
                    break
        return number


    def __processed_line(self, str_input, input_method):
        """
        Метод содержит в себе все методы для поочередной обработки строки когда в строке содержаться перечисления.
        По итогу возвращает полностью готовую строку с параметрами для дальнейшей работы.
        :param str_input: Строка с данными от пользователя.
        :param input_method: Значение two - обозначает что может быть передано несколько значений для одного ключа.
        :return: Возвращает строку с числовыми параметрами для каждого и ключей.
        """
        good_string, list_index = self.__input_string_processing(str_input)
        if input_method == 'two':
            good_string = self.__checking_all(good_string, input_method)
            good_string = self.__checking_enumeration(good_string, input_method)
            # Соберем строку еще ра так как нужны правильные индексы ключей.
            good_string, list_index = self.__input_string_processing(good_string)
        return good_string, list_index


    def checking_values(self, str_input:str, input_method='one') -> dict[str,list[int]]:
        """
        Метод проверяет введены ли верные параметры при выборе копии для замены.

        :str_input: Строка с выбранным параметром возвращает метод selection.
        :input_method: принимает один из двух параметров one - может быть одно числовое значение для одного ключа,
                        two - может быть несколько значений для одного ключа.
        :return: Возвращает словарь с параметрами.
        """

        dict_param = {}
        input_method = input_method.lower()
        # Обработаем строку и вернем ее в нужном формате вместе со списком индексов
        str_input, list_index = self.__processed_line(str_input, input_method)
        # print('str_input = ', str_input, ' list_index = ', list_index)
        for index, keys in enumerate(self.__current_folder(str_input)):
            # print('str_input2222 = ', str_input, ' list_index2222 = ', list_index)
            if str_input.find(keys) >= 0:
                # Извлечём число из строки если оно есть
                string_tmp = re.findall(Validator.PATTERN_DIGITS,
                                        str_input[len(keys) + list_index[index]: list_index[index + 1]], re.IGNORECASE)
                # print(f'string_tmp {keys} dig = ', string_tmp)
                if input_method == 'one' and len(string_tmp) > 1:
                    dict_param[keys] = [-1]
                    break
                elif input_method == 'one' and len(string_tmp) == 1:
                    if len(string_tmp[0]) == '0':
                        dict_param[keys] = [-1]
                        break
                    else:
                        dict_param[keys] = [int(string_tmp[0])]
                        continue
                elif input_method == 'two' and len(string_tmp) >= 1:
                    for value in string_tmp:
                        if len(value) > 1:
                            if value[0] == '0':
                                dict_param[keys] = [-1]
                                break
                            else:
                                if keys in dict_param:
                                    dict_param[keys].append(int(value))
                                else:
                                    dict_param[keys] = [int(value)]
                        else:
                            if keys in dict_param:
                                dict_param[keys].append(int(value))
                            else:
                                dict_param[keys] = [int(value)]
                else:
                    dict_param[keys] = [-1]
        # backend0d75dfrontend2
        #  frontend2backend075d
        # backend075dfrontend23
        # frontend3backend2
        # frontend1,2,4 backend 1,3,4
        # ----- frontend1,23,4 backend 1,3,41
        for key, values in dict_param.items():
            for index, value in enumerate(values):
                for item, k in enumerate(self.files.dict_copy().keys()):
                    if k == key:
                        if input_method == 'one':
                            int_inp = self.checking_selection_values(key, value, input_method, index)
                            dict_param[key] = [int_inp]
                            # print('dict_param[key] = ', dict_param[key])
                        elif input_method == 'two':
                            # print('value========== ', value)
                            # print("values = ", values)
                            int_inp = self.checking_selection_values(key, value, input_method, index)

                            dict_param[key][index] = int_inp

        # print('dict_param = ', dict_param)
        return dict_param


    def check_selection(self, dict_param:Dict[str,list[int]],prefix:str) -> str|None :
        """
        Метод проверяет соответствие выбранных версий.
        :param dict_param: Словарь с номерами версий.
        :param prefix: Префикс - для идентификации файла и папки
        :return: Путь к файлу с копией проекта или None
        """
        checking_values = dict_param
        # Нужно первым делом собрать файл и проекта и сравнить с тем на который меняем, а после сравнения собранный файл
        # Удалить. Создать его с каким то маркером. Также нужно отслеживать что в списке в словаре не более одной цифры
        #  если более одной то уведомлять пользователя что замена возможна только на 1 копию. Реализовать запись в файл
        #  результатов анализа
        file_analysis = None
        dict_copy = self.files.dict_copy()
        # Нужно перебрать словарь и сделать сравнение текущей версии с заменяемой для этого необходимо создать копию, а затем ее удалить
        for key,value in checking_values.items() :
            # создаю копию
            self.files.create_file_copy_project(prefix)
            # Обновляю данные в словаре.
            # Первая копия это копия проекта которую будем сравнивать. А это значит что строки, которые отсутствуют
            # в заменяемом файле были добавлены
            new_dict_copy = self.files.dict_copy()[key][1]
            # выбираю копию
            selected_copy = self.files.dict_copy()[key][value[0]]
            # Получаю имя файла который будем менять
            # print('selected_copy = ',selected_copy )
            replacement_file_name = self.files.get_name_file(selected_copy)
            # Метод возвращает путь к файлу с результатами анализа
            file_analysis = self.files.file_analysis(key, new_dict_copy, selected_copy, 10)
            # print('file_analysis = ', file_analysis)
            if self.get_yes_no(input(f" {self.files.show_translation("check_selection_yes_no_input_start",
                replacement_file_name,"check_selection_yes_no_input_center","check_selection_yes_no_input_end")}")):
                try:

                    # print('file_analysis path = ',file_analysis )
                    if file_analysis := self.files.file_analysis(key, new_dict_copy, selected_copy,10) :
                        self.files.starting_file(file_analysis)
                        time.sleep(3)

                except Exception as e:
                    print(e)
                if self.get_yes_no(input(f"{self.files.show_translation("check_selection_get_yes_no_input")}")):
                    # Удаляю созданную копию и файл аналитики
                    self.files.delete_copies_analyst(file_analysis,prefix)
                    return selected_copy
                else:
                    return None
            if self.get_yes_no(input(f"{self.files.show_translation("check_selection_get_yes_no_input_next")}")):
                # Удаляю созданную копию и файл аналитики
                self.files.delete_copies_analyst(file_analysis,prefix)
                return selected_copy
        # Удаляю созданную копию и файл аналитики
        self.files.delete_copies_analyst(file_analysis,prefix)
        return None


    def validator_replace(self,dict_param:Dict[str,list[int]]) -> Dict[str,list[int]]|None:
        # Посчитаем количество одинаковых ключей
        for key,value in dict_param.items() :
           if len(value) > 1 :
               max_value = len(self.files.dict_copy()[key])
               print(f"{self.files.show_translation("validator_replace_print")}")
               string_inp = input(f"{self.files.show_translation("validator_replace_input_start",key,
                                              "validator_replace_input_center",max_value,"enter_exit")} ")
               string_inp = self.checking_digits(string_inp,1,max_value)
               string_inp = self.checking_selection_values(key,string_inp,'one',0)
               # Увеличиваем значение на единицу так как будет создана новая копия для сравнения
               dict_param[key] = [int(string_inp) + 1]
           else:
               # Извлечем номер копии и словаря и сместим его на единицу в большую сторону
               int_value = dict_param.get(key)[0]
               dict_param[key] = [int_value + 1]
        return dict_param


    @staticmethod
    def makes_exit() :
         raise UnknownException ('EXIT')


    def __checking_absolut_path(self,str_input:str,question:str) -> str:
        """
        Метод для проверки введен ли абсолютный путь.
        Если введен не абсолютный путь, то дает возможность
        пользователю указать верный абсолютный путь.
        :param str_input: Строка введенная пользователем.
        :param question: Текст вопроса для поля ввода данных.
        :return: Строку с абсолютным путем
        """
        # Проверим, является ли путь абсолютным
        while True:
            if self.files.path_absolut_check(str_input):
                return str_input
            else:
                # Exit
                if str_input == '':
                    self.makes_exit()
                print(f"{self.files.show_translation("checking_absolut_path_print")}")
                str_input = self.select(question)