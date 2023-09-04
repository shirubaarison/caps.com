// Créditos ao "Bro Code" https://www.youtube.com/watch?v=AnmwHjpEhtA

const cells = document.querySelectorAll(".cell");
const statusText = document.querySelector("#statusText");
const restartBtn = document.querySelector("#restartBtn");
const nomeJogador = document.querySelector("#nomeJogador").innerHTML;
const user = document.querySelector("#player1");

let whoWon = "";

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
let running = false;

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
            botPlay();
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
            break;
        }
    }

    if (roundWon)
    {
        running = false;
        statusText.textContent = `${currentPlayer} ganhou`;
        whoWon = `${currentPlayer}`;
        setTimeout(() => {
            restartGame();
            sendData();
        }, 1000);
    }
    else if(!options.includes(""))
    {
        statusText.textContent = `Empate!`;
        running = false;
        restartGame();
    }
    else
    {
        changePlayer();
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
    // Por enquanto está aleatória
    let move;
    
    for (let i = 0; i < options.length; i++) 
    {
        let randomMove = Math.floor(Math.random() * options.length);
        
        // Tirar alguns casos
        if(options[i] == "")
        {
            move = i;
        }
        else if (options[randomMove] == "")
        {
            move = randomMove;
        }
      }
  
    return move;
}

function botPlay()
{
    const cells = document.getElementsByClassName("cell");
    const move = makeMove();

    //console.log(move);
    //console.log(cells[move]);
    
    updateCell(cells[move], move);
    checkWinner();
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

    console.log(vitorias1);
    console.log(vitorias2);
    
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