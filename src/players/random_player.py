from .base_player import BasePlayer
import random

class RandomPlayer(BasePlayer):

    def info(self):
        info = {'name': "RandomPlayer"}
        return info

    def select_move(self, select_time, state, moves):
        return random.sample(moves, 1)[0]

    def study(self, study_time):
        pass

    def prepare(self, prepare_time):
        pass