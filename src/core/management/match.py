
class Match:

    def __init__(self, spec, description):
        self.spec = spec
        self.description = description

class MatchSpec:

    def __init__(self, game, players, study_time, start_time, decide_time):
        self.game = game
        self.players = players
        self.study_time = study_time
        self.start_time = start_time
        self.decide_time = decide_time