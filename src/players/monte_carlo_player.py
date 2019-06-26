from .base_player import BasePlayer
from ..core.statemachines.prolog import PrologStateMachine

import random
import time

class MonteCarloPlayer(BasePlayer):

    def info(self):
        info = {'name': "MonteCarloPlayer"}
        return info

    def select_move(self, select_time, state, moves):
        if len(moves) == 1:
            return moves[0]

        start = time.time()
        time.clock()
        elapsed = 0

        curr_index = 0
        values = [0]*len(moves)
        num_charges = [0]*len(moves)
        while (elapsed < select_time):
            values[curr_index] += self.depth_charge(state, moves[curr_index])
            num_charges[curr_index] += 1
            curr_index += 1
            if curr_index == len(moves):
                curr_index = 0
            elapsed = time.time() - start

        for i in range(len(values)):
            values[i] /= num_charges[i]

        curr_max_index = 0
        curr_max = 0
        for i in range(len(values)):
            if values[i] > curr_max:
                curr_max_index = i
                curr_max = values[i]

        return moves[curr_max_index]

    def study(self, study_time):
        pass

    def prepare(self, prepare_time):
        self.sm = PrologStateMachine(self.match.spec.game_description)

    def depth_charge(self, init_state, init_move=None):
        curr_state = init_state
        if init_move is not None:
            joint_moves = self.sm.get_legal_joint_moves(curr_state)
            chosen_moves = {}
            for role in joint_moves:
                if role == self.role:
                    chosen_moves[role] = init_move
                else:
                    chosen_moves[role] = random.choice(joint_moves[role])
            curr_state = self.sm.get_next_state(curr_state, chosen_moves)

        while not self.sm.is_terminal(curr_state):
            joint_moves = self.sm.get_legal_joint_moves(curr_state)
            chosen_moves = {}
            for role in joint_moves:
                chosen_moves[role] = random.choice(joint_moves[role])
            curr_state = self.sm.get_next_state(curr_state, chosen_moves)

        return self.sm.get_goal_value(curr_state, self.role)