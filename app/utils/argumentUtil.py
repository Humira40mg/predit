import argparse
from os import path, getcwd

def parse_arguments():
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
    
    return path.abspath(args.file_path), path.abspath(args.output_directory)