import signal
from api import load_config, get_api_key, get_comfyui_dir
from menu import display_main_menu, download_model_menu
from config import change_api_key, change_comfyui_dir

def signal_handler(sig, frame):
    """
    Handle interrupts gracefully. CTRL+C can't escape us!
    """
    print("\n[bold red]Download cancelled. Cleaning up...[/bold red]")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():
    """
    The main function. This is where the magic happens!
    """
    config = load_config()
    api_key = get_api_key()
    comfyui_dir = get_comfyui_dir()

    while True:
        action = display_main_menu()
        
        if action == "download":
            download_model_menu()
        elif action == "api_key":
            change_api_key()
        elif action == "comfyui_dir":
            change_comfyui_dir()
        elif action == "exit":
            print("[bold green]Thanks for using this awesome CLI. Now go make some amazing art![/bold green]")
            break

if __name__ == "__main__":
    main()
