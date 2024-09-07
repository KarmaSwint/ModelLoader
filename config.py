import os
import json
from typing import Dict

CONFIG_FILE = "config.json"

def load_config() -> Dict[str, str]:
    """
    Load the config file with all our important settings.
    
    Returns:
        Dict[str, str]: A dictionary of settings, or an empty dict if the file's missing.
    """
    try:
        with open(CONFIG_FILE, "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print("Oops! Looks like our config file took a vacation. Time to file a missing persons report!")
        return {}
    except json.JSONDecodeError:
        print("Our config file seems to be speaking in tongues. Maybe it needs a translator?")
        return {}

def save_config(config: Dict[str, str]) -> None:
    """
    Save the config to a file. Handle with care!

    Args:
        config (Dict[str, str]): The configuration to be saved in JSON format.
    """
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def get_api_key() -> str:
    """
    Fetch the API key or prompt the user for a new one.
    
    Returns:
        str: The API key.
    """
    config = load_config()
    if "api_key" not in config:
        api_key = input("Enter your CivitAI API key (pretty please): ")
        config["api_key"] = api_key
        save_config(config)
    return config["api_key"]

def get_comfyui_dir() -> str:
    """
    Get the ComfyUI directory or ask for it if not set.
    
    Returns:
        str: The path to ComfyUI.
    """
    config = load_config()
    if "comfyui_dir" not in config:
        comfyui_dir = input("Where did you put ComfyUI? Enter the directory: ")
        config["comfyui_dir"] = os.path.expanduser(comfyui_dir)
        save_config(config)
    return config["comfyui_dir"]

def change_api_key():
    """
    Change the API key. Out with the old, in with the new!
    """
    config = load_config()
    current_api_key = config.get("api_key", "Not set")
    print(f"Current API key: {current_api_key}")
    
    new_api_key = input("Enter new API key (leave blank to keep the current one): ").strip()
    if new_api_key:
        config["api_key"] = new_api_key
        save_config(config)
        print("API key updated successfully! You're on a roll!")
    else:
        print("API key remains unchanged. If it ain't broke, don't fix it, right?")
    
    input("Press Enter to return to the main menu...")

def change_comfyui_dir():
    """
    Change the ComfyUI directory. Let's make sure we know where everything is!
    """
    config = load_config()
    current_comfyui_dir = config.get("comfyui_dir", "Not set")
    print(f"Current ComfyUI directory: {current_comfyui_dir}")
    
    new_comfyui_dir = input("Enter new ComfyUI installation directory (leave blank to keep the current one): ").strip()
    if new_comfyui_dir:
        config["comfyui_dir"] = os.path.expanduser(new_comfyui_dir)
        save_config(config)
        print("ComfyUI directory updated successfully! You're a navigation wizard!")
    else:
        print("ComfyUI directory remains unchanged. Consistency is key!")
    
    input("Press Enter to return to the main menu...")