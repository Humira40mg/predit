from os import mkdir, getcwd, path
from sys import exit
from pathlib import Path
from shutil import which

from app.rest_client.ollama import get_client
from app.config.config_reader import TMP, ACCEPT_LIST, COMPATIBLE, ID, FORMAT
from app.utils.list_util import is_empty

def check_ffmpeg_insalled():
    if which("ffmpeg") is None:
        print("Error : ffmpeg is not installed. Please install it before using this tool.")
        exit(1)

def check_ollama_installed():
    try:
        get_client().list()
    except Exception as e:
        print(f"Ollama must be installed and running.\nError: {e}")
        exit(1)
    
def create_tmp_folder_if_not_existing():
    if not Path(TMP).exists():
        mkdir(TMP)

def check_application_dependencies_and_folders():
    check_ffmpeg_insalled()
    check_ollama_installed()
    create_tmp_folder_if_not_existing()

def check_if_output_folder_exist(output_directory):
    if path.isdir(output_directory) :
        return output_directory
        
    print(f"Output directory '{output_directory}'does not exist.\n")
    if str(input("Use the current directory instead ? (Y/n): ")).lower() in ACCEPT_LIST: 
        return getcwd()
    else:
        print("Aborted.")
        exit(1)
    
    
def check_if_no_medias(media_list, message = "No files found."):
    if is_empty(media_list):
        print(message)
        exit(1)

def check_compatible_files_and_sort(files_list):
    liste = [media for media in files_list if media.split(".")[-1] in COMPATIBLE]
    liste.sort()
    return liste

def check_if_user_accept(media_list, output_directory):
    print("The files will be derushed in order:\n  {}".format(',\n  '.join(media_list)))
    print('A project file "Project-{}.{}" will be created in:\n  {}\n'.format(ID, FORMAT, output_directory))
    if str(input('Proceed to pre-edit? (Y/n)')).lower() not in ACCEPT_LIST:
        print('\nAborted.')
        exit(1)