from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from dotenv import load_dotenv

from os import getenv

from lib.bet import Bet
from lib.login import Login

from lib.utils import is_same_scoreboard

load_dotenv()

betfair_email = getenv("BETFAIR_EMAIL")
betfair_password = getenv("BETFAIR_PASSWORD")
headless = getenv("HEADLESS")


def bot(options):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")

    if headless == "true":
        chrome_options.add_argument("--headless")

#    driver = webdriver.Chrome("./chromedriver", chrome_options=chrome_options)
    driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        chrome_options=chrome_options,
    )

    login = Login(driver)
    login.setup_login(betfair_email, betfair_password)

    bet = Bet(driver, options)

    bet.start()
