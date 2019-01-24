from core.dl_parsing.general.game_parsing import parse_game
from core.management.match import Match

class GameManager:

    match_queue = []
    games = {}

    def add_match(self, match):
        self.match_queue.append(match)

    def add_matches(self, matches):
        self.match_queue.extend(matches)

    def start_matches(self):
        for match_spec in self.match_queue:
            #If contains, use description already
            description = parse_game(match_spec.game)
            self.games[match_spec.game] = description
            new_match = Match(match_spec, description)
            self.run_match(new_match)

    def run_match(self, match):
        print("Running match with description")
        print(match.description)

    def flush_games(self):
        self.games = {}