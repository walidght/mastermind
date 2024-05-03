from flask import Flask, render_template, request
import sys
sys.path.insert(0, '../')
sys.path.insert(0, './api/')
from knuthTree import knuth_all, calcul_candidate, calcul_max_guess_remaining
import itertools

color = '123456'
codes = list(itertools.product(color, repeat=4))
candidates = list(itertools.product(color, repeat=4))
candidates_AI = list(itertools.product(color, repeat=4))
alpha = {(0, 4) : 0, (0, 3) : 1, (0, 2) : 2, (0, 1) : 3, (0, 0) : 4,
        (1, 3) : 5, (1, 2) : 6, (1, 1) : 7, (1, 0) : 8,
        (2, 2) : 9, (2, 1) : 10, (2, 0) : 11,
        (3, 1) : 12, (3, 0) : 13,
        (4, 0) : 14}

app = Flask(__name__, static_url_path='', static_folder='static')
strategy = None
knuth_second_codes = [['2', '2', '1', '1'], ['1', '2', '1', '3'], ['2', '3', '4', '4'], ['2', '3', '5', '5'], ['3', '3', '4', '6'],
                      None, ['1', '2', '1', '4'], ['1', '1', '3', '4'], ['1', '3', '5', '5'], 
                      ['1', '2', '1', '3'], ['1', '2', '2', '4'], ['1', '2', '3', '4'],
                      None, ['1', '2', '2', '3'],
                      ['1', '1', '2', '2']]
lastKnuthTree = None

@app.route('/')
def index():
    return render_template('title.html')
        
@app.route('/solo')
def solo():
    #print("solo")
    return render_template('index.html')

@app.route('/difficulty')
def difficulty():
    #print("difficulty")
    return render_template('difficulty.html')

@app.route('/select_difficulty', methods=['POST'])
def select_difficulty():
    global strategy
    difficulty = request.json['mode']
    if difficulty == 0:
        strategy = normal
    else:
        strategy = hard
    #print("strategy =", strategy)
    return "OK"

@app.route('/vs')
def vs():
    #print("vs")
    #print("strategy =", strategy)
    return render_template('vs.html')

@app.route('/answer', methods=['POST'])
def getAnswer():
    global answer
    answer = request.json['data']
    answer = [str(peg+1) for peg in answer]
    return "OK"

@app.route('/guess', methods=['POST'])
def evalGuess():
    global candidates
    all_guesses = request.json['guess']
    eval = request.json['eval']
    nb_guess = request.json['nb_guess']
    guess = [str(i+1) for i in all_guesses[nb_guess-1]]
    index = alpha[tuple(eval[nb_guess-1])]
    _, list_candidates = calcul_candidate(candidates, guess)
    if nb_guess == 0:
        candidates = list_candidates[index]
        return "5,"+str(len(candidates))
    else:
        _, _, _, knuthTree = knuth_all(codes, candidates, guess)
        max_guess_remaining = calcul_max_guess_remaining(0, knuthTree)
        candidates = list_candidates[index]
        return str(max_guess_remaining)+','+str(len(candidates))
    
@app.route('/AI', methods=['POST'])
def guess_AI():
    global candidates_AI
    nb_guess = request.json['nb_guess']
    if nb_guess == 0:
        guess = ['1', '1', '2', '2']
    else:
        eval = request.json['eval']
        index = alpha[tuple(eval[nb_guess-1])]
        guess = strategy(nb_guess, index)

    str_guess = ''
    for c in guess:
        str_guess += c

    #print("str_guess =", str_guess)

    return str_guess
    
def normal(nb_guess, index):
    global candidates_AI
    #print("normal")
    return candidates_AI[0]

def hard(nb_guess, index):
    global candidates_AI
    #print("hard, nb_guess", nb_guess)
    if nb_guess == 1:
        #print("AI guesses ", knuth_second_codes[index])
        return knuth_second_codes[index]
    else:
        #print("lastKnuthTree =", lastKnuthTree[index])
        if len(lastKnuthTree[index]) == 2:
            print("ici", lastKnuthTree[index])
            return lastKnuthTree[index][1][0]
        else:
            return lastKnuthTree[index][2]
    
@app.route('/AI_eval', methods=['POST'])
def evalGuessAI():
    global candidates_AI, lastKnuthTree
    all_guesses = request.json['guess']
    eval = request.json['eval']
    nb_guess = request.json['nb_guess']
    
    print("all_guesses_AI =", all_guesses)
    print("eval_AI =", eval)
    print("nb_guess_AI =", nb_guess)
    guess = [str(all_guesses[nb_guess-1][i]+1) for i in range(4)]
    index = alpha[tuple(eval[nb_guess-1])]
    #print("guess_AI =", guess)
    #print("")
    _, list_candidates = calcul_candidate(candidates_AI, guess)
    tmp = candidates_AI[:]
    candidates_AI = list_candidates[index]
    if nb_guess > 0:
        _, _, _, lastKnuthTree = knuth_all(codes, tmp, guess)
        print("nb_guess", nb_guess)
        print("lastKnuthTree", lastKnuthTree)
    return "OK"

if __name__ == '__main__':
    app.run(debug=True)