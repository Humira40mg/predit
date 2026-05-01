import argparse
from os import path, listdir, remove, getcwd, mkdir
import sys
from shutil import which

from app.config.config_reader import TMP, OLLAMA_URL, OLLAMA_HEADERS, FORMAT, ID

from app.rest_client.ollama import get_client
from app.utils.path_util import check_if_exist

from app.core.derush import DeRusher
from app.core.merger import Merger, Path, VideoFileClip
from app.core.project_writter import write_file
from app.core.ffmpeg import normalize_video_s_audio
from app.core.speechToText import transcribe_audio

from app.gateway.llm_gateway import mascot_sequence


TEMP_AUDIO_PATH = f"{TMP}/audio.wav"
ACCEPT_LIST = ['', 'y', 'yes', 'o', 'oui']
COMPATIBLE = ['mp4', 'mkv', 'mp3', 'wav']
ollama_cli = get_client(OLLAMA_URL, OLLAMA_HEADERS)

def main():
    # Verify existence of ffmpeg
    if which("ffmpeg") is None:
        print("Error : ffmpeg is not installed. Please install it before using this tool.")
        sys.exit(1)
    
    try:
        ollama_cli.list()
    except Exception as e:
        print(f"Ollama must be installed and running.\nError: {e}")
        sys.exit(1)
    
    # Verify existence of tmp folder
    if not Path(TMP).exists():
        mkdir(TMP)

    media_list = []
    context_directory = "./"

    # define argument parser
    parser = argparse.ArgumentParser(
        description='Get video and audio files with the path given to a directory or file. It will create a new folder in the current directory or indicated directory with all the subclips of the video and audio files.'
    )
    parser.add_argument('file_path',
                        default= getcwd(),
                        type=str,
                        help='Path to the video or audio file (or directory)')

    parser.add_argument('-o', '--output-directory',
                        default= getcwd(),
                        type=str,
                        help='Path to the output directory (or directory)')
    
    args = parser.parse_args()
    
    # Define complete paths
    base_path = path.abspath(args.file_path)
    output_directory = path.abspath(args.output_directory)

    # Verify path of the output folder
    if not path.isdir(output_directory) :
        print(f"Output directory '{output_directory}'does not exist.\n")
        if str(input("Use the current directory instead ? (Y/n): ")).lower() in ACCEPT_LIST: 
            output_directory = getcwd()
        else:
            print("Aborted.")
            sys.exit(1)

    parent_directory = path.abspath(base_path)
    # If the path is a directory, get all files from this directory
    if path.isdir(base_path):
        media_list.extend([f"{base_path}/{f}" for f in listdir(base_path)]) # Add files from this directory to the file list (with the full path)

    else: # Otherwise, get the single file from this path
        media_list.append(base_path)
        parent_directory = path.abspath(Path(base_path).parent)

    # Cancel if there are no files
    if len(media_list) == 0:
        print("No files found.")
        sys.exit(1)
    
    media_list = [media for media in media_list if media.split(".")[-1] in COMPATIBLE] # Filter files where the extension is in COMPATIBLE
    media_list.sort() # Sort files alphabetically

    print("The files will be derushed in order:\n  {}".format(',\n  '.join(media_list)))
    print('A project file "Project-{}.{}" will be created in:\n  {}\n'.format(ID, FORMAT, output_directory))
    if str(input('Proceed to pre-edit? (Y/n)')).lower() in ACCEPT_LIST:
        
        mkdir("{}/Predit_Enhanced_({})".format(parent_directory, ID))

        # Convert videos to mp4 and normalize the sound
        list_path = [
            path.abspath(
                normalize_video_s_audio(media)
            ) for media in media_list
        ]
        list_path = [x for x in list_path if path.isfile(x)]
        list_path.sort()

        print(list_path)

        if len(list_path) == 0:
            print("No files to derush.\nAborted.")
            sys.exit(1)

        all_clips = [VideoFileClip(path_to_file) for path_to_file in list_path]

        #Derush
        derusher: DeRusher = DeRusher(TEMP_AUDIO_PATH)
        for clip, path_to_file in zip(all_clips, list_path):
            derusher.extract_audio(clip) # save temp audio to find timestamps of speechs
            derusher.make(clip, path_to_file) # official derush in the project file
        
        derusher.end_of_derush()
        
        # Used to make an edited version of the audio to use it in the Speech to text model.
        merger: Merger = Merger(all_clips)
        derusher.extract_audio(merger.full_clip)
        merger.makeSubClips(derusher.getTimeStamps())
        success = merger.write_concatenated_audio_clips()
        
        if success :
            speech = transcribe_audio(f"{TMP}/merged.wav")
            mascot_sequence(speech=speech)

        write_file(output_directory)

        print("All Done !")

        # Clean up temporary files in the tmp directory
        [remove(f"{TMP}/{item_path}") for item_path in listdir(TMP)]
        

if __name__ == '__main__':
    main()