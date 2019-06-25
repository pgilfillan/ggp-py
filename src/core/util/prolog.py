from pyswip import Prolog
import os


def load_game_description(description):
    prolog = Prolog()
    # First, clear all prior knowledge
    with open('.tmp_pl', 'w') as f:
        f.write("")
    prolog.consult('.tmp_pl')
    os.remove('.tmp_pl')

    with open('.tmp_pl', 'w') as f:
        f.write(description)
    prolog.consult('.tmp_pl')
    os.remove('.tmp_pl')