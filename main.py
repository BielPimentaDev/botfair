from lib.bot import bot
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

def start_bot(above, tie,visitor, stop_param_lose, stop_param_win, stop_time):
    body = {
        "above": above, "tie": tie , "stop_param_lose": stop_param_lose, "stop_param_win": stop_param_win, "stop_time": stop_time
    }
    print('iniciando bot')
    bot(body)
    print("bot terminou")

@app.route('/start_bot', methods=['POST'] )
def hello():
    body = request.json
    threading.Thread(target=start_bot, args=body).start()
    return {"status": 200, "message": "bot has started"}

@app.route('/le_bdd')
def banco():
    return """
    DATA E HORA DA MENSAGEM : MENSAGEM DO BOT    
    """




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
    app.run()



body = {
        "above": {"coef": 1.55, "value": 0.77, "martingale": 3, "enabled": True},
        "tie": {"coef": 1.55, "value": 0.77, "martingale": 3, "enabled": True},
        "visitor": {"coef": 1, "value": 1, "martingale": 2, "enabled": True},
        "stop_param_lose": -0.5,
        "stop_param_win": 0.5,
        "stop_time": 180,
    }


   