from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By


driver = webdriver.Chrome(
        ChromeDriverManager().install()     
    )

driver.get("https://www.google.com/")

print('pegando xpath')

test = driver.find_element(By.XPATH, '//*')
print(test.text)



driver.quit()