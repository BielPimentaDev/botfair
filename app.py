from lib.bot import bot
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import threading
import uuid
import time
from tenacity import retry, stop_after_attempt, wait_fixed
from bdd import show_table,show_bot_by_id, create_stoped_bot, stoped_bots_list
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By

app = Flask(__name__)
stop_event = threading.Event()



# @retry(wait=wait_fixed(2), stop=stop_after_attempt(4))
def start_bot(body, bot_id):
    print('Iniciando bot...')
    body = {
            "above": body['above'], "tie": body['tie'] , "stop_param_lose": body['stop_param_lose'], "stop_param_win": body['stop_param_win'], "stop_time": body['stop_time'], "visitor": body['visitor'], "bot_id": bot_id
        }
    bot(body)
    


bot_id = str(uuid.uuid4())

@app.route('/')
def hello_world():
    return "Hello world"

@app.route('/create_bot', methods=['POST'] )
def create_bot():
    global bot_id
    create_stoped_bot(bot_id)
    bot_id = str(uuid.uuid4())
    body = request.json    
    threading.Thread(target=start_bot, args=(body, bot_id)).start()
    return {"status": 200, "message": "bot has started", "bot_id": bot_id}


    
 
@app.route('/get_bots')
def bots_list():
    table = show_table()    
    return table

@app.route('/show_bot/<id>')
def bot_list(id):
    table = show_bot_by_id(str(id))
    return table


@app.route('/test')
def test_link():
    driver = webdriver.Chrome(
        ChromeDriverManager().install()     
    )

    driver.get("https://www.betfair.com/br")

    print('pegando xpath')

    test = driver.find_element(By.XPATH, '//*')


    print(test.text)
    driver.quit()

    return 'ok'


if __name__ == "__main__":
    """
    above - acima de 2.5 gols
    tie - soma do total de gols igual a 2
    visitor - visitante vence
    coef - coeficiente multiplicador do martingale
    value - aposta inicial
    martingale - numero de jogos martingale
    enabled - se a linha era executar ou nao
    stop_param_lose - valor de parada em perdas
    stop_param_win - valor de parada em ganhos
    stop_time - tempo de espera para reiniciar em minutos
    """
    print('started')
    app.run(port=5000)
    ""
# body = {
#             "above": {"coef": 1.55, "value": 0.77, "martingale": 3, "enabled": True},
#             "tie": {"coef": 1.55, "value": 0.77, "martingale": 3, "enabled": True},
#             "visitor": {"coef": 1, "value": 1, "martingale": 2, "enabled": True},
#             "stop_param_lose": -0.5,
#             "stop_param_win": 0.5,
#             "stop_time": 180,
#         }
   




   