from base_player import BasePlayer
import random

class RandomPlayer(BasePlayer):

    def info(self):
        info = {'name': "RandomPlayer"}
        return info

    def select_move(self, select_time, state, moves):
        return random.choice(moves)