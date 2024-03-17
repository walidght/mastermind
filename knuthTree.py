import numpy as np
import itertools

def knuth(codes, candidates, guess):
    nb_candidates, list_candidates = calcul_candidate(candidates, guess)
    knuthTree = [None]*15
    answers = []

    # pour chaque alpha(i, j)
    for i in range(len(list_candidates)):
        # s'il a plus que 2 codes possibles
        if len(list_candidates[i]) > 2:
            val_remaining = np.inf
            code_keep = None
            # pour chque code possible
            for code in codes:
                new_nb_candidates, _ = calcul_candidate(list_candidates[i], list(code))
                # si c'est bien la réponse
                if new_nb_candidates == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]:
                    knuthTree[i] = (len(list_candidates[i]), code)
                    code_keep = list(code)
                    break
                # sinon on prend celui qui minimise le plus grand nombre de candidat
                else:
                    # si le plus grand nombre de candidat possible est plus petit que le meilleur stoqué
                    if max(new_nb_candidates) < val_remaining:
                        val_remaining = max(new_nb_candidates)
                        code_keep = list(code)
            if knuthTree[i] == None:
                res, next_answers = knuth(codes, list_candidates[i], code_keep)
                if len(next_answers) < 2:
                    knuthTree[i] = (len(list_candidates[i]), code_keep)
                elif len(next_answers) == 2:
                    knuthTree[i] = (len(list_candidates[i]), next_answers[0]+['x'])
                else:
                    knuthTree[i] = res
            if code_keep not in answers:
                answers.append(code_keep)
        # sinon c'est fini pour cette branche
        else:
            knuthTree[i] = len(list_candidates[i])
            
    return (sum(nb_candidates), guess, knuthTree), answers

def calcul_candidate(p, guess):
    candidate = [0]*15
    allp = []
    # pattern of codemaker (white, black)
    # (0,0), (0,1), (0,2), (0,3), (0,4)
    # (1,0), (1,1), (1,2), (1,3)
    # (2,0), (2,1), (2,2)
    # (3,0), (3,1)
    # (4,0)

    p00 = []
    p01 = []
    p02 = []
    p03 = []
    p04 = []

    p10 = []
    p11 = []
    p12 = []
    p13 = []

    p20 = []
    p21 = []
    p22 = []

    p30 = []
    p31 = []

    p4 = []

    for code in p:
        count_white = 0
        count_black = 4
        remaining_guess = []
        remaining_code = []
        # count black
        for i, guess_peg in enumerate(guess):
            if guess_peg != code[i]:
                count_black -= 1
                remaining_guess.append(guess[i])
                remaining_code.append(code[i])

        # count white
        for i, color_guess in enumerate(remaining_guess):
            if color_guess in remaining_code:
                remaining_code.remove(color_guess)
                count_white += 1

        if count_black == 0:
            if count_white == 0:
                p00.append(code)
            elif count_white == 1:
                p01.append(code)
            elif count_white == 2:
                p02.append(code)
            elif count_white == 3:
                p03.append(code)
            else:
                p04.append(code)
        elif count_black == 1:
            if count_white == 0:
                p10.append(code)
            elif count_white == 1:
                p11.append(code)
            elif count_white == 2:
                p12.append(code)
            else:
                p13.append(code)
        elif count_black == 2:
            if count_white == 0:
                p20.append(code)
            elif count_white == 1:
                p21.append(code)
            else:
                p22.append(code)
        elif count_black == 3:
            if count_white == 0:
                p30.append(code)
            else:
                p31.append(code)
        else:
            p4.append(code)

    candidate[0] = len(p04)
    candidate[1] = len(p03)
    candidate[2] = len(p02)
    candidate[3] = len(p01)
    candidate[4] = len(p00)

    candidate[5] = len(p13)
    candidate[6] = len(p12)
    candidate[7] = len(p11)
    candidate[8] = len(p10)

    candidate[9] = len(p22)
    candidate[10] = len(p21)
    candidate[11] = len(p20)

    candidate[12] = len(p31)
    candidate[13] = len(p30)

    candidate[14] = len(p4)

    allp.append(p04)
    allp.append(p03)
    allp.append(p02)
    allp.append(p01)
    allp.append(p00)

    allp.append(p13)
    allp.append(p12)
    allp.append(p11)
    allp.append(p10)
    
    allp.append(p22)
    allp.append(p21)
    allp.append(p20)

    allp.append(p31)
    allp.append(p30)

    allp.append(p4)

    return candidate, allp

def calcul_count_win(res):
    count = 0
    for res_alpha in res:
        if type(res_alpha) == tuple:
            if len(res_alpha) == 3:
                count += calcul_count_win(res_alpha[2])
    if res[-1] == 1:
        count += 1
    return count

def get_str_knuth_tree(n, guess, knuthTree):
    guess_str = ''
    for x in guess:
        guess_str += x
    buffer = str(n)+'('+guess_str+': '
    for i in range(len(knuthTree)):
        alpha = knuthTree[i]
        if not isinstance(alpha, tuple):
            if i != len(knuthTree)-1:
                buffer += str(alpha)+', '
            else:
                buffer += str(alpha)+')'
        else:
            if len(alpha) == 2:
                subn, sub_guess = alpha
                sub_guess_str = ''
                for x in sub_guess:
                    sub_guess_str += x
                if i != len(knuthTree)-1:
                    buffer += str(subn)+'('+sub_guess_str+'), '
                else:
                    buffer += str(subn)+'('+sub_guess_str+'))'
            else:
                subn, sub_guess, sub_tree = alpha
                buffer += get_str_knuth_tree(subn, sub_guess, sub_tree)+', '
    return buffer

def print_result(n, guess, knuthTree):
    buffer = get_str_knuth_tree(n, guess, knuthTree)

    with open("result.txt", "w") as f:
        f.write(buffer)

    return

if __name__ == "__main__":
    color = '123456'
    codes = list(itertools.product(color, repeat=4))

    guess = ['1', '1', '2', '2']

    (n, guess, knuthTree), _ = knuth(codes, codes, guess)
    print(n, guess, knuthTree)
    print_result(n, guess, knuthTree)