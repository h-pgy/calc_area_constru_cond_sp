from dotenv import load_dotenv
import os

from utils import create_folder_if_not_exists

def get_env_var(varname:str)->str:
    
    load_dotenv()

    try:
        return os.environ[varname]
    except KeyError:
        raise RuntimeError(f'Variavel de ambiente {varname} não definida.')


ORIGINAL_DATA_FOLDER=create_folder_if_not_exists(get_env_var('ORIGINAL_DATA_FOLDER'))
GENERATED_DATA_FOLDER=create_folder_if_not_exists(get_env_var('GENERATED_DATA_FOLDER'))

ID_SESSAO=get_env_var('ID_SESSAO')