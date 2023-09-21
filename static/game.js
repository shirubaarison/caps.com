// Créditos ao "Bro Code" https://www.youtube.com/watch?v=AnmwHjpEhtA

const cells = document.querySelectorAll(".cell");
const statusText = document.querySelector("#statusText");
const restartBtn = document.querySelector("#restartBtn");
const nomeJogador = document.querySelector("#nomeJogador").innerHTML;
const user = document.querySelector("#player1");

let whoWon = "";
let running = false;

const winConditions = 
[
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
];

let options = ["", "", "", "", "", "", "", "", ""];
let currentPlayer = "X";

let ai = "O";
let human = "X";

let scores = {
    "X": -10,
    "O": 10,
    "tie": 0
};

initializeGame();

function initializeGame()
{
    cells.forEach(cell => cell.addEventListener("click", cellClicked));
    restartBtn.addEventListener("click", restartGame);
    statusText.textContent = `Vez de ${currentPlayer}`;
    running = true;
}

function cellClicked()
{
    const cellIndex = this.getAttribute("cellIndex");

    if(options[cellIndex] != "" || !running)
    {
        return;
    }

    updateCell(this, cellIndex);
    checkWinner();
}

function updateCell(cell, index)
{
    options[index] = currentPlayer;
    cell.textContent = currentPlayer;
}

function changePlayer()
{
    currentPlayer = (currentPlayer == "X") ? "O" : "X";
    statusText.textContent = `Vez de ${currentPlayer}`;
    if (currentPlayer == "O")
    {
        running = false;
        statusText.textContent = `${nomeJogador} está pensando...`;
        setTimeout(() => {
            makeMove();
            running = true;
        }, 1000);
    } 
}

function checkWinner()
{
    let roundWon = false;
    for(let i = 0; i < winConditions.length; i++){
        const condition = winConditions[i];
        const cellA = options[condition[0]];
        const cellB = options[condition[1]];
        const cellC = options[condition[2]];

        if(cellA == "" || cellB == "" || cellC == "")
        {
            continue;
        }
        if(cellA == cellB && cellB == cellC)
        {
            roundWon = true;
            whoWon = cellA;
            break;
        }
    }

    if (roundWon)
    {
        running = false;
        statusText.textContent = `${whoWon} ganhou`;
        setTimeout(() => {
            restartGame();
            sendData();
        }, 1000);
    }
    else if(!options.includes(""))
    {
        statusText.textContent = `Empate!`;
        running = false;
        setTimeout(() => {
            restartGame();
        }, 1000);
    }
    else
    {
        changePlayer();
    }
}

function minimaxCheckWinner(board)
{
    let winner = null;

    for(let i = 0; i < winConditions.length; i++){
        const condition = winConditions[i];
        const cellA = board[condition[0]];
        const cellB = board[condition[1]];
        const cellC = board[condition[2]];

        if(cellA == "" || cellB == "" || cellC == "")
        {
            continue;
        }
        if(cellA == cellB && cellB == cellC)
        {
            winner = cellA;           
            break;
        }
    }
    if(whoWon == null && !board.includes(""))
    {
        return "tie";
    }
    else
    {
        return winner;
    }
}

function restartGame()
{
    options = ["", "", "", "", "", "", "", "", ""];
    statusText.textContent = `Vez de ${currentPlayer}`;
    cells.forEach(cell => cell.textContent = "");
    running = true;
    changePlayer();
}

function makeMove()
{   
    // "AI" escolhe a jogada
    let move;

    let bestScore = -Infinity;
    for (let i = 0; i < options.length; i++) 
    {   
        if (options[i] == "")
        {
            // Necessario para gerar o score do minimax
            options[i] = ai;
            // Verificar as possibilidades da IA...
            let score = minimax(options, 0, false)
            // Desfazer a modificação
            options[i] = '';
            if (score > bestScore)
            {
                bestScore = score;
                move = i;
            }
        }
    }
    updateCell(cells[move], move);
    checkWinner();
}

function minimax(board, depth, isMaximizing)
{
    // Verificar o ganhador
    let result = minimaxCheckWinner(board);

    // Se não for um "estado final"
    if (result != null)
    {
        return scores[result] / depth;
    }

    // Se é a IA ou Jogador
    if (isMaximizing)
    {
        let bestScore = -Infinity;
        for (let i = 0; i < board.length; i++) 
        {   
            if (board[i] == "")
            {
                board[i] = ai;
                let score = minimax(board, depth + 1, false);
                board[i] = '';
                
                bestScore = Math.max(score, bestScore);
            }
        }
        return bestScore;
    }
    else
    {
        let bestScore = Infinity;
        for (let i = 0; i < board.length; i++) 
        {   
            if (board[i] == "")
            {
                board[i] = human;
                let score = minimax(board, depth + 1, true);
                board[i] = '';
                
                bestScore = Math.min(score, bestScore);
            }
        }
        return bestScore;
    }
}


// Serve para se comunicar com o back-end
function sendData() 
{
    let vitorias1 = parseInt(document.querySelector("#vitorias1").innerHTML);
    let vitorias2 = parseInt(document.querySelector("#vitorias2").innerHTML);

    if (whoWon == "X")
    {
        vitorias1++;
    }
    else if (whoWon == "O")
    {
        vitorias2++;
    }    
    $.ajax(
        {
        url: '/jogar',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ 'whoOn': whoWon, 'vitorias1': vitorias1, "adversario": nomeJogador, "vitorias2": vitorias2 }),
        success: function(response) {
            console.log(response.result);
            if (whoWon == "X") {document.getElementById('vitorias1').innerHTML = vitorias1}
            else if (whoWon == "O"){document.getElementById('vitorias2').innerHTML = vitorias2;}
        },
        error: function(error) {
            console.log(error);
        }
    });
}