from mygit.files_class import Files


files = Files()


frequently_question = files.show_translation("frequently_question","enter_exit")
menu_structure = {
               "main_menu": [
            {
                "title": "copy",
                "description": f"{files.show_translation("copy_description")}",
                "sub_menu": [
                    {

                "action": "copy_files",
                "data_type":"all",
                "input_method":"one"
                    }
                        ]
            },
            {
                "title": "replace",
                "description": f"{files.show_translation("replace_description")}",
                "sub_menu": [
                    {

                     "choice": "choice_list_copies",
                     "action": "replace_files",
                     "data_type":"all",
                     "input_method": "two",
                     "question": f"{files.show_translation("replace_question","enter_exit")}"
                    }

                ]
            },
            {
                "title": "rebuild copies",
                "description": f"{files.show_translation("rebuild_copies_description")}",

            "sub_menu": [
                    {

                "action": "rebuild_copies"
                    }
                ]
            },
            {
                "title": "delete",
                "description": f"{files.show_translation("delete_description")}",
                "sub_menu": [
                   {

                    "choice": "choice_list_copies",
                    "action": "delete_copies",
                    "data_type": "all",
                    "input_method": "two",
                    "question": f"{files.show_translation("delete question","enter_exit")}"
                    }
               ]
            },
            {
                "title": "ignor",
                "description": f"{files.show_translation("ignor_description")}",
                "sub_menu": [
                   {

                    "action": "save_file_ignor",
                    "choice": "choice_list_copies",
                    "data_type": "all",
                    "input_method": "two",
                    "question": f"{files.show_translation("ignor_question","enter_exit")}"
                }

               ]
            },

            {
                "title": "help",
                "description": f"{files.show_translation("help_description")}",
                "sub_menu": [
                   {

                "action": "open_file_help",
                "data_type":"string",
                "input_method": "two"
                   }
                ]
            },
            {
                "title": "Setting",
                "description": f"{files.show_translation("help_description")}",
                "sub_menu": [
                   {
                    "title": "change language",
                    "description": f"{files.show_translation("language_description")}",
                "sub_menu": [
                    {"title": "English"},
                    {"title": "Russian"},
                    {
                    "action": "modify_file_config",
                    "choice": "choice_list_language",
                    "requirement" : "change_language",
                    "create_field": "language :",
                    "data_type": "all",
                    "input_method": "one",
                    "question": f"{files.show_translation("language_question","enter_exit")}"
                            }
                       ]
                },
                    {
                        "title": "change project",
                        "description": f"{files.show_translation("change_project_description")}",
                        "sub_menu": [
                            {
                        "action": "modify_file_config",
                        "choice": "choice_list_project",
                        "data_type": "all",
                        "input_method": "one",
                        "question": f"{files.show_translation("change_project_question","enter_exit")}"
                            }
                        ]

                    },
                    {
                        "title": "added project",
                        "description": f"{files.show_translation("added_project_description")}",
                        "sub_menu": [
                        {
                        "action": "add_file_config",
                        "data_type": "string",
                        "input_method": "one",
                        "requirement" : "path_absolut",
                        "create_field": "list_projects :",
                        "question": f"{files.show_translation("added_absolute_path_question","enter_exit")}"
                        # "question": "Добавить проект Enter выход : "
                    },
                    {
                        "action": "add_file_config",
                        "data_type": "string",
                        "input_method": "one",
                        "requirement" : "path_absolut",
                        "create_field": "list_projects :",
                        "question": f"{files.show_translation("added_path_question","enter_exit")}"
                    },
                    {"select" : '1'}

                ]

                    },

                    {
                    "title": "web",
                    "description": f"{files.show_translation("web_description")}",
                    "sub_menu": [
                       {
                        # "title": "",
                        "action": "web_settings",
                        # "choice": "choice_list_copies",
                        "data_type": "all",
                        "input_method": "string",
                        "question": f"{files.show_translation("web_question","enter_exit")}"
                    }
                   ]
                   },
                    {
                        "title": "llm",
                        "description": f"{files.show_translation("llm_description")}",
                        "sub_menu": [
                            {
                                "action": "env_modify",
                                "choice": "choice_list_llm",
                                "data_type": "all",
                                "input_method": "one",
                                "question": f"{files.show_translation("llm_question","enter_exit")}"
                            }

                        ]
                    },

                    {"question": f"{frequently_question }" ,"data_type":"all","input_method": "one" }
               ]
            },
            {"question": f"{frequently_question }" ,"data_type":"all","input_method": "one"  }
        ]
    }


menu_default = { "main_menu": [
    {

        "title": f"{files.show_translation("setting_environment")}",
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
            "question": f"{files.show_translation("added_absolute_path_question","enter_exit")}"

        },
        {

            "action": "save_file_config",
            "field": "path_to_project_copies_folder_default :",
            "data_type": "string",
            "input_method": "one",
            "create_field" : "path_to_project_copies_folder_default :",
            "question": f"{files.show_translation("added_path_question","enter_exit")}"

        },
        {
            "action": "save_file_ignor",
            "data_type": "string" ,
            "input_method": "two",
            "question": f"{files.show_translation("file_ignor_question","enter_exit")}"
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
                "create_field": "language :",
                "data_type": "string",
                "input_method": "one"

            },
            {
                "title": "Russian",
                "action": "save_file_config",
                "create_field": "language :",
                "data_type": "string",
                "input_method": "one"

            },
            {"question": f"{files.show_translation("language_question","enter_exit")}" ,"data_type":"all","input_method": "one" }
    ]
}







