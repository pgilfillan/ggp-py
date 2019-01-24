import sys
sys.path.insert(0,'..')
from core.management.manager import GameManager
from core.management.match import Match, MatchSpec
from core.dl_parsing.general.game_parsing import parse_game
import argparse

# Parse arguments
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('game_name', metavar='game_name', help='Name of the game to play')
arg_parser.add_argument('player1', metavar='player 1', help='Name of Player 1')
arg_parser.add_argument('player2', metavar='player 2', help='Name of Player 2')
args = arg_parser.parse_args()

# Setup manager
m = GameManager()
games = []
games.append(args.game_name)

for game in games:
    new_match_spec = MatchSpec(game, (args.player1, args.player2), 0, 60, 10)
    m.add_match(new_match_spec)
    m.start_matches()