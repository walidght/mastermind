import numpy as np
import itertools

def knuth(codes, candidates, guess):
    nb_candidates, list_candidates = calcul_candidate(candidates, guess)
    knuthTree = [None]*15

    # pour chaque alpha(i, j)
    for i, nb_candidate in enumerate(nb_candidates):
        # s'il a plus que 2 codes possibles
        if nb_candidate > 2:
            val_remaining, count_remaining = [np.inf], [0]
            code_keep = None
            # pour chque code possible
            for code in codes:
                new_nb_candidates, _ = calcul_candidate(list_candidates[i], list(code))
                # si c'est bien la réponse
                if new_nb_candidates == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]:
                    knuthTree[i] = (nb_candidate, code)
                    break
                # sinon on prend celui qui minimise le plus grand nombre de candidat
                else:
                    val, count = np.unique(new_nb_candidates, return_counts=True)
                    sort_index = np.argsort(val)[::-1]
                    val = val[sort_index]
                    count = count[sort_index]
                    for j in range(len(val_remaining)):
                        # si le plus grand nombre de candidat possible est plus petit que le meilleur stoqué
                        if val[j] < val_remaining[j]:
                            val_remaining, count_remaining = val, count
                            code_keep = list(code)
                            break
                        # s'ils ont le plus grand nombre de candidat possible est le même, on compare l'occurance
                        elif val[j] == val_remaining[j]:
                            # s'il a un plus petit nombre d'occurance, on le prend
                            if count[j] < count_remaining[j]:
                                val_remaining, count_remaining, val, count
                                code_keep = list(code)
                                break
                            # sinon on le prend pas
                            else:
                                break
                        # sinon on le prend pas
                        else:
                            break
            if knuthTree[i] == None:
                knuthTree[i] = (knuth(codes, list_candidates[i], code_keep))
        # sinon c'est fini pour cette branche
        else:
            knuthTree[i] = nb_candidate

    return (sum(nb_candidates), guess, knuthTree)

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

if __name__ == "__main__":
    color = '123456'
    codes = list(itertools.product(color, repeat=4))

    guess = ['1', '1', '2', '2']

    n, guess, knuthTree = knuth(codes, codes, guess)
    for alpha in knuthTree:
        print(alpha)
        print()