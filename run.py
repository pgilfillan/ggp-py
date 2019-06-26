from src.core.statemachines.prolog import PrologStateMachine
from config import default
from src.core.management.match import Match, MatchSpec

import inspect
import argparse
import sys
import pkgutil
from importlib import import_module


def load_players(match, sm):
    if args.players == None:
        players = {}
        players_mod = import_module("src.players")
        for importer, modname, ispkg in pkgutil.walk_packages(path=players_mod.__path__,
                                                              prefix=players_mod.__name__ + '.',
                                                              onerror=lambda x: None):
            mod = import_module(modname)
            for _, obj in inspect.getmembers(mod):
                if inspect.isclass(obj):
                    if default.player == obj.__name__:
                        for role_name in sm.roles:
                            players[role_name] = obj(match, role_name)

        if len(players) == 0:
            print("Unable to find default.player class")
            sys.exit(1)
    elif len(args.players) != len(sm.roles):
        print("%d players specified, but given game requires %d roles" % (len(args.players), len(sm.roles)))
        sys.exit(1)
    else:
        players = {}
        num_found = 0
        players_mod = import_module("src.players")
        for importer, modname, ispkg in pkgutil.walk_packages(path=players_mod.__path__,
                                                              prefix=players_mod.__name__ + '.',
                                                              onerror=lambda x: None):
            mod = import_module(modname)
            for _, obj in inspect.getmembers(mod):
                if inspect.isclass(obj):
                    for player_name in args.players:
                        if player_name == obj.__name__:
                            players[sm.roles[num_found]] = obj(match, sm.roles[num_found])
                            num_found += 1

        if num_found != len(sm.roles):
            print("Was only able to find %d of the %d players specified" % (num_found, len(args.players)))
            sys.exit(1)

    return players


def main():
    game_description_pl = "games/" + args.game + "/" + args.game + ".pl"
    with open(game_description_pl, 'r') as f:
        game_description = f.read()

    sm = PrologStateMachine(game_description)
    match = Match(MatchSpec(game_description))
    players = load_players(match, sm)

    # Start games
    for run in range(args.num_matches):
        print("#### STARTING MATCH %d ####" % (run + 1))

        # Study
        if args.study_time != 0:
            for role_name in players:
                players[role_name].study(args.study_time)

        # Prepare
        for role_name in players:
            players[role_name].prepare(args.prepare_time)

        curr_state = sm.get_initial_state()
        moves_played = 0
        while moves_played < args.max_moves and not sm.is_terminal(curr_state):
            print("Curr state:", curr_state)
            joint_moves = sm.get_legal_joint_moves(curr_state)
            next_moves = {}
            for role_name in joint_moves:
                next_moves[role_name] = players[role_name].select_move(args.select_time, curr_state, joint_moves[role_name])
            print("Chosen moves:", next_moves)
            curr_state = sm.get_next_state(curr_state, next_moves)
            moves_played += 1

        if moves_played == args.max_moves:
            print("Game ended before terminating: max moves reached")
        else:
            print("Game ended in", moves_played, "moves")
            print("Ending state:", curr_state)
            print("Player scores: xplayer: ", sm.get_goal_value(curr_state, "xplayer"), "; oplayer: ", sm.get_goal_value(curr_state, "oplayer"))

        print()

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--game', metavar='game_name', help='Name of the game to play', default=default.game)
    arg_parser.add_argument('--players', metavar='players', help='Name of players for the game', nargs='+')
    arg_parser.add_argument('--num_matches', metavar='num_repetitions', help='Number of times to repeat the game',
                            type=int, default=1)
    arg_parser.add_argument('--max_moves', metavar='max_moves', help='Maximum number of moves for each game', type=int,
                            default=100)
    arg_parser.add_argument('--study_time', metavar='study_time',
                            help='TIme limit (s) for player to study the game before the match', type=int, default=0)
    arg_parser.add_argument('--prepare_time', metavar='prepare_time',
                            help='Time limit (s) for player to prepare for the match', type=int, default=60)
    arg_parser.add_argument('--select_time', metavar='select_time',
                            help='Time limit (s) for player to select a move during the match', type=int, default=5)
    args = arg_parser.parse_args()

    main()