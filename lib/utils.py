# if the string is "19:55 Switzerland 2 - 1 Spain", it returns ['2', '1']
def get_scores_from_string(string):
    infos = string.split(" ")
    scores = []
    for data in infos:
        if data.isnumeric():
            scores.append(int(data))

    return scores


# if the string is "19:55 Switzerland 2 - 1 Spain", it returns ['Switzerland', 'Spain']
def get_teams_from_string(string):
    infos = string.split(" - ")

    team_1 = infos[0].split(" ")
    team_1.pop(0)
    del team_1[-1]
    team_1 = " ".join(team_1)

    team_2 = infos[1].split(" ")
    team_2.pop(0)
    team_2 = " ".join(team_2)

    return [team_1, team_2]


# if the string is "19:55 Switzerland 2 - 1 Spain", it returns "19:55"
def get_hour_from_string(string):
    infos = string.split(" ")
    return infos[0]


def is_same_scoreboard(score, scores_2_verify):
    return score == scores_2_verify or score[::-1] == scores_2_verify
