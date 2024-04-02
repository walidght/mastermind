from flask import Flask, render_template, request
import sys
sys.path.insert(0, '../')
sys.path.insert(0, './api/')
from knuthTree import knuth_all, calcul_candidate, calcul_max_guess_remaining
import itertools

color = '123456'
codes = list(itertools.product(color, repeat=4))
candidates = list(itertools.product(color, repeat=4))
alpha = {(0, 4) : 0, (0, 3) : 1, (0, 2) : 2, (0, 1) : 3, (0, 0) : 4,
        (1, 3) : 5, (1, 2) : 6, (1, 1) : 7, (1, 0) : 8,
        (2, 2) : 9, (2, 1) : 10, (2, 0) : 11,
        (3, 1) : 12, (3, 0) : 13,
        (4, 0) : 14}

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/answer', methods=['POST'])
def getAnswer():
    global answer
    answer = request.json['data']
    print("answer", answer)
    answer = [str(peg) for peg in answer]
    return "OK"

@app.route('/guess', methods=['POST'])
def getGuess():
    global candidates, answer
    all_guesses = request.json['guess']
    eval = request.json['eval']
    nb_guess = request.json['nb_guess']
    print("answer ;", answer)
    print("code", all_guesses)
    guess = [str(i) for i in all_guesses[nb_guess]]
    print("guess", guess)
    print("eval", eval)
    index = alpha[tuple(eval[nb_guess])]
    print("index:", index)
    print('nb_ guess', nb_guess)
    _, list_candidates = calcul_candidate(candidates, guess)
    _, _, _, knuthTree = knuth_all(codes, candidates, guess)
    max_guess_remaining = calcul_max_guess_remaining(nb_guess, knuthTree, tuple(answer))
    candidates = list_candidates[index]
    print("max remaining", max_guess_remaining)
    print("candidates", candidates)
    return {"max" : max_guess_remaining-nb_guess}

if __name__ == '__main__':
    app.run(debug=True)