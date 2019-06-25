from .base_player import BasePlayer
import random

class MonteCarloPlayer(BasePlayer):

    def info(self):
        info = {'name': "RandomPlayer"}
        return info

    def select_move(self, select_time, state, moves):
        return random.choice(moves)

    def study(self, study_time):
        pass

    def prepare(self, prepare_time):
        pass

    def depth_charge(self, init_state):
        pass