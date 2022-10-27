import time
from lib.martingale import Martingale


class Tie(Martingale):
    def __init__(self, driver, options):
        bet = options.get("tie")
        self.bet = Martingale(driver, bet.get("value"), bet.get("coef"))
        self.driver = driver
        self.options = options

    def start(self):
        attempts = 1
        while attempts <= self.options.get("attempts"):
            print(
                "Aguardando o ultimo jogo ser atualizado para apostar em soma de 2 gols"
            )
            time.sleep(180)
            last_game_info = self.get_last_game_result().info
            while True:
                time.sleep(3)
                last_game_result = self.get_last_game_result()
                if last_game_info != last_game_result.info:
                    break
            score = last_game_result.scores
            xpath = "/html/body/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/div[1]/div[6]/div[2]/div/div[3]/div/div[2]/a"
            if score[0] + score[1] == 2:
                self.bet.make_bet(xpath)
                self.bet.reset()
            else:
                self.bet.play(xpath)
            attempts += 1
