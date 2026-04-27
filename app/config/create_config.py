from app.rest_client.ollama import get_client
from app.utils.path_util import get_full_path, check_if_exist
import os
import sys

def create_config_file():
    print("""
    
░▒▓███████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░▒▓███████▓▒░░▒▓█▓▒░▒▓████████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░     
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░     
░▒▓███████▓▒░░▒▓███████▓▒░░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░     
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░     
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░     
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     

    """)
    # Define the target directory: ~/.config/predit
    config_dir = os.path.expanduser("~/.config/predit")
    # Ensure the directory exists
    os.makedirs(config_dir, exist_ok=True)

    # Define the full path for the config file
    config_file_path = os.path.join(config_dir, "config.yml")

    # --- Configuration Logic ---
        # 1. Directories
    # We will write the content directly to the file, as per the request.
    # The original interactive setup is modified to ensure the output is in the target location.
    config_data = {}

    # --- Step 1: Configure Directories Interactively (Modified) ---
    print("--- Configuring directories ---")
    config_data['directories'] = {}

    # Interactive setup to get directory names
    config_data['directories']['mascot'] = get_full_path(str(input("Enter the name of the 'mascot' directory (Default is None): ").strip()))
    config_data['directories']['memes'] = get_full_path(str(input("Enter the name of the 'memes' directory (Default is None): ").strip()))

    # Init None if default
    if config_data['directories']['mascot'] == "":
        config_data['directories']['mascot'] = None

    if config_data['directories']['memes'] == "":
        config_data['directories']['memes'] = None   

    # --- Step 2: Configure Ollama Model Interactively (Modified) ---
    print("\n--- Configuring the Ollama model ---")

    ollamaurl = str(input("Enter the URL used by Ollama (leave blank for default - http://127.0.0.1:11434): ").strip())
    token = str(input("Enter the Ollama token (leave blank for default - None): ").strip())
    
    if ollamaurl == "":
        ollamaurl = "http://127.0.0.1:11434"

    headers = {}
    if token != "":
        headers["Authorization"] = f"Bearer {token}"

    config_data['ollama'] = {
        'url': ollamaurl,
        'model': None,
        'headers': headers
    }

    available_models = []
    # This part relies on the 'ollama' library being accessible.
    try:
    # Attempt to list Ollama models
        ollama = get_client(ollamaurl, headers)

        response = ollama.list()

        if 'models' in response:
            available_models = [model.model for model in response['models']]
    except Exception as e:
        print(f"Could not access Ollama list. Ollama must be installed and running.\nError: {e}")
        if not str(input("\nContinue without Ollama ? (Ollama is not required for the derush part): (Y/n)")).lower() in ["", "y", "o", "yes", "oui"]:
            sys.exit(0)

    if len(available_models) > 0 :
        # Interactive model selection
        selected_model = ""
        if available_models:
            print("\nAvailable Ollama models:")
            for i, model in enumerate(available_models):
                print(f"{i+1}. {model}")

            while True:
                try:
                    choice = input("Please choose a model (enter the number): ").strip()
                    if choice.isdigit() and 1 <= int(choice) <= len(available_models):
                        selected_model = available_models[int(choice) - 1]
                        break
                    else:
                        print("Invalid choice. Please enter a number corresponding to the list of models.")
                except ValueError:
                    print("Invalid input. Please enter a number.")


        config_data['ollama']['model'] = selected_model

    # --- Step 3: Write the YAML file to the specified location ---
    print(f"\n--- Writing configuration to {config_file_path} ---")

    try:
        # Write the content to the file in the target directory
        with open(config_file_path, 'w') as f:
            # Ensure the file has the required structure
                f.write("directories:\n")
                f.write(f"  mascot: \"{config_data['directories']['mascot']}\"\n")
                f.write(f"  memes: \"{config_data['directories']['memes']}\"\n")
                f.write("ollama:\n")
                f.write(f"  url: \"{config_data['ollama']['url']}\"\n")
                f.write(f"  model: \"{config_data['ollama']['model']}\"\n")
                f.write(f"  headers:\n")
                if headers.get("Authorization") :
                    f.write(f"    Authorization: \"{config_data['ollama']['headers']["Authorization"]}\"\n")
                f.write(f"project:\n")
                f.write(f"  fps: 60\n")
                f.write(f"  format: otio # the project file format, check which one is compatible with your editor.\n # All the preinstalled formats adapters are ['maya_sequencer', 'burnins', 'cmx_3600', 'svg', 'AAF', 'ale', 'xges', 'fcp_xml', 'otio_json', 'otioz', 'otiod'].\n # You can install new adapters with pip (you don't need to edit the code of predit)")
            
        print(f"\nConfiguration created successfully in {config_file_path}!")
        print("Content of the created file:")
            
            # Display the content of the file for confirmation
        with open(config_file_path, 'r') as f:
                print(f.read())

    except IOError as e:
        print(f"\nError writing the file {config_file_path}: {e}")
        print("Ensure the script has the necessary permissions to write to ~/.config/predit.")