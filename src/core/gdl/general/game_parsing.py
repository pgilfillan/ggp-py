import os

def parse_game(game_name):
    games_path = "/Users/patrickgilfillan/Documents/ggp-lib/games"
    game_dir = os.path.join(games_path, game_name)
    with open(os.path.join(game_dir, game_name + ".gdl"), 'r') as f:
        return f.read().strip()