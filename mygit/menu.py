frequently_question = "Выберите интересующий пункт меню (Enter - выход): "
menu_structure = {
               "main_menu": [
            {
                "title": "copy",
                "description": " - создать копию файлов",
                "sub_menu": [
                    {

                "action": "copy_files",
                "data_type":"all",
                "input_method":"two"
                    }
                        ]
            },
            {
                "title": "replace",
                "description": " - перезаписать файлы в папке проекта",
                "sub_menu": [
                    {

                     "choice": "choice_list_copies",
                     "action": "replace_files",
                     "data_type":"all",
                     "input_method": "two",
                     "question": f"Выберите копию для замены (название/номер) Enter выход : "
                    }

                ]
            },
            {
                "title": "rebuild copies",
                "description": " - пересобрать все копии",

            "sub_menu": [
                    {

                "action": "rebuild_copies"
                    }
                ]
            },
            {
                "title": "delete",
                "description": " - удалить",

                "sub_menu": [
                   {

                    "choice": "choice_list_copies",
                    "action": "delete_copies",
                    "data_type": "all",
                    "input_method": "two",
                    "question": "Выберите копию(и) для удаления (название/номер) (All - все) Enter выход : "
                    }
               ]
            },
            {
                "title": "ignor",
                "description": " - добавить в игнор",
                "sub_menu": [
                   {

                    "action": "save_file_ignor",
                    "choice": "choice_list_copies",
                    "data_type": "all",
                    "input_method": "two",
                    "question": "Выберите копию(и) для добавления в ignor ('*' - файл, '/' - папка ) Enter выход : "
                }

               ]
            },
            #     {
            #     "title": "web",
            #     "description": " - настройка web хранилища",
            #     "sub_menu": [
            #        {
            #         # "title": "",
            #         "action": "web_settings",
            #         # "choice": "choice_list_copies",
            #         "data_type": "all",
            #         "input_method": "string",
            #         "question": "Выберите копию(и) для добавления в ignor ('*' - файл, '/' - папка ) Enter выход : "
            #     }
            #
            #    ]
            # },
            {
                "title": "help",
                "description": " - помощь",
                "sub_menu": [
                   {

                "action": "open_file_help",
                "data_type":"string",
                "input_method": "two"
                   }
                ]
            },
            {"question": f"{frequently_question }" ,"data_type":"all","input_method": "two" }
        ]
    }


menu_default = { "main_menu": [
    {

        "title": "Настройка окружения : ",
        "sub_menu": [
        {

            "action": "create_file_config"
        },
        {

            "action": "save_file_config",
            "data_type": "string",
            "input_method": "one",
            "create_field" : "path_to_project_folder_default :",
            "requirement" : "path_absolut",
            "question": "Введите абсолютный путь к отслеживаемой директории, где хранятся файлы проекта : "

        },
        {

            "action": "save_file_config",
            "field": "path_to_project_copies_folder_default :",
            "data_type": "string",
            "input_method": "one",
            "create_field" : "path_to_project_copies_folder_default :",
            "question": "Введите путь абсолютный к директории где будут храниться копии проекта : "

        },
        {
            "action": "save_file_ignor",
            "data_type": "string" ,
            "input_method": "one",
            "question": "Укажите игнорируемые файлы/папки для добавления в my_git_ignor ('*' - файл, '/' - папка ) Enter выход : "
        }
            ]
        },
        {"select" : '1'}
                    ]

        }


menu_language = {
               "main_menu": [
            {
                "title": "English",
                "action": "save_file_config",
                "create_field": "language :"

            },
            {
                "title": "Russian",
                "action": "save_file_config",
                "create_field": "language :"

            },
            {"question": f"Select language" ,"data_type":"all","input_method": "one" }
    ]
}







