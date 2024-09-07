from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.console import Console
from rich.table import Table
from api import search_models, get_api_key, get_comfyui_dir
from downloader import download_version
from collections import deque
import requests
import json
import random
from typing import Dict, List, Optional, Tuple
from ascii_art import ASCII_HEADERS
import os
import signal

console = Console()

WITTY_SUBTITLES = [
    "Downloading models faster than you can say 'Wow!'",
    "Making AI art like a pro, one download at a time",
    "Because manually downloading models is so last year",
    "Turning your PC into an AI powerhouse, or a fancy paperweight",
    "Downloading pixels and dreams with style",
    "Making your GPU work overtime since 2024",
    "Fetching models faster than a caffeinated cheetah",
    "Because who needs free time when you have infinite AI models?",
    "Turning electricity into art, one model at a time",
    "Downloading dreams and inspiration in equal measure"
]

MENU_FLAVORS = {
    "model_type": [
        "Choose a model type, you indecisive genius:",
        "What flavor of AI magic do you want today?",
        "Pick your poison, digital alchemist:",
        "Select a model type or I'll choose for you:",
        "What kind of pixel-pushing wizardry are we doing?",
        "Choose your weapon, art warrior:",
        "What's your AI specialty? Pick one:",
        "Select a model type, or just mash the keyboard like a pro:",
        "What kind of digital sorcery are we conjuring today?",
        "Pick a model type, or I'll assume you want 'Poorly Drawn Stick Figures':",
        "Choose your flavor of AI madness:",
        "What's your digital treat of choice?",
        "Select a model type, or I'll let my cat choose for you:",
        "Pick your AI playground, you magnificent creator:",
        "What kind of computational magic are we getting into?",
        "Choose a model type, or I'll assume you're here by accident:",
        "Select your flavor of digital creativity:",
        "What's your AI specialty? Don't be shy:",
        "Pick a model type, or I'll choose the most interesting one:",
        "What kind of binary brilliance are we dealing with today?"
    ],
    "base_model": [
        "Choose a base model, you picky genius:",
        "What's the foundation of your AI dreamscape?",
        "Select the base model, or I'll pick the most popular one:",
        "What's your AI starting point, genius?",
        "Choose your base model, or admit you have no clue:",
        "Pick the backbone of your digital Frankenstein:",
        "What's the base model? Don't mess this up:",
        "Select your AI launch pad, rocket scientist:",
        "Choose a base model, or just close your eyes and point:",
        "What's the starting point for your pixel-perfect masterpiece?",
        "Pick your base model, or I'll assume you want 'Crayon Drawings':",
        "Choose the foundation of your AI house of cards:",
        "What's the base for your digital soup?",
        "Select a base model, or I'll let my goldfish decide:",
        "Pick your AI primordial soup:",
        "What's the base model for your digital dumpster fire?",
        "Choose your AI ancestor, you evolutionary mistake:",
        "Select the base model, or admit you're just here for the fun:",
        "What's the starting point for your AI fever dream?",
        "Pick a base model, or I'll assume you're a time-traveler from 1995:"
    ],
    "sort_by": [
        "How do you want to sort this?",
        "Choose your sorting method, you OCD genius:",
        "How should I arrange this digital collection?",
        "Pick a sorting method, or I'll just throw darts at the screen:",
        "How do you want this AI smorgasbord served?",
        "Choose your sorting preference, you picky genius:",
        "How should I line up these digital ducks?",
        "Select a sorting method, or I'll use my patented chaos theory:",
        "How do you want this AI buffet organized?",
        "Pick your sorting poison:",
        "How should I arrange this pixel parade?",
        "Choose a sorting method, or I'll just use a random number generator:",
        "How do you want this binary banquet sorted?",
        "Select your preferred order of creativity:",
        "How should I arrange this digital dogpile?",
        "Choose a sorting method, or I'll ask my magic 8-ball:",
        "How do you want this AI assortment arranged?",
        "Pick a sorting style, you detail-oriented deviant:",
        "How should I organize this computational chaos?",
        "Choose your sorting adventure, or I'll just shake the digital Etch A Sketch:"
    ],
    "search_term": [
        "What are you looking for?",
        "Enter your search term, or just mash the keyboard:",
        "What's your AI specialty? Type it here:",
        "Enter a search term, or I'll assume you want 'Poorly Drawn Cats':",
        "What kind of digital masterpiece are you seeking?",
        "Type your search term, or just sneeze on the keyboard:",
        "What's your AI dream? Describe it here:",
        "Enter a search term, or I'll just randomly generate one:",
        "What pixelated wonder are you after?",
        "Type your search, or I'll assume you're looking for 'Eldritch Horrors':",
        "What's your digital desire? Spill it:",
        "Enter a search term, or I'll let my pet rock decide:",
        "What AI-generated nightmare fuel are you seeking?",
        "Type your search, or I'll assume you want 'Abstract Potato Art':",
        "What's your computational craving? Share it here:",
        "Enter a search term, or I'll use predictive text from your last fever dream:",
        "What digital delusion are you chasing?",
        "Type your search, or I'll assume you're looking for 'Surreal Meme Templates':",
        "What's your AI itch? Let's scratch it:",
        "Enter a search term, or I'll just use 'Cosmic Horror Clipart':"
    ],
    "model_select": [
        "Select a model to download or navigate, you indecisive genius:",
        "Select an option already, it's not rocket science:",
        "Choose your digital destiny, or just keep browsing like a zombie:",
        "Select a model, navigate, or just admit you're lost in the AI sauce:",
        "What's it gonna be? Download, navigate, or continue this endless scrolling?",
        "Make a choice, or I'll assume you're here for the witty menu options:",
        "Pick something, or I'll start charging you for browsing time:",
        "Select a model, navigate, or just enjoy this menu like it's Netflix:",
        "Choose your next move, digital adventurer:",
        "What's your pleasure? Download, navigate, or continue this AI window shopping?",
        "Make a decision, or I'll assume you're paralyzed by the awesome choices:",
        "Select something, or admit you're just here to read my hilarious prompts:",
        "Pick a model, navigate, or just keep basking in the glow of this menu:",
        "What'll it be? Download, browse, or continue this digital dance?",
        "Choose your fate: download, navigate, or eternal indecision:",
        "Select a model, move around, or just enjoy the view from AI purgatory:",
        "Make a choice, or I'll assume you're writing down all these witty options:",
        "Pick something, or confess you're just here for the UI experience:",
        "What's next? Download, navigate, or continue this AI shopping spree?",
        "Select your next move, or I'll assume you're stuck in a decision-making loop:",
    ],
    "version_select": [
        "Pick your poison, version junkie:",
        "Which iteration of this digital crack do you want?",
        "Choose your AI vintage, you picky genius:",
        "Select a version, or I'll pick the one that'll melt your GPU:",
        "What flavor of pixel vomit are you in the mood for?",
        "Pick a version, or admit you're just here for the witty prompts:",
        "Choose your digital destiny, you indecisive genius:",
        "Which version of this AI fever dream do you fancy?",
        "Select your preferred flavor of computational chaos:",
        "Pick a version, or I'll assume you want 'Buggy Beta 0.0.1':",
        "What's your AI poison? Choose wisely (or don't, I don't give a fuck):",
        "Select a version, or just close your eyes and point at the screen:",
        "Which digital abomination shall we summon today?",
        "Pick your version, or I'll let my pet rock decide for you:",
        "Choose your AI adventure, you brave little toaster:",
        "Select a version, or I'll assume you're into 'Experimental Clusterfucks':",
        "Which iteration of this pixel circus do you want to download?",
        "Pick a version, or I'll just roll a D20 for you:",
        "Choose your digital weapon, you AI warrior:",
        "Select a version, or admit you're overwhelmed by the awesome choices:"]
}

def get_random_flavor(key):
    return random.choice(MENU_FLAVORS[key])

def display_random_ascii_header():
    colors = ["red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    random_color = random.choice(colors)
    random_header = random.choice(ASCII_HEADERS)
    console.print(random_header, style=random_color)

def display_main_menu() -> str:
    """
    Display the main menu and get user's choice.
    
    Returns:
        str: The action chosen by the user.
    """
    console.clear()
    
    display_random_ascii_header()
    
    console.print(random.choice(WITTY_SUBTITLES), style="italic cyan")
    console.print("\n")
    
    action = inquirer.select(
        message=get_random_flavor("model_select"),
        choices=[
            Choice("download", "Download a model (let's get creative)"),
            Choice("api_key", "Change API key (security first!)"),
            Choice("comfyui_dir", "Change ComfyUI Installation Directory (home sweet home)"),
            Choice("exit", "Exit Program (until next time!)")
        ]
    ).execute()
    return action

def download_model_menu():
    """
    Run the download model menu. It's like a choose-your-own-adventure, but for AI enthusiasts.
    """
    console.clear()
    model_type = inquirer.select(
        message=get_random_flavor("model_type"),
        choices=[
            "ALL", "Checkpoint", "LORA", "Upscaler", "TextualInversion",
            "AestheticGradient", "Hypernetwork", "Unet", "VAE",
            "Workflows", "Other", "Unknown", "Controlnet", "Poses"
        ]
    ).execute()

    base_model = inquirer.select(
        message=get_random_flavor("base_model"),
        choices=[
                  "ALL",
                  "SD 1.4",
                  "SD 1.5",
                  "SD 1.5 LCM",
                  "SD 1.5 Hyper",
                  "SD 2.0",
                  "SD 2.0 768",
                  "SD 2.1",
                  "SD 2.1 768",
                  "SD 2.1 Unclip",
                  "SDXL 0.9",
                  "SDXL 1.0",
                  "SD 3",
                  "Pony",
                  "Flux.1 S",
                  "Flux.1 D",
                  "AuraFlow",
                  "SDXL 1.0 LCM",
                  "SDXL Distilled",
                  "SDXL Turbo",
                  "SDXL Lightning",
                  "SDXL Hyper",
                  "Stable Cascade",
                  "SVD",
                  "SVD XT",
                  "Playground v2",
                  "PixArt a",
                  "PixArt E",
                  "Hunyuan 1",
                  "Lumina",
                  "Kolors",
                  "Other"
        ]
    ).execute()

    sort_by = inquirer.select(
        message=get_random_flavor("sort_by"),
        choices=[
            "Highest Rated", "Most Downloaded", "Most Liked",
            "Most Discussed", "Most Collected", "Most Images",
            "Newest", "Oldest"
        ]
    ).execute()

    query = inquirer.text(message=get_random_flavor("search_term")).execute()

    cursor = None  # Initialize cursor
    previous_cursors: deque = deque(maxlen=5)  # Limit history to the last 5 pages

    while True:
        console.clear()  # Clear the screen before showing results
        models, metadata = search_models(get_api_key(), model_type, base_model, sort_by, query, cursor)
        
        if not models:
            console.print("[bold red]No models found. Your search fu is weak, grasshopper.[/bold red]")
            input("\nPress Enter to return to the main menu.")
            return

        table = Table(title="Search Results")
        table.add_column("Index", style="cyan")
        table.add_column("Model Name", style="magenta")
        table.add_column("Type", style="red")
        table.add_column("Base Model", style="green")
        table.add_column("Downloads", style="yellow")
        table.add_column("Model Page", style="blue")  # New column for model page links

        for i, model in enumerate(models, 1):
            model_name = model.get('name', 'Unknown Model')
            model_url = f"https://civitai.com/models/{model['id']}"  # Construct the model URL
            base_model = model.get('modelVersions', [{}])[0].get('baseModel', 'Unknown')
            download_count = model.get('stats', {}).get('downloadCount', '0')
            model_type = model.get('type', 'Unknown')

            table.add_row(
                str(i),
                f"[link={model_url}]{model_name}[/link]",  # Hyperlink for model name
                model_type,
                base_model,
                str(download_count),
                model_url  # Add model URL in the new column
            )

        console.print(table)

        # Add pagination options
        pagination_choices = []
        if previous_cursors:  # Check if we can go back
            pagination_choices.append(Choice("previous_page", "[PREVIOUS PAGE]"))

        # Add model selection options
        model_choices = [Choice(str(i), model['name']) for i, model in enumerate(models, 1)]
        
        # Add main menu and next page options
        navigation_choices = [
            Choice("main_menu", "[RETURN TO MAIN MENU]"),
        ]
        if metadata.get('nextPage'):
            navigation_choices.append(Choice("next_page", "[NEXT PAGE]"))
        
        all_choices = pagination_choices + model_choices + navigation_choices

        selected_index = inquirer.select(
            message="Select a model to download or navigate:",
            choices=all_choices
        ).execute()

        if selected_index == "main_menu":
            return  # This will exit the download_model_menu function and return to the main menu

        elif selected_index == "previous_page":
            if previous_cursors:
                cursor = previous_cursors.pop()
                continue
            else:
                console.print("[bold red]No previous page available, you time-traveling wannabe.[/bold red]")
                input("Press Enter to continue, or just sit there and contemplate your life choices...")
                continue

        elif selected_index == "next_page":
            if metadata.get('nextPage'):
                previous_cursors.append(cursor)
                cursor = metadata['nextCursor']
                continue
            else:
                console.print("[bold red]No next page available. You've reached the end of the internet.[/bold red]")
                input("Press Enter to continue, or just stare at the screen like a zombie...")
                continue

        try:
            model = models[int(selected_index) - 1]
            
            versions = model['modelVersions']

            version_table = Table(title=f"Model Versions: {model['name']}")
            version_table.add_column("AName", style="cyan")
            version_table.add_column("baseModel", style="blue")
            version_table.add_column("Size", style="magenta")
            version_table.add_column("Downloads", style="yellow")
            version_table.add_column("Rating", style="green")
            
            version_choices = []

            for i, version in enumerate(versions, 1):
                version['type'] = model.get('type', "Unknown")
                version_name = version.get('name', f"Version {i}")
                version_size = f"{version['files'][0]['sizeKB'] / 1024:.2f} MB"  # Format this shit
                version_downloads = str(version['stats']['downloadCount'])  # Stringify this mofo
                version_thumbs_up = version['stats']['thumbsUpCount']
                version_thumbs_down = version['stats']['thumbsDownCount']
                version_rating = f"{(version_thumbs_up / (version_thumbs_up + version_thumbs_down)) * 100:.2f}%"  # Format this bastard
                version_base_model = version.get('baseModel', 'Unknown')

                version_choices.append(Choice(str(i), f"{version_name}"))
        
                version_table.add_row(
                    version_name,
                    version_base_model,
                    version_size,
                    version_downloads,
                    version_rating
                )
            console.print(version_table)
                           
            selected_version_index = inquirer.select(
                message=get_random_flavor("version_select"),  # Use the new flavor here
                choices=version_choices
            ).execute()
       
            download_version(versions[int(selected_version_index) - 1], get_comfyui_dir(), get_api_key())

            input("\nPress Enter to continue...")

        except Exception as e:
            print(f"Holy shitballs! Something went wrong: {e}")
            input("Press Enter to continue, or go cry in a corner...")
            continue
