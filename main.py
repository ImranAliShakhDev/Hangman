import os
import random
from typing import Dict, List, Optional

ASSETS_FILE = "assets.txt"
DICTIONARY_FILE = "dict.txt"

def load_ascii_assets(file_name: str) -> Dict[str, str]:
    """
    Load ASCII assets from a txt file and return it as a dictionary

    :param file_name: The name of the file containing ASCII assets.
    :return: A dictionary where keys are identifiers and values are ASCII assets multiline strings.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)

    with open(file_path, 'r') as file:
        lines = file.read().strip().split('\n\n')
        ascii_assets = {}
        for section in lines:
            key, *art = section.split('\n')
            ascii_assets[key.strip()] = '\n'.join(art)
        return ascii_assets
    
def get_random_word(file_name: str) -> str:
    """
    Load words from a text file and choose random word

    :param file_name: The name of the file containing words.
    :return: A randomly selected word.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)

    with open(file_path, 'r') as file:
        words: List[str] = [line.strip() for line in file if line.strip()]
    return random.choice(words)

def start_game_round():
    """
    get game option
    make set up: load assets and get random word
    if new game start game loop
    make start_game_loop
    """
    game_option = input("[N]ew game or [E]xit\n").lower()
    if game_option == 'n':
        print("Let's start!")
        ascii_assets = load_ascii_assets(ASSETS_FILE)
        random_word = get_random_word(DICTIONARY_FILE)
        start_game_loop(ascii_assets, random_word)
    elif game_option == 'e':
        print("Have a nice day!")

def start_game_loop(assets: Dict[str, str], random_word: str):
    """
    make check_game_state via counter for dict of try and get needed asset for print
    while loop were we get asking for guessing char of the random word
    and make rendering of hidden random word and counter for getting suitable
    asset in sequence of tries
    and make constants where we print if player win or lose and asking for next try
    """
    key_to_fetch = "SECOND_TRY"
    fallback_value = "ASCII asset not found"
    result: Optional[str] = assets.get(key_to_fetch, fallback_value)
    print(result)
    print(f"Random word: {random_word}")


if __name__ == "__main__":
    start_game_round()