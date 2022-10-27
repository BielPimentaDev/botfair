import time
from selenium.webdriver.common.by import By


import time
from lib.entities.game import Game

from lib.utils import get_hour_from_string

# initial_value = valor de aposta
# factor = coeficiente de aposta


class Martingale:
    def __init__(self, driver, initial_value, factor, number):
        self.driver = driver
        self.bet = self.initial_value = initial_value
        self.factor = factor
        self.number = number
        self.attempts = 0
        self.current_value = 0

    def play(self, xpath):
        if self.attempts != 0:
            self.bet *= self.factor
        self.attempts += 1
        self.make_bet(xpath)
        if self.attempts == self.number + 1:
            self.reset()

    def reset(self):
        self.attempts = 0
        self.bet = self.initial_value

    def get_last_game_result(self):
        last_game = self.driver.find_element(
            By.CSS_SELECTOR, ".between-arrows > .title"
        )
        last_teams = self.driver.find_elements(
            By.CSS_SELECTOR, ".teams > .individual-team"
        )
        last_score = self.driver.find_elements(
            By.CSS_SELECTOR, ".match-results > .side-container"
        )

        hour = get_hour_from_string(last_game.text)

        team_1 = last_teams[0].text
        team_2 = last_teams[1].text
        score_1 = int(last_score[0].text)
        score_2 = int(last_score[1].text)

        info = f"{hour} {team_1} {score_1} - {score_2} {team_2}"

        return Game([team_1, team_2], [score_1, score_2], hour, info)

    def make_bet(self, xpath):
        time.sleep(1)
        print(f"Fazendo aposta com {self.bet}")
        button = self.driver.find_element(
            By.XPATH,
            xpath,
        )
        time.sleep(1)
        # print(f"xpath button = {xpath}")
        button.click()

        time.sleep(1)
        
        self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[2]/div[2]/div/div[2]/div[3]/div/div/div/div[1]/form/div/div[2]/div/div[3]/div[2]/div/ul/li/div[2]/div[2]/div/div[1]/div/input[1]",
        ).send_keys(round(self.bet, 2))

        time.sleep(1)

        self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[2]/div[2]/div/div[2]/div[3]/div/div/div/div[1]/form/div/div[3]/div[3]/div[2]/button",
        ).click()
        time.sleep(2)

        self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[2]/div[2]/div/div[2]/div[3]/div/div/div/div[3]/div/div[3]/div[2]/button",
        ).click()
