# Класс для работы с файлами
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red, green, black
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from mygit.data_class import Data
from .unknownexception import UnknownException
from datetime import datetime
from pathlib import Path
import platform
import subprocess
import os
import shutil
import difflib

class Files :

    # Имя конфигурационного файла
    NAME_FILE_CONFIG = '../my_git_config'
    # Список обязательных полей для конфигурационного файла
    LIST_PARAM_CONFIG = ["path_to_project_folder_default :", "path_to_project_copies_folder_default :"]
    NAME_FILE_IGNOR = '.my_git_ignor'
    FILE_ANALYSIS_RESULT = 'Files_analysis_result_'
    TEXT_FILE_NAME = '[file name]: ' # для разграничения файлов, указывается имя файла и путь к нему не абсолютный
    TEXT_FILE_CONTENT = '[file content begin]'  # Начало файла
    TEXT_FILE_END = '[file content end]'  # Конец файла
    NAME_FOLDER_SAVE_COPY = 'Copy_code_'  # Часть имени директории где будет храниться файл с кодами проекта
    ADDED = '  Added   '
    ABSENCE = '  Absence '
    PATTERN_DATA = r"\d{4}-\d{2}-\d{2}"
    __EXTENSION_FILE = '.txt'  # Закрытая переменная
    __EXTENSION_FILE_ANALYSIS = '.pdf'
    def __init__(self):
        self.data_cls = Data()


    # закрою доступ к изменению переменной
    def __setattr__(self, key, value):
        if key == '_MyGit__EXTENSION_FILE' and hasattr(self, '_MyGit__EXTENSION_FILE'):
            raise AttributeError("Нельзя изменить значение __EXTENSION_FILE")
        object.__setattr__(self, key, value)


    @property
    def len_path_read_dir(self):
        return len(self.path_folder_project().strip()) if isinstance(self.path_folder_project(), str) else 0


    @property
    def len_name_file(self):
        return len(self.get_name_project()) if isinstance(self.get_name_project(), str) else 0


    @property
    def len_text_file_name(self):
        return len(self.data_cls.clear_space(Files.TEXT_FILE_NAME)) if isinstance(Files.TEXT_FILE_NAME, str) else 0


    @property
    def len_extension(self):
        return len(Files.__EXTENSION_FILE) if isinstance(Files.__EXTENSION_FILE, str) else 0


    @staticmethod
    def pwd() -> str :
        """
        Метод для получения пути к текущему каталогу
        :return: Путь текущего каталога
        """
        return os.getcwd()


    @staticmethod
    def search_file(path:str,file_name:str) -> bool:
        """
        Метод для проверки существования файла
        :param path: Путь к файлу
        :param file_name: Имя файла
        :return: True - файл найден, False - файл не найден
        """
        total_path = os.path.join(path,file_name)
        if os.path.exists(total_path):
            return True
        return False


    @staticmethod
    def create_dir(path_dir:str)-> None :
        # Проверим существование директории для записи в нужном месте
        if not os.path.exists(path_dir):
            # Создадим нужную директорию если ее нет
            os.mkdir(path_dir)


    @staticmethod
    def create_dirs(path_dir:str) -> None :
        # Проверим существование директории для записи в нужном месте
        if not os.path.exists(os.path.join(path_dir)):
            os.makedirs(os.path.join(path_dir))


    @staticmethod
    def create_file(path:str,file_name:str) -> None:
        """
        метод для создания файла если он отсутствует
        :param path: Путь к категории
        :param file_name: Имя файла
        :return: None
        """
        total_path = os.path.join(path,file_name)
        if not os.path.exists(total_path):
            open(total_path, 'x').close()


    @staticmethod
    def delete_file(path_file:str) -> None:
        """
        Метод удаляет файл по указанному пути.
        :param path_file: Путь удаляемому файлу.

        """
        if os.path.exists(path_file):
            os.remove(path_file)


    def create_absolut_path(self,name_folder:str) -> str :
        """
        Метод для создания абсолютного пути
        :param name_folder: Имя создаваемой папки
        :return: абсолютный путь
        """
        return os.path.join(self.pwd(),name_folder)


    def field_contents_presence(self,path: str, file_name: str) -> list[tuple[bool,str]] :
        """
        Метод проверяет наличие содержимого обязательных полей в конфигурационном файле
        :param path: Путь к файлу
        :param file_name: Имя файла
        :return: True - все поля есть в файле, List - список отсутствующих полей
        """
        # Полный путь к конфигурационному файлу.
        total_path = os.path.join(path, file_name)
        list_result = []
        clear_line = None
        # Откроем файл и прочитаем
        with open(total_path, 'r') as file:
            read_file = file.readlines()
            for value in Files.LIST_PARAM_CONFIG:
                for line in read_file:
                    clear_line = line.strip()
                    if value in clear_line and self.field_status(clear_line,value):
                        list_result.append([True,clear_line])
                        break
                if  clear_line is None :
                    list_result.append([False, value])
                elif not value in clear_line :
                    list_result.append([False,value])
            return list_result


    @staticmethod
    def field_status(contents: str, name_field: str) -> bool:
        """
       Метод проверяет заполнено ли обязательное поле в конфигурационном файле
       :param contents: Содержимое обязательного поля
       :param name_field: Название проверяемого поля
       :return: True - поле заполнено, False - поле пустое
       """
        len_contents = len(contents.strip())
        len_name_field = len(name_field)
        if len_contents > len_name_field:
            return True
        return False


    @staticmethod
    def get_name_file(total_path:str) -> str :
        """
        Метод для извлечения базового имени файла
        :param total_path: Полный путь к файлу с его именем
        :return: Базовое имя файла без пути
        """
        return os.path.basename(total_path)


    def configuration_file_state(self,path: str, file_name: str) -> bool:
        """
        Метод проверяет состояние конфигурационного файла
        :param path: Путь к файлу
        :param file_name: Имя файла
        :return:
        """
        field_presence = self.field_contents_presence(path,file_name)
        if isinstance(field_presence,list) :
            path_extraction = self.path_extraction(field_presence)
            if  not self.path_absolut_check(path_extraction)  :
                print(f'Введенный путь {path_extraction} не верный')
                return False
            else:
                return True
        else:
            # Проверяем заполнены ли поля
            pass


    def field_contents(self,path: str, file_name: str) -> bool:
       """
       Метод проверяет наличие корректного пути в указанном поле
       :return:
       """
       field_presence = self.field_contents_presence(path, file_name)
       if isinstance(field_presence, list):
           pass
       else:
           raise UnknownException (f'unidentified type : {self.field_contents.__name__}')


    @staticmethod
    def path_extraction(field_data:list[tuple[bool,str]]) -> str|None:
        """
        Метод для извлечения пути из конфигурационного файла
        :param field_data: Список списков с данными о поле
        :return: str - список списков если поле в файле найдено, None - поля не найдены
        """
        for data in field_data :
            if data[0] :
                for name_field in Files.LIST_PARAM_CONFIG :
                    if name_field in data[1] :
                        path = data[1].replace(name_field,'').strip()
                        return path
        return None


    @staticmethod
    def path_absolut_check(path:str) -> bool:
        """
        Метод проверяет, является ли путь абсолютным и папкой
        :param path: Путь который нужно проверить
        :return: True or False
        """

        return os.path.isabs(path) and os.path.isdir(path)


    @staticmethod
    def save_data_file(path:str,file_name:str,data:str) -> None:
        """
        Метод для записи в файл
        :param path: Путь к файлу
        :param file_name: Имя файла
        :param data: Данные для записи
        :return: None
        """
        total_path = os.path.join(path,file_name)
        with open(total_path,"a") as file :
            file.write(data + '\n')



    def path_folder_copies(self) -> str :
        """
        Метод для получения пути к папке хранения копий проекта.
        Файл ignor храниться в той же папке, что и копии проекта
        :return: Путь к папке с файлом ignor
        """
        search_field = "path_to_project_copies_folder_default :"
        return self.path_project_field(search_field)


    def path_folder_project(self) -> str :
        """
        Метод для получения пути к папке хранения отслеживаемого проекта.
        :return: Путь к папке с файлом ignor
        """
        search_field = "path_to_project_folder_default :"
        return self.path_project_field(search_field)


    def path_project_field(self,search_field:str) -> str :
        """
        Метод для получения пути к необходимой папке из конфигурационного файла
        :param search_field: Искомое поле в конфигурационном файле
        :return: Путь к папке с копией проекта
        """

        path_file_config = os.path.join(self.pwd(),self.NAME_FILE_CONFIG)
        with open(path_file_config, 'r') as file :
            for line in file :
                if  search_field in line :
                    return line.replace( search_field,'').strip()
            return ''


    def add_ignore(self,data_ignore:list) -> list:
        """
        Метод добавляет в файл игнорируемые файлы и папки
        :param data_ignore: Список с данными которые необходимо добавить в ignor '/'- папка, '*' - файл
        :return: Список с игнорируемыми файлами и папками
        """
        list_tmp = []
        path_file_ignor = os.path.join(self.path_folder_copies(),self.NAME_FILE_IGNOR)
        # Прочитаем файл и добавим содержимое в множество.
        with open(path_file_ignor, 'r') as f_ignor:
            for item_file in f_ignor:
                item_file = item_file.strip()
                if not item_file in list_tmp:
                    list_tmp.append(item_file)
        for item_list in data_ignore:
            item_list = item_list.strip()
            if not item_list in list_tmp:
                list_tmp.append(item_list)
        # Откроем файл и запишем в него данные
        list_tmp = sorted(list_tmp, key=lambda x='/': x, reverse=True)
        with open(path_file_ignor, 'w') as file_new_data:
            for new_data in list_tmp:
                file_new_data.write(new_data + '\n')
        return list_tmp


    def changing_default_fields(self,line_file:str,new_line:str) -> str:
        """
        Метод для перезаписи данных в файле
        :param line_file: Текущая строка и файла
        :param new_line: Новая строка которую необходимо записать
        :return: Строку для записи.
        """
        # Если найдена строка должны сверить ее содержимое и перезаписать его
        for value in self.LIST_PARAM_CONFIG :
            if value in line_file :
                if new_line is not None and value in new_line:
                    if line_file != new_line :
                        return new_line

        return line_file


    def file_modification(self,path:str,file_name:str,new_line:str) -> None:
        """
        Метод для перезаписи определенных данных в файле
        :param path: Путь к файлу
        :param file_name: Имя файла
        :param new_line: Строка с новыми данными
        :return: None
        """
        if isinstance(new_line,str) :
            total_path = os.path.join(path, file_name)
            with open(total_path,'r') as file :
                lines = file.readlines()
                with open(total_path,'w+') as mod_file :
                    for line in lines :
                        mod_line = self.changing_default_fields(line.strip(),new_line.strip())
                        mod_file.write(mod_line + '\n')


    @staticmethod
    def field_presence(path: str, file_name: str,fields:list[str]) -> list[tuple[bool,str]]  :
        """
        Метод проверяет наличие обязательного поля в файле
        :param path: Путь к файлу
        :param file_name: Имя файла
        :param fields: Список обязательных полей
        :return:
        """
        # Полный путь к конфигурационному файлу.
        total_path = os.path.join(path, file_name)
        list_result = []
        clear_line = None
        # Откроем файл и прочитаем
        with open(total_path, 'r') as file:
            read_file = file.readlines()
            for value in fields:
                for line in read_file:
                    clear_line = line.strip()
                    if value in clear_line :
                        list_result.append([True, value])
                        break
                if clear_line is None:
                    list_result.append([False, value])
                elif not value in clear_line:
                    list_result.append([False, value])
            return list_result


    def action_file(self,path:str,file_name:str,field:str,save_data:str) -> bool :
        """
        Метод для определения необходимого действия с обязательным полем.
         Записать новую строку или модифицировать уже существующую.
        :param path: Путь к файлу
        :param file_name: Имя файла
        :param field: Наименование поля
        :param save_data: Данные которые необходимо записать
        :return:
        """
        self.create_file(self.pwd(),self.NAME_FILE_CONFIG)
        for item in self.field_presence(path,file_name,self.LIST_PARAM_CONFIG) :
            if field in item[1] :
                if item[0] :
                    self.file_modification(self.pwd(), self.NAME_FILE_CONFIG, save_data)
                else:
                    self.save_data_file(self.pwd(), self.NAME_FILE_CONFIG, save_data)
        return True


    @staticmethod
    def get_data_ignor(path:str,file_name:str,separator:str) -> list[str]:
        """
        Метод для сбора в словарь данных по разделителю
        :param path: Путь к файлу
        :param file_name: Имя файла
        :param separator: Разделитель по которому производится поиск
        :return: Список игнорируемых папок
        """
        total_path = os.path.join(path, file_name)
        list_data = []
        with open(total_path , 'r') as file :
            for line in file :
                if line[0] == separator :
                    list_data.append(line[1:].strip())
            return list_data


    def get_name_project(self) -> str:
        """
        Метод для извлечения имени проекта из пути в необходимом формате
        :return: Имя проект в необходимом формате
        """
        if self.path_folder_project()[-1] == '/':
            name_project = os.path.basename(self.path_folder_project()[:-1])
        else:
            name_project = os.path.basename(self.path_folder_project())
        if name_project[-1] != '_' :
            name_project += '_'
        return name_project.replace(' ','_')


    def copy_file(self, path_original, path_copy_dir):
        """
        Метод копирует файлы в нужную директорию если директории не существует то он ее создаёт.
        :param path_original: Абсолютный путь к оригинальному файлу.
        :param path_copy_dir: Путь к директории в которую будет производиться копирование.
        :return:
        """
        # От path_original нужно отрезать часть, которая содержится в self.path_folder_project().
        part_path_original = path_original[
                             self.len_path_read_dir + 1: len(path_original) - len(os.path.basename(path_original))]
        total_path_copy_files = os.path.join(path_copy_dir, part_path_original)
        if not os.path.exists(total_path_copy_files):
            os.makedirs(total_path_copy_files)

        shutil.copy2(path_original, str(total_path_copy_files))


    def folder_ignor(self) -> list[str]:
        """
        Метод для сбора игнорируемых папок
        :return: Список игнорируемых папок
        """
        return self.get_data_ignor(self.path_folder_copies(),self.NAME_FILE_IGNOR,'/')


    def files_ignor(self) -> list[str]:
        """
        Метод для сбора игнорируемых файлов
        :return: Список игнорируемых файлов
        """
        return self.get_data_ignor(self.path_folder_copies(),self.NAME_FILE_IGNOR,'*')


    def copy_folder(self):
        """
        Метод для сбора списка копируемых директорий.
        :return: Список копируемых директорий
        """
        dir_copy = []
        for directories in os.listdir(self.path_folder_project()):
            item_path = os.path.join(self.path_folder_project(), directories)
            # Исключаем указанные директории
            if directories not in self.folder_ignor():
                if os.path.isdir(item_path):
                    dir_copy.append(directories)
        return dir_copy


    def create_file_copy_project(self,prefix = '') -> None:
        """
        Метод создает текстовый файл который, содержит коды всех файлов проекта.
        Кроме, тех файлов и папок которые добавлены в файл ignor.
        :param prefix: Добавление к имени для дальнейшей идентификации при удалении созданной копии для анализа файлов
        :return:
        """
        # backend1frontend0
        prefix_data_time = datetime.now()
        prefix_data = datetime.date(prefix_data_time)
        # Обход всех поддиректорий и файлов
        for root, directories, files in os.walk(self.path_folder_project()):
            # Исключаем указанные директории
            directories[:] = [d for d in directories if d not in self.folder_ignor()]
            # Исключаем файлы, содержащие определенные подстроки
            filtered_files = [file for file in files if not any(sub in file for sub in self.files_ignor())]
            for file in filtered_files:
                for name_folder in self.copy_folder() :
                    if root.find(name_folder) >= 0:
                        # путь к директории в которую буду записывать файл
                        new_path_save_dir = os.path.join(self.path_folder_copies(),
                                                         f'{self.NAME_FOLDER_SAVE_COPY}{prefix_data}{prefix}')
                        # Имя файла для записи
                        name_file_save = (f'{self.get_name_project()}{name_folder}_'
                                          f'{prefix_data_time.strftime("%Y-%m-%d %H-%M")}{prefix}{Files.__EXTENSION_FILE}')
                        path_and_name_file_save = os.path.join(new_path_save_dir,name_file_save)
                        # Путь к папке в которую копируем файлы
                        path_coy_files =  os.path.join(new_path_save_dir,
                                f'{name_folder}_{prefix_data_time.strftime("%Y-%m-%d %H-%M")}{prefix}')
                        # Создадим основную папку если ее нет.
                        self.create_dir(new_path_save_dir)
                        # Если файла нет, то создадим его в директории для записи.
                        self.create_file(new_path_save_dir,name_file_save)
                        # Копируем файлы в созданную директорию.
                        self.copy_file(os.path.join(root,file),path_coy_files)
                        try :
                            # Откроем интересующий нас файл для копирования если он существует
                            if os.path.exists(os.path.join(root, file)):
                                # Для начала проверим не пустой ли файл.
                                file_size = os.path.getsize(os.path.join(root, file))
                                if file_size != 0  :
                                    with open(os.path.join(root, file), 'r' ) as file_read:
                                        # начнем читать этот файл по строчно, но для начала откроем файл для записи
                                        with open(path_and_name_file_save, 'a' ) as file_save:
                                            file_read_lines = file_read.readlines()
                                            # Запишем первые строки
                                            file_save.write(f'\n{Files.TEXT_FILE_NAME} '
                                                 f'{os.path.join(root[len(self.path_folder_project()) + 1:], file)}\n')
                                            file_save.write(f'{Files.TEXT_FILE_CONTENT} \n')
                                            for line in   file_read_lines :
                                                # Читаем файл построчно и записываем в свой файл также построчно
                                                file_save.write(line)
                                            # Запишем последнюю строку для текущего файла который копировали
                                            file_save.write(f'\n{Files.TEXT_FILE_END} \n')
                        # заглушим ошибку
                        except UnicodeDecodeError :
                             pass


    def get_path_to_file_being_built(self,root:str,directory:str,file_name:str) -> list[list[str]] :
        """
        Метод для извлечения путей к создаваемым файлам из копии
        :return: Список со списками путь, имя файла
        """
        list_path = []
        with (open(os.path.join(root, directory, file_name), 'r+') as file_tmp):
            for line in file_tmp:
               if line.find(Files.TEXT_FILE_NAME) >= 0:
                    # Нужно разобрать эту строку и получить из нее название папки и имя
                    dir_name = os.path.dirname(self.data_cls.clear_space(line)
                                               [self.len_text_file_name:])
                    path_tmp = Path(line)
                    file_name_tmp = path_tmp.name
                    path_main_directory = str(os.path.join(root, directory,
                                                           file_name[self.len_name_file:len(
                                                               file_name) - self.len_extension],
                                                           dir_name))
                    list_path.append([line,path_main_directory,file_name_tmp.strip()])

            return list_path


    # ЗАКРЫТЬ ЭТОТ МЕТОД
    def file_collector(self):
        """
        Метод собирает из файла копии назад в папки/файлы
        :return: список имен файлов вместе с папкой
        """
        # зайдем по указанному пути и найдем интересующую нас папку, которая начинается на Code
        for root, directories, files in os.walk(self.path_folder_copies()):
            for d in directories:
                if d.find(Files.NAME_FOLDER_SAVE_COPY) == 0:
                    # Найдем файл в имени которого присутствует self.name_file.
                    for file in os.listdir(str(os.path.join(root, d))):
                        if file.find(self.get_name_project()) >= 0:
                            # Переберем список с данными и совершим действия с этими файлами
                            # index 0 - Строка и файла содержащая TEXT_FILE_NAME
                            # index 1 - Абсолютный путь к файлу без имени файла
                            # index 2 - Имя файла.
                            # Начнем читать файл с копией файлов
                            with (open(os.path.join(root, d, file), 'r+') as file_tmp):
                                for list_param in self.get_path_to_file_being_built(root,d,file) :
                                    # Соберем путь к файлу
                                    file_path = os.path.join(list_param[1],list_param[2])
                                    # Удалим файл если он есть
                                    self.delete_file(file_path)
                                    # Создадим файл и будем в него записывать
                                    with open(file_path,'w+',encoding='utf-8') as new_file :
                                            for line in file_tmp :
                                                if list_param[0] == line or Files.TEXT_FILE_CONTENT == line.strip():
                                                    continue
                                                elif line.strip() == Files.TEXT_FILE_END :
                                                    new_file.close()
                                                    break
                                                else:
                                                    new_file.write(line)

    def dict_copy(self):
        """
        :return: возвращает словарь с доступными копиями проекта. Вместе с путем к ним
        """
        dict_tmp = {}
        list_name = []
        for root, directories, files in os.walk(self.path_folder_copies()):
            # Исключаем указанные директории
            directories[:] = [d for d in directories if d not in self.folder_ignor()]
            for d in directories:
                if d.find(Files.NAME_FOLDER_SAVE_COPY) == 0:
                    # Найдем файл в имени которого содержится self.name_file
                    for file in os.listdir(str(os.path.join(root, d))):
                        if not file in self.files_ignor():
                            if file.find(self.get_name_project()) >= 0:
                                list_name.append(os.path.join(root, d, file))

        for keys in self.copy_folder():
            dict_tmp[keys] = {}
            key = 1
            index_tmp = len(list_name)
            for _, value in zip(range(index_tmp), sorted(list_name, reverse=True)):
                if value.find(keys) >= 0:
                    dict_tmp[keys][key] = value
                    key += 1

        return dict_tmp



    def delete_path(self,value:str) -> str:
        """
        Метод убирает путь к файлу.
        :value: Имя файла с полным путем.
        :return: Чистое имя файла без пути

        """
        find_name_file = value.find(self.get_name_project())
        return value[find_name_file : ]


    def __delete_folder(self,path_file,key_file) -> None:
        """
        Метод удаляет папку по указанному пути.
        :param path_file: Путь к файлу с копией проекта.
        :param key_file: Ключ по которому будет происходить удаление.

        """
        # Получим дату и время из имени файла.
        file_date_time = self.data_cls.get_data_or_datatime(self.data_cls.PATTERN_DATA_TIME,path_file)
        # Получим путь к удаляемой папке.
        number_position_file_name = path_file.find(self.get_name_project())
        path_folder  = os.path.join(path_file[ : number_position_file_name - 1],key_file + '_' + file_date_time )
        if os.path.exists(path_folder) :
            shutil.rmtree(path_folder)


    def __delete_empty_folder(self) -> None:
        """
        Метод удаляет папку по указанному пути если она пустая.
        """
        if os.path.exists(self.path_folder_copies()) :
            for folder in os.listdir(self.path_folder_copies()) :
                if folder.find(Files.NAME_FOLDER_SAVE_COPY) >= 0 :
                    path_dir = os.path.join(self.path_folder_copies(),folder)
                    if os.path.isdir(path_dir) and len(os.listdir(path_dir)) == 0:
                        shutil.rmtree(path_dir)


    def delete_copies(self,dict_data):
        """
        Метод удаляет указанную папку с копией проекта.
        :param dict_data: Словарь с удаляемыми копиями

        """
        # backend0d75dfrontend2
        #  frontend2backend075d
        # backend075dfrontend23
        # frontend3backend2
        # frontend1,2,4 backend 1,3,4
        # frontend1,23,4 backend 1,3,41
        # backend kjlkj 1
        # Словарь с копиями проекта
        dict_copies = self.dict_copy()
        # Получим имя файла по ключу
        for key_dict_data , values_dict_data in dict_data.items() :
            for value_dict_data  in values_dict_data :
                for key_dict_copies,value_dict_copies in dict_copies.get(key_dict_data ).items():
                    if value_dict_data == key_dict_copies :
                         self.__delete_folder(value_dict_copies,key_dict_data)
                         self.delete_file(value_dict_copies)
                         self.__delete_empty_folder()


    def file_analysis(self, key_file_for_analysis:str, path_file_for_analysis:str, path_next_file:str,size_text:int) -> str|None:
        """
        Метод создает аналитический файл для сравнения. После файл удаляется за ненадобностью при переходе
        к следующему действию.
        :param key_file_for_analysis: Ключ добавленный к имени файла в моем примере это 'frontend' или 'backend'.
        :param path_file_for_analysis: Путь к файлу который, будем анализировать.
        :param path_next_file: Путь к файлу с которым будем сравнивать.
        :param size_text: Размер шрифта текста
        :return: Путь к файлу с результатом анализа
        """
        # backend1frontend0
        # Регистрация шрифта с поддержкой кириллицы (например, DejaVuSans)
        pdfmetrics.registerFont(TTFont('ComicRelief-Regular', '../Comic_Relief/ComicRelief-Regular.ttf'))
        name_file_for_analysis = self.get_name_file(path_file_for_analysis)
        name_file_next_file = self.get_name_file(path_next_file)
        # Извлечем часть пути, а именно уберем название файла
        part_path = os.path.dirname(path_next_file)
        # Извлечем дату из названия файла
        data_file_for_analysis = self.data_cls.get_data_or_datatime(Files.PATTERN_DATA, name_file_next_file)
        # Путь к файлу с результатами анализа файлов
        path_file_result_analysis = os.path.join(part_path,
                                                 Files.FILE_ANALYSIS_RESULT + key_file_for_analysis + '_' +
                                                 data_file_for_analysis + Files.__EXTENSION_FILE_ANALYSIS)

        # Откроем файлы на чтение и начнем анализировать результат будем писать в папку с тем файлом на который
        # хотели заменить, потом этот файл удалим
        # try:
        list_diff_lines = self.line_difference_generator(path_file_for_analysis, path_next_file)

        if  list_diff_lines[0] :
            print('Файлы имеют разное содержимое !!!')
            list_text_header_file_analysis = ['File analysis :', name_file_for_analysis,
                                              'and', name_file_next_file]
            lines_header = self.file_result_analysis_header(name_file_for_analysis,
                                                            name_file_next_file,list_text_header_file_analysis)

            list_diff_lines[1] = lines_header + list_diff_lines[1]

            # Создаем PDF
            c = canvas.Canvas(path_file_result_analysis, pagesize=letter)
            width, height = letter
            y_position = height - 40  # Начальная позиция Y (сверху)

            # Устанавливаем шрифт
            c.setFont('ComicRelief-Regular', size_text)


            for index,(text, color, strike) in enumerate(list_diff_lines[1]):
                # Устанавливаем цвет
                c.setFillColor(color)
                if index < 1:
                    self.draw_header(size_text,text,y_position,width,c)
                # Записываем текст

                c.drawString(30, y_position, text)
                if strike:
                    # Определяем длину текста
                    text_width = c.stringWidth(text, 'ComicRelief-Regular', size_text)
                    # Рисуем линию поверх текста
                    c.setStrokeColor(color)  # Цвет линии совпадает с цветом текста
                    c.setLineWidth(1)
                    c.line(30, y_position + 2, 30 + text_width, y_position + 2)
                # Переносим строку
                y_position -= 15

                # Проверяем, не вышли ли за пределы страницы
                if y_position < 40:
                    c.showPage()
                    y_position = height - 40
                    c.setFont('ComicRelief-Regular', size_text)

            # Сохраняем PDF
            c.save()
            return path_file_result_analysis
        else:
            print('Файлы имеют одинаковое содержимое !!!')
            return None


    def delete_copies_analyst(self, path_file_analysis:str|None,prefix:str) -> None :
        """
        Метод для удаления файлов и папок созданных для сравнения
        :param path_file_analysis: Путь к файлу с аналитикой
        :param prefix: prefix - добавленный к имени файла для идентификации при необходимости
        :return: None
        """
        print('print()',self.dict_copy().keys())
        for keys, values in self.dict_copy().items():
            for key , val in values.items():
                if val.find(prefix) >= 0 :
                    print('keys = ', key)
                    print('values[0] = ', val)
                    self.delete_copies({keys: [key]})
                if path_file_analysis is not None :
                    self.delete_file(path_file_analysis)


    @staticmethod
    def draw_header(size_text:int,text:str,position_y:int,width,obj_canvas):
        """
        Метод для центрирования заголовка
        :param size_text: Размер шрифта
        :param text: Текст который необходимо центрировать.
        :param position_y: Расположения текста по y-координате
        :param width: Ширина
        :param obj_canvas: Объект класса Canvas
        :return:
        """
        obj_canvas.setFont('ComicRelief-Regular', size_text)
        text_width = obj_canvas.stringWidth(text, 'ComicRelief-Regular', size_text)
        star_width = obj_canvas.stringWidth("*", 'ComicRelief-Regular', size_text)
        total_stars = int((width - text_width) / (2 * star_width))
        left_stars = "*" * total_stars
        right_stars = "*" * total_stars
        full_line = f"{left_stars} {text} {right_stars}"
        obj_canvas.drawCentredString(width / 2, position_y, full_line)


    @staticmethod
    def file_result_analysis_header(file_base_name:str, file_patch_name:str,string_status:str|list[str]) -> list:
        len_file_base = len(file_base_name)
        len_file_patch = len(file_patch_name)
        if len_file_base > len_file_patch:
            len_default = len_file_base
        else:
            len_default = len_file_patch
        total_width_default = len_default + 50
        list_header = []
        if (isinstance(string_status, list) and
                all(isinstance(item, str) for item in string_status)):
            list_header.append((f"{'*' * total_width_default}",black,False))
            list_header.append((f"**{''.center(total_width_default - 4)}**",black,False))
            for text in string_status:
                list_header.append((f"**{text.center(total_width_default - 4)}**",black,False))
                list_header.append((f"**{''.center(total_width_default - 4)}**",black,False))
            list_header.append((f"{'*' * total_width_default}",black,False))
        elif isinstance(string_status, str):
            count_symbol = (total_width_default - len(string_status)) // 2
            list_header.append((f"{'<' * count_symbol}{string_status}{'>' * count_symbol}",black,False))
            return list_header
        else:
            raise ValueError(f'Не верный параметр в функции : {Files.file_result_analysis_header.__name__} ')
        return list_header


    @staticmethod
    def line_difference_generator(path_base_file:str, path_patch_file:str) ->list[list]:
        """
        Метод построчно сравнивает два файла и в результате возвращает строку которая, отсутствует в
        заменяемом файле либо наоборот была добавлена в заменяемый файл.
        :param path_base_file: Путь к заменяемому файлу.
        :param path_patch_file: Путь к исходному файлу (Файл который соответствует текущей версии файла).
        :return: Строка, которая была добавлена или наоборот отсутствует и номер строки
        """

        list_diff_lines = [[],[]]
        with open( path_base_file, 'r') as base_file, open(path_patch_file, 'r') as patch_file:

            diff = difflib.ndiff(base_file.readlines(), patch_file.readlines())

        for i, line in enumerate(diff):
            if line[:2].count('-') == 1 :
                line_add = line[1:].strip()
                if line_add != '' :
                    if not list_diff_lines[0] :
                        list_diff_lines[0].append('absense')
                    list_diff_lines[1].append((line_add.strip(), red, True))

            elif line[:2].count('+') == 1 :
                line_add = line[1:].strip()
                if line_add != '':
                    if not list_diff_lines[0]:
                        list_diff_lines[0].append('added')
                    list_diff_lines[1].append((line_add.strip(), green, False))
            else:
                list_diff_lines[1].append((line.strip(), black, False))
        return list_diff_lines


    @staticmethod
    def starting_file(path_file:str) -> None:
        """
        Метод для открытия файла в программе по умолчанию для разных операционных систем.
        :param path_file: Путь к файлу который нужно запустить
        """
        # Определим какая операционная система и на основании этого будем открывать файл.
        system = platform.system()
        try:
            if system == 'Windows':
                os.startfile(path_file)
            elif system == 'Linux':
                subprocess.run(["xdg-open", path_file], stderr=subprocess.DEVNULL, check=True)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", path_file], check=True)
        except:
            raise Exception(f'Не известная ОС. Файл не открыт')



    def replacing_files(self,path_files:str|None) -> None:
        if path_files is not None :
            # Путь к папке которую нужно переместить
            path_files = path_files.replace(self.get_name_project() ,'').replace(Files.__EXTENSION_FILE,'')
            shutil.copytree(path_files, self.path_folder_project(), symlinks=False, ignore=None,
                            copy_function=shutil.copy2, ignore_dangling_symlinks=False,
                            dirs_exist_ok=True)



# f =Files()
# base = '/home/max/PythonProject/test/Copy_code_2025-05-10/project_deepseek_frontend_2025-05-10 12-43.txt'
# no_base =  '/home/max/PythonProject/test/Copy_code_2025-05-10/project_deepseek_frontend_2025-05-10 10-06.txt'
# f.line_difference_generator(base ,no_base)