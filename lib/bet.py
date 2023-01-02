
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bdd import write_in_bdd
from datetime import date, datetime, timedelta
from lib.entities.game import Game
from lib.martingale import Martingale
import threading
from lib.utils import (
    get_hour_from_string,
)

from bdd import stoped_bots_list

import time



class Bet:
    def __init__(self, driver, options):
        driver.get("https://www.betfair.com/sport/virtuals/football-world-cup")
        self.above_enabled = options.get("above")
        self.tie_enabled = options.get("tie")
        self.visitor_enabled = options.get("visitor")
        self.bot_id = options.get("bot_id")
        self.driver = driver
        self.current_points_to_stop = 0
        self.stop_param_win = options.get("stop_param_win")
        self.stop_param_lose = options.get("stop_param_lose")
        self.stop_time = options.get("stop_time")
        self.stop_operation = False
        self.tie = Martingale(
            driver,
            self.tie_enabled.get("value"),
            self.tie_enabled.get("coef"),
            self.tie_enabled.get("martingale"),
        )
        self.above = Martingale(
            driver,
            self.above_enabled.get("value"),
            self.above_enabled.get("coef"),
            self.above_enabled.get("martingale"),
        )
        self.visitor = Martingale(
            driver,
            self.visitor_enabled.get("value"),
            self.visitor_enabled.get("coef"),
            self.visitor_enabled.get("martingale"),
        )
        self.options = options
        
    def stop(self):
        self.stop_operation = True

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

    # start the bet
    def start(self):
        hour2bet = self.driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/div[1]/div/div/span[1]",
        ).text
        hour, minutes = hour2bet.split(":")
        now = datetime.now()
        bet_hour = datetime(
            datetime.now().year,
            datetime.now().month,
            datetime.now().day,
            int(hour),
            int(minutes),
        )

        time_to_wait = (bet_hour - now).seconds
        if time_to_wait < 300: 
            print(
                f"Aguardando {time_to_wait} segundos até {hour2bet} para realizar a primeira aposta"
            )
            time.sleep(time_to_wait)
        else:
            time.sleep(5)
            self.start()
        
        while True:
            print(f'BOT {self.bot_id}')
            list_to_check = stoped_bots_list()
            if self.bot_id in list_to_check:
                print('Parando por ja ter outro bot sendo iniciado')
                break 
            if ( self.stop_param_lose >= self.current_points_to_stop or self.current_points_to_stop >= self.stop_param_win ):
                print(
                    f"Criterio de parada alcancado: {self.current_points_to_stop}")
                self.current_points_to_stop = 0                
                time.sleep(self.stop_time * 60)
                print("Término do tempo de parada.")

            print("Aguardando o ultimo jogo ser atualizado")
            print(f"Total de pontos: {self.current_points_to_stop}")


            time.sleep(180)
            last_game_info = self.get_last_game_result().info
            while True:
                time.sleep(3)
                self.driver.get(
                    "https://www.betfair.com/sport/virtuals/football-world-cup"
                )
                last_game_result = self.get_last_game_result()
                if last_game_info != last_game_result.info:
                    print(last_game_result.info)
                    break
            score = last_game_result.scores

            if self.above_enabled["enabled"]:
                self.is_sum_of_goals_is_above_2_5(score)
            if self.tie_enabled["enabled"]:
                self.is_tie(score)
            if self.visitor_enabled["enabled"]:
                self.is_sum_of_goals_bellow_2_5(score)
            if self.stop_operation:
                self.stop_operation = False
                break

    def winning_bet(self, value_to_increase: Martingale, increase_xpath, type_of_operation):
        value = float(self.driver.find_element(By.XPATH, increase_xpath).text)
        gain = (
            value_to_increase.bet * value
        ) - value_to_increase.bet
        
        self.current_points_to_stop += gain
        message = f"Green: +{gain}"
        write_in_bdd(self.bot_id,gain, f'green {type_of_operation}' )
        
        

    def losing_bet(self, value_to_decrease: Martingale, type_of_operation):
        loss = value_to_decrease.bet
        self.current_points_to_stop -= loss
        
        write_in_bdd(self.bot_id, loss, f'red {type_of_operation}')
       
#SOMA DE 2.5 GOLS
    def is_sum_of_goals_is_above_2_5(self, score):
        xpath = "/html/body/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/a"
        if score[0] + score[1] >= 2.5:
            self.winning_bet(self.above, xpath,'goals > 2.5')
            self.above.reset()
        else:
            self.losing_bet(self.above,'goals > 2.5')
            
        self.above.play(xpath)
#TOTAL DE GOLS 2
    def is_tie(self, score):
        xpath = "/html/body/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/div[1]/div[6]/div[2]/div/div[3]/div/div[2]/a"
        if score[0] + score[1] == 2:
            self.winning_bet(self.tie, xpath, 'goals = 2')
            self.tie.reset()
        else:
            self.losing_bet(self.tie, 'goals = 2')

        self.tie.play(xpath)

#MENOS DE 2.5 GOLS
    def is_sum_of_goals_bellow_2_5(self, score):
        xpath = "/html/body/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/div[1]/div[3]/div[2]/div/div/div[1]/div/div[2]/a"
        if score[0] + score[1] <= 2.5:
            self.winning_bet(self.visitor, xpath, 'goals < 2.5')
            self.visitor.reset()
        else:
            self.losing_bet(self.visitor, 'goals < 2.5')

        self.visitor.play(xpath)


