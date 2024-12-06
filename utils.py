import os

def create_folder_if_not_exists(folder:str)->str:


    if not os.path.exists(folder):
        os.mkdir(folder)

    return os.path.abspath(folder)