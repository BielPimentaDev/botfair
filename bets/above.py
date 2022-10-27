import time
from lib.martingale import Martingale


class Above(Martingale):
    def __init__(self, driver, options):
        bet = options.get("above")
        self.bet = Martingale(driver, bet.get("value"), bet.get("coef"))
        self.driver = driver
        self.options = options

    def play(self):
        print(
            "Aguardando o ultimo jogo ser atualizado para apostar em acima de 2.5 gols"
        )
        # time.sleep(180)
        last_game_info = self.get_last_game_result().info
        while True:
            time.sleep(3)
            last_game_result = self.get_last_game_result()
            if last_game_info != last_game_result.info:
                break
        score = last_game_result.scores
        xpath = "/html/body/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/a"
        if score[0] + score[1] >= 2.5:
            self.bet.make_bet(xpath)
            self.bet.reset()
        else:
            self.bet.play(xpath)
