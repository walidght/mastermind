from flask import Flask, render_template, request
import sys
sys.path.insert(0, '../')
sys.path.insert(0, './api/')
from knuthTree import knuth_all, calcul_candidate, calcul_max_guess_remaining

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/answer', methods=['POST'])
def getAnswer():
    answer = request.json['data']
    print("answer", answer)
    return "OK"

@app.route('/guess', methods=['POST'])
def getGuess():
    code = request.json['guess']
    eval = request.json['eval']
    nb_guess = request.json['nb_guess']
    print("code", code)
    print("eval", eval)
    print('nb_ guess', nb_guess)
    return "OK"

if __name__ == '__main__':
    app.run(debug=True)