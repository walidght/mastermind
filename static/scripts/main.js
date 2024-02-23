let color = 0;

const secret_code = generateRandomCode();

const new_guess = [-1, -1, -1, -1];

let guesses_number = 0;

let ended = false;
let won = false;

const all_guesses = [
    [-1, -1, -1, -1],
    [-1, -1, -1, -1],
    [-1, -1, -1, -1],
    [-1, -1, -1, -1],
    [-1, -1, -1, -1],
    [-1, -1, -1, -1],
    [-1, -1, -1, -1],
    [-1, -1, -1, -1],
    [-1, -1, -1, -1],
    [-1, -1, -1, -1],
];
const all_evaluations = [
    [0, 0],
    [0, 0],
    [0, 0],
    [0, 0],
    [0, 0],
    [0, 0],
    [0, 0],
    [0, 0],
    [0, 0],
    [0, 0],
];

function generateRandomCode() {
    const randomArray = [];
    for (let i = 0; i < 4; i++) {
        randomArray.push(Math.floor(Math.random() * 6));
    }
    return randomArray;
}

const guess_template = (
    black,
    white,
    first = 'gray',
    second = 'gray',
    third = 'gray',
    forth = 'gray'
) => {
    console.log(first, second, third);
    // Create div elements
    const guessDiv = document.createElement('div');
    guessDiv.classList.add('guess');
    const codeRepresentationDiv = document.createElement('div');
    codeRepresentationDiv.classList.add('code-representation');

    // Create circle elements
    const circles = [first, second, third, forth].map((color) => {
        const circleDiv = document.createElement('div');
        circleDiv.classList.add('circle', color);
        return circleDiv;
    });

    // Append circles to codeRepresentationDiv
    circles.forEach((circle) => {
        codeRepresentationDiv.appendChild(circle);
    });

    // Create evaluation element
    const evaluationDiv = document.createElement('div');
    evaluationDiv.classList.add('evaluation');

    for (let i = 0; i < 4; i++) {
        let eval_col = 'gray';
        const smallCircleDiv = document.createElement('div');
        if (black > 0) {
            eval_col = 'black';
            black -= 1;
        } else if (white > 0) {
            eval_col = 'white';
            white -= 1;
        }
        smallCircleDiv.classList.add('small-circle', eval_col);
        evaluationDiv.appendChild(smallCircleDiv);
    }

    // Append codeRepresentationDiv and evaluationDiv to guessDiv
    guessDiv.appendChild(codeRepresentationDiv);
    guessDiv.appendChild(evaluationDiv);

    return guessDiv;
};

const update_all_guesses = () => {
    guesses_container = document.querySelector('.guesses');
    console.log('aftetr clearging');
    guesses_container.innerHTML = '';
    console.log('aftetr clearging');

    for (let i = 0; i < 10; i++) {
        if (i < guesses_number) {
            console.log('if');
            guesses_container.appendChild(
                guess_template(
                    all_evaluations[i][0],
                    all_evaluations[i][1],
                    get_color_from_int(all_guesses[i][0]),
                    get_color_from_int(all_guesses[i][1]),
                    get_color_from_int(all_guesses[i][2]),
                    get_color_from_int(all_guesses[i][3])
                )
            );
        } else {
            console.log('else');
            guesses_container.appendChild(
                guess_template(all_evaluations[i][0], all_evaluations[i][1])
            );
        }
    }
};

const get_color_from_int = (color) => {
    if (color == 0) return 'green';
    if (color == 1) return 'yellow';
    if (color == 2) return 'blue';
    if (color == 3) return 'red';
    if (color == 4) return 'black';
    if (color == 5) return 'white';
};

const get_int_from_color = (color) => {
    if (color == 'green') return 0;
    if (color == 'yellow') return 1;
    if (color == 'blue') return 2;
    if (color == 'red') return 3;
    if (color == 'black') return 4;
    if (color == 'white') return 5;
};

const change_selected_color = (c) => {
    document
        .querySelector('.buttons')
        .querySelector(`.color-button.${get_color_from_int(color)}`)
        .classList.remove('selected-color');
    color = get_int_from_color(c);
    document
        .querySelector('.buttons')
        .querySelector(`.${c}`)
        .classList.add('selected-color');
};

document.querySelectorAll('.color-button').forEach((e) =>
    e.addEventListener('click', (e) => {
        const new_color = e.target.dataset.color;
        change_selected_color(new_color);
    })
);

const empty_buttons = document.querySelectorAll('.empty');

empty_buttons.forEach((e, i) =>
    e.addEventListener('click', (e) => {
        // add color
        if (new_guess[i] == -1) {
            empty_buttons[i].classList.add(get_color_from_int(color));
            new_guess[i] = color;
        } else {
            // already has color, clear old then add new
            empty_buttons[i].classList.remove(get_color_from_int(new_guess[i]));
            empty_buttons[i].classList.add(get_color_from_int(color));
            new_guess[i] = color;
        }
    })
);

document.querySelector('.guess-button').addEventListener('click', (e) => {
    if (won) {
        alert('You already won');
        return;
    }
    if (new_guess.includes(-1)) {
        alert('Please select a valid guess');
        return;
    }
    if (guesses_number == 10) {
        alert('Max guesses reached (Alreay made 10 guesses)');
        ended = true;
        show_secret_code();
        return;
    }
    all_guesses[guesses_number][0] = new_guess[0];
    all_guesses[guesses_number][1] = new_guess[1];
    all_guesses[guesses_number][2] = new_guess[2];
    all_guesses[guesses_number][3] = new_guess[3];

    all_evaluations[guesses_number] = evaluate(new_guess, secret_code);

    guesses_number += 1;

    empty_buttons.forEach((e, i) => {
        empty_buttons[i].classList.remove(get_color_from_int(new_guess[i]));
        new_guess[i] = -1;
    });

    update_all_guesses();
});

update_all_guesses();

const evaluate = (guess, answer) => {
    let blackCount = 0;
    let whiteCount = 0;
    let unmatchedGuessPegs = [];
    let unmatchedAnswerPegs = [];

    // Count black pegs
    for (let i = 0; i < guess.length; i++) {
        if (guess[i] === answer[i]) {
            blackCount++;
        } else {
            unmatchedGuessPegs.push(guess[i]);
            unmatchedAnswerPegs.push(answer[i]);
        }
    }

    // Count white pegs
    for (let peg of unmatchedGuessPegs) {
        let index = unmatchedAnswerPegs.indexOf(peg);
        if (index !== -1) {
            unmatchedAnswerPegs.splice(index, 1);
            whiteCount++;
        }
    }

    if (blackCount == 4) {
        won = true;
        ended = true;
        show_secret_code();
        alert('You won!');
    }

    return [blackCount, whiteCount];
};

const show_secret_code = () => {
    const codeRepresentationDiv = document.querySelector('.secret-code');
    codeRepresentationDiv.innerHTML = '';
    secret_code.forEach((color) => {
        const circleDiv = document.createElement('div');
        circleDiv.classList.add('circle', get_color_from_int(color));
        codeRepresentationDiv.appendChild(circleDiv);
    });
};

document.querySelector('.show-code-button').addEventListener('click', (e) => {
    show_secret_code();
});
