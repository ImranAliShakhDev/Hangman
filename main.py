import os
import random
from typing import Dict, List, Set, Union

ASSETS_FILE = "assets.txt"
DICTIONARY_FILE = "dict.txt"
HANGMAN_STAGES = {
    1: "FIRST_TRY",
    2: "SECOND_TRY",
    3: "THIRD_TRY",
    4: "FOURTH_TRY",
    5: "FIFTH_TRY",
    6: "SIXTH_TRY"
}
LAST_HANGMAN_ATTEMPT = 6
NEW_GAME_OPTION = 'n'
UNKNOWN_STATE_CHAR = "X"
START_COUNTER = 0
GAME_STATE_WON = "You are the winner!"
GAME_STATE_LOST = "Oh no, you've lost! The correct word was: {word}. Better luck next time!"
GAME_STATE_NOT_FINISHED = "Game is NOT FINISHED!"

game_state: Dict[str, Union[Dict[str,str], str, List[str], Set[str], int]] = {
    "assets": None,
    "random_word": None,
    "masked_word": None,
    "guessed_letters": None,
    "attempts_counter": None
}

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
    while True:
        game_option = input("[N]ew game or [E]xit\n").lower()
        if game_option != NEW_GAME_OPTION:
            print("Have a nice day!")
            break

        print("Let's start!")
        game_state["assets"] = load_ascii_assets(ASSETS_FILE)
        game_state["random_word"] = get_random_word(DICTIONARY_FILE).lower()
        game_state["masked_word"] = [UNKNOWN_STATE_CHAR for _ in range(len(game_state["random_word"]))]
        game_state["guessed_letters"] = set()
        game_state["attempts_counter"] = START_COUNTER
        start_game_loop(game_state)

def start_game_loop(game_state):
    while(check_game_state(game_state) == GAME_STATE_NOT_FINISHED):
        print_state(game_state)
        player_guess = make_player_guess(game_state["guessed_letters"])
        check_player_guess(game_state, player_guess)
    else:
        print(check_game_state(game_state))


def check_game_state(game_state) -> str:
    """
    constant for dict of tries
    counter for key from constant dict
    if counter == L return Game state lost with format string
    while counter up just return game state not finished
    """
    if game_state["attempts_counter"] == LAST_HANGMAN_ATTEMPT:
        return GAME_STATE_LOST.format(word=game_state["random_word"].upper())
    elif are_all_chars_guessed(game_state["masked_word"]):
        return GAME_STATE_WON
    
    return GAME_STATE_NOT_FINISHED

def make_player_guess(guessed_letters: Set[str]) -> str:
    while True:
        player_guess = input("Please, input a letter\n").strip().lower()

        if len(player_guess) != 1 or not player_guess.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
        elif player_guess in guessed_letters:
            print(f"You've already guessed '{player_guess}'. Try a different letter")
            continue

        guessed_letters.add(player_guess)
        return player_guess

def check_player_guess(game_state, player_guess: str):
    if player_guess in game_state["random_word"]:
        for idx, char in enumerate(game_state["random_word"]):
            if char == player_guess:
                game_state["masked_word"][idx] = player_guess.upper()
    else:
        game_state["attempts_counter"] += 1
        attempt_countdown = LAST_HANGMAN_ATTEMPT - game_state["attempts_counter"]
        print(f"\nOops, you gave a wrong letter. Attempts remaining: {attempt_countdown}")

    
def print_state(game_state):
    # print(game_state["random_word"].upper())
    print(''.join(game_state["masked_word"]))
    if game_state["guessed_letters"]:
        print(f"That's your guesses so far: {", ".join(game_state["guessed_letters"])}")
    if game_state["attempts_counter"]:
        key_to_fetch = HANGMAN_STAGES.get(game_state["attempts_counter"])
        attempts_state = game_state["assets"].get(key_to_fetch)
        print(attempts_state)


def are_all_chars_guessed(masked_word: List[str]):
    return UNKNOWN_STATE_CHAR not in masked_word

if __name__ == "__main__":
    start_game_round()