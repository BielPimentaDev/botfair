class Game:
    teams = []
    scores = []
    hour = None
    info = None

    def __init__(self, teams, scores, hour, info):
        self.teams = teams
        self.scores = scores
        self.hour = hour
        self.info = info
