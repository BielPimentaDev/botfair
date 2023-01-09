import time
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class Login:
    def __init__(self, driver):
        self.driver = driver

    def setup_login(self, email, password):
        self.driver.get("https://www.betfair.com/br")

        # accept cookies
        print('try login')
        
        button_accept_cookies_id = "onetrust-accept-btn-handler"

        accept_cookies_button = WebDriverWait(self.driver, timeout=15).until(
            lambda d: d.find_element(By.ID, button_accept_cookies_id)
        )
        print('keep')

        accept_cookies_button.click()
       
        # WebDriverWait(self.driver, timeout=15).until(
        #     lambda d: d.find_element(By.ID, button_accept_cookies_id)
        # )
        # accept_cookies_button = self.driver.find_element(
        #     By.ID, button_accept_cookies_id
        # )

      
        # accept_cookies_button.click()

        # setup login
        email_input = self.driver.find_element(By.ID, "ssc-liu")
        email_input.send_keys(email)

        password_input = self.driver.find_element(By.ID, "ssc-lipw")
        password_input.send_keys(password)

        login_button = self.driver.find_element(By.ID, "ssc-lis")
        login_button.click()

        time.sleep(5)
        # wait login
        # WebDriverWait(self.driver, timeout=20).until(
        #     lambda d: d.find_element(By.XPATH, "// td[@class='ssc-wla']")
        # )
