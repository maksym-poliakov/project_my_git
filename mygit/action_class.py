# Класс для обработки выбранных действий
from .unknownexception import UnknownException
from .files_class import Files
from .data_class import Data

class Action:

    def __init__(self):
        self.files = Files()
        self.data_cls = Data()


    def action(self,action:str,value:str|list[str]) -> bool|None:
        """
        Метод для управления действиями для того или иного пункта меню
        :param action: Действие необходимое для этого пункта меню
        :param value: Параметры необходимые для совершения того или иного действия
        :return:
        """
        if action == "copy_files" :
            # print("action == copy_files")
            self.files.create_file_copy_project()
            return None
        elif action == "replace_files" :
            self.files.replacing_files(value)
            return None
        elif action == "rebuild_copies" :
            self.files.file_collector()
            return True
        elif action == "delete_copies" :
            # print('value delete = ',value)
            self.files.delete_copies(value)
            return True
        elif action == "save_file_ignor" :
            # Создадим файл если его нет
            self.files.create_file(self.files.path_folder_copies(),self.files.NAME_FILE_IGNOR)
            if value  is not None :
                self.data_cls.sorted_data_ignor(self.files.add_ignore(value))
                return True
            return None
        elif action == "open_file_help" :
            pass
        elif action == "save_file_config" :
            select,field,requirement = value
            if select is not None :
                save_data = field + select
                if requirement is not None :
                    self.files.action_file(self.files.pwd(), self.files.NAME_FILE_CONFIG,field,save_data)
                else:
                    if self.files.path_absolut_check(select):
                        self.files.action_file(self.files.pwd(), self.files.NAME_FILE_CONFIG, field, save_data)
                    else:
                        self.files.create_dir(select)
                        save_data = field + self.files.create_absolut_path(select)
                        self.files.action_file(self.files.pwd(), self.files.NAME_FILE_CONFIG, field, save_data)
            return True
        elif action == "create_file_config" :
            # Если файл не найден, то создадим
            if not self.files.search_file(self.files.pwd(),Files.NAME_FILE_CONFIG) :
                self.files.create_file(self.files.pwd(),Files.NAME_FILE_CONFIG)
            return True
        elif action == "web_settings" :
            pass
        else:
            raise UnknownException (f"unknown type action : {action.__name__}")