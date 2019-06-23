from src.core.statemachines.prolog import PrologStateMachine
from config import default
import inspect

import argparse
import random
import sys
import pkgutil
from importlib import import_module

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--game', metavar='game_name', help='Name of the game to play', default=default.game)
arg_parser.add_argument('--players', metavar='players', help='Name of players for the game', nargs='+')
arg_parser.add_argument('--num_games', metavar='num_repetitions', help='Number of times to repeat the game', type=int, default=1)
args = arg_parser.parse_args()

game_description = "games/" + args.game + "/" + args.game + ".pl"
sm = PrologStateMachine(game_description)

# Load players for the game
if args.players == None:
    players = [default.player]*len(sm.roles)
elif len(args.players) != len(sm.roles):
    print("%d players specified, but given game requires %d roles" % (len(args.players), len(sm.roles)))
    sys.exit(1)
else:
    players = [None]*len(sm.roles)
    num_found = 0
    players_mod = import_module("src.players")
    for importer, modname, ispkg in pkgutil.walk_packages(path=players_mod.__path__,
                                                          prefix=players_mod.__name__ + '.',
                                                          onerror=lambda x: None):
        mod = import_module(modname)
        for _, obj in inspect.getmembers(mod):
            if inspect.isclass(obj):
                for i in range(len(players)):
                    if args.players[i] == obj.__name__:
                        players[i] = obj(game_description)
                        num_found += 1

    if num_found != len(players):
        print("Was only able to find %d of the %d players specified" % (num_found, len(players)))
        sys.exit(1)

# Start games
for run in range(args.num_games):
    curr_state = sm.get_initial_state()

    moves_played = 0
    max_moves = 20
    while moves_played < max_moves and not sm.is_terminal(curr_state):
        print("Curr state:", curr_state)
        joint_moves = sm.get_legal_joint_moves(curr_state)
        next_moves = {}
        for player in joint_moves:
            next_moves[player] = random.choice(joint_moves[player])
        print("Chosen moves:", next_moves)
        curr_state = sm.get_next_state(curr_state, next_moves)
        moves_played += 1

    if moves_played == max_moves:
        print("Game ended before terminating: max moves reached")
    else:
        print("Game ended in", moves_played, "moves")
        print("Ending state:", curr_state)
        print("Player scores: xplayer: ", sm.get_goal_value(curr_state, "xplayer"), "; oplayer: ", sm.get_goal_value(curr_state, "oplayer"))
