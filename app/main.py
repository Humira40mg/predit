from os import path, listdir, remove
from pathlib import Path

from .config.config_reader import TMP, OLLAMA_URL, OLLAMA_HEADERS, ID

from .utils.verificationUtil import check_application_dependencies_and_folders, check_if_no_medias, check_if_user_accept, check_if_output_folder_exist, check_compatible_files_and_sort
from .utils.argumentUtil import parse_arguments

from .core.project_writter import write_file
from .core.speechToText import transcribe_audio
from .core.editor import Editor

from .rest_client.ollama import get_client

import app.core.sequences as sequences


ollama_cli = get_client(OLLAMA_URL, OLLAMA_HEADERS)

def main():
    check_application_dependencies_and_folders()

    media_list = []
    base_media_path, output_directory = parse_arguments()

    output_directory = check_if_output_folder_exist(output_directory)
    parent_directory = path.abspath(base_media_path)

    if path.isdir(base_media_path):
        # get all files from this directory
        media_list.extend([f"{base_media_path}/{f}" for f in listdir(base_media_path)]) # Add files from this directory to the file list (with the full path)

    else: 
        # get the single file from this path
        media_list.append(base_media_path)
        parent_directory = path.abspath(Path(base_media_path).parent)

    check_if_no_medias(media_list)
    media_list = check_compatible_files_and_sort(media_list)
    
    check_if_user_accept(media_list=media_list, output_directory=output_directory)

    # Make an editor object with the path to the project folder
    editor = Editor("{}/Predit_Enhanced_({})".format(parent_directory, ID))

    editor.convert_videos_to_mp4_and_normalize_the_sound(media_list)

    check_if_no_medias(editor.list_path, "No files to derush.\nAborted.")

    editor.path_to_clip()

    editor.derush()
    success = editor.merge_clips_for_stt_model()
    
    if success :
        speech = transcribe_audio(f"{TMP}/merged.wav")
        
        for object_name in sequences.__all__ :
            worker = getattr(sequences, object_name)(speech) # create object
            worker.do_sequence()

    write_file(output_directory)

    print("All Done !")

    # Clean up temporary files in the tmp directory
    [remove(f"{TMP}/{item_path}") for item_path in listdir(TMP)]
        

if __name__ == '__main__':
    main()