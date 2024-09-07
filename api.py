import requests
import os
import json
from typing import Dict, List, Tuple, Optional
from rich.console import Console

console = Console()

API_BASE_URL = "https://civitai.com/api/v1"
CONFIG_FILE = "config.json"

def api_request(endpoint: str, params: Dict = None, headers: Dict = None) -> Dict:
    """
    Make an API request like a pro. Don't break the internet.

    Args:
        endpoint (str): The API endpoint. Try not to misspell it.
        params (Dict, optional): Query parameters. Default is None.
        headers (Dict, optional): Request headers. Default is None, but you should probably use some.

    Returns:
        Dict: The API response, or None if something goes wrong.
    """
    try:
        response = requests.get(endpoint, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[bold red]Error: {e}[/bold red]")
        return None

def load_config() -> Dict[str, str]:
    """
    Load the config file. It's like reading your diary, but less embarrassing.

    Returns:
        Dict[str, str]: The config, or an empty dict if something went wrong.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config: Dict[str, str]) -> None:
    """
    Save the config. Try not to lose it this time.

    Args:
        config (Dict[str, str]): The precious config. Handle with care.
    """
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def get_api_key() -> str:
    """
    Get the API key. It's like finding the Holy Grail, but for nerds.

    Returns:
        str: The API key. Guard it with your life.
    """
    config = load_config()
    if "api_key" not in config:
        api_key = input("Enter your CivitAI API key: ")
        config["api_key"] = api_key
        save_config(config)
    return config["api_key"]

def get_comfyui_dir() -> str:
    """
    Get the ComfyUI directory. Try not to get lost in your own filesystem.

    Returns:
        str: The path to ComfyUI. Remember it this time.
    """
    config = load_config()
    if "comfyui_dir" not in config:
        comfyui_dir = input("Enter your ComfyUI installation directory: ")
        config["comfyui_dir"] = os.path.expanduser(comfyui_dir)
        save_config(config)
    return config["comfyui_dir"]

def search_models(api_key: str, model_type: str, base_model: str, sort_by: str, query: str, cursor: Optional[str] = None) -> Tuple[List[Dict], Dict]:
    """
    Search for models like you're hunting for digital unicorns. Now with 100% more working code!

    Args:
        api_key (str): Your API key. Keep it safe.
        model_type (str): The type of model you're after. Choose wisely.
        base_model (str): The base model. Don't mix them up.
        sort_by (str): How to sort the results. Because order is important.
        query (str): Your search query. Try to be specific.
        cursor (Optional[str], optional): For pagination. Default is None.

    Returns:
        Tuple[List[Dict], Dict]: A list of models and metadata, or an empty list if you're out of luck.
    """
    params = {
        "limit": 10,
        "query": query,
    }
    if cursor is not None:
        params["cursor"] = cursor
    if model_type != "ALL":
        params["types"] = model_type
    if base_model != "ALL":
        params["baseModels"] = base_model
    if sort_by:
        params["sort"] = sort_by

    headers = {"Authorization": f"Bearer {api_key}"}
    url = f"{API_BASE_URL}/models"
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('items', []), data.get('metadata', {})
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error fetching models: {e}[/bold red]")
        return [], {}