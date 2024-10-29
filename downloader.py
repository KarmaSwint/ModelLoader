import os
import requests
import zipfile
import time
import hashlib
import zlib
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn, DownloadColumn
from typing import Dict, List, Optional, Tuple

console = Console()

def calculate_file_hash(file_path: str, hash_algorithm: str) -> str:
    """
    Calculate the hash of the file like you're solving a puzzle.

    Args:
        file_path (str): Path to the file you want to hash.
        hash_algorithm (str): The hash algorithm to use.

    Returns:
        str: The calculated hash, you crypto wizard.
    """
    if hash_algorithm == "SHA256":
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    elif hash_algorithm == "CRC32":
        with open(file_path, "rb") as f:
            file_data = f.read()
            return format(zlib.crc32(file_data) & 0xFFFFFFFF, '08x')  # Return as hex
    else:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

def download_version(version: Dict, comfyui_dir: str, api_key: str) -> None:
    """
    Download a version like you're acquiring a rare collectible. But legally.
    Now with more stats than a baseball game!

    Args:
        version (Dict): The version info. Try not to lose it.
        comfyui_dir (str): Where to store this digital gold.
        api_key (str): Your super secret API key. Keep it safe!
    """
    if 'files' not in version or not version['files']:
        console.print("[bold red]No files found in the version. What kind of trickery is this?[/bold red]")
        return
    
    file_info = version['files'][0]
    download_url = file_info['downloadUrl']
    file_name = file_info['name']
    
    model_type = version.get('type', 'Unknown')

    # Adjusted: If the model type is 'Checkpoint', save it to 'checkpoints2' instead of 'checkpoints'
    subdirectory = {
        "Checkpoint": "models/checkpoints2",  # Changed to checkpoints2
        "LORA": "models/loras",
        "Upscaler": "models/upscale_models",
        "TextualInversion": "models/embeddings",
        "AestheticGradient": "models/embeddings",
        "Hypernetwork": "models/hypernetworks",
        "Unet": "models/unet",
        "VAE": "models/vae",
        "Workflows": "user/default/workflows",
        "Controlnet": "models/controlnet",
        "Poses": "models/poses"
    }.get(model_type, "unknown")

    full_file_path = os.path.join(comfyui_dir, subdirectory, file_name)
    os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
    
    console.print(f"[bold green]Downloading to: {full_file_path}[/bold green]")
    
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        with requests.get(download_url, headers=headers, stream=True) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            
            with open(full_file_path, 'wb') as f, Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                DownloadColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeRemainingColumn(),
                TextColumn("[bold blue]{task.fields[speed]}"),
                console=console
            ) as progress:
                download_task = progress.add_task("[cyan]Downloading...", total=total_size, speed="-")
                start_time = time.time()
                downloaded = 0
                
                for chunk in response.iter_content(chunk_size=8192):
                    size = f.write(chunk)
                    downloaded += size
                    elapsed = time.time() - start_time
                    if elapsed > 0:
                        speed = downloaded / elapsed
                        speed_str = f"{speed/1024/1024:.2f} MB/s"
                        progress.update(download_task, advance=size, speed=speed_str)
        
        console.print("[bold green]Download complete, you magnificent genius![/bold green]")
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            console.print("[bold red]Error 403: Forbidden. Can't download this version. It might require credits or special permissions.[/bold red]")
        else:
            console.print(f"[bold red]HTTP Error occurred: {e}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
    
    unzip_model(full_file_path)

def unzip_model(file_path: str) -> None:
    """
    Unzip the version file like you're unwrapping a digital present.

    Args:
        file_path (str): Path to the zip file. Don't get lost.
    """
    if not file_path.lower().endswith('.zip'):
        console.print(f"[yellow]{file_path} is not a zip file. No unzipping needed.[/yellow]")
        return

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(file_path))
    console.print(f"[green]Successfully unzipped {file_path}[/green]")
    os.remove(file_path)
