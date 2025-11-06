(() => {
  const gridEl = document.getElementById('grid');
  const statusEl = document.getElementById('status');
  const newGameBtn = document.getElementById('newGame');
  const humanSymbolSelect = document.getElementById('humanSymbol');

  let board = Array(9).fill(' ');
  let gameOver = false;
  let humanSymbol = humanSymbolSelect.value;
  let aiSymbol = humanSymbol === 'X' ? 'O' : 'X';

  // ---------------------------
  // Render board
  // ---------------------------
  function render() {
    gridEl.innerHTML = '';
    board.forEach((cell, idx) => {
      const div = document.createElement('div');
      div.className = 'cell' + (cell !== ' ' ? ' filled' : '');
      div.textContent = cell === ' ' ? '' : cell;
      div.setAttribute('role', 'gridcell');
      div.setAttribute('aria-label', `Cell ${idx}`);
      if (!gameOver && cell === ' ') {
        div.addEventListener('click', () => handlePlayerMove(idx));
      } else {
        div.classList.add('disabled');
      }
      gridEl.appendChild(div);
    });
  }

  // ---------------------------
  // Set status text
  // ---------------------------
  function setStatus(text, cls) {
    statusEl.className = 'status' + (cls ? ' ' + cls : '');
    statusEl.textContent = text;
  }

  // ---------------------------
  // Start new game (calls /start)
  // ---------------------------
  async function resetBoard() {
    board = Array(9).fill(' ');
    gameOver = false;
    humanSymbol = humanSymbolSelect.value;
    aiSymbol = humanSymbol === 'X' ? 'O' : 'X';
    setStatus('Starting new game…');
  
    try {
      const res = await fetch('/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ aiSymbol })
      });
  
      const data = await res.json();
      board = data.board;
      render();
  
      if (data.aiMove !== null) {
        setStatus(`Your turn (${humanSymbol})`);
      } else {
        setStatus(`Your turn (${humanSymbol})`);
      }
    } catch (err) {
      console.error(err);
      setStatus('Error starting game', 'loss');
    }
  }
  

  // ---------------------------
  // Winner message
  // ---------------------------
  function winnerText(winner) {
    if (winner === 'Draw') return 'Draw!';
    return `${winner} wins!`;
  }

  // ---------------------------
  // Handle human move (calls /move)
  // ---------------------------
  async function handlePlayerMove(index) {
    if (gameOver || board[index] !== ' ') return;
    setStatus('AI thinking…');
    try {
      const res = await fetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ board, position: index, humanSymbol, aiSymbol })
      });
      if (!res.ok) {
        const e = await res.json().catch(() => ({}));
        setStatus(e.error || 'Invalid move', 'loss');
        return;
      }
      const data = await res.json();
      board = data.board;
      render();
      if (data.status === 'ended') {
        gameOver = true;
        const cls = data.winner === 'Draw'
          ? 'draw'
          : data.winner === humanSymbol
          ? 'win'
          : 'loss';
        setStatus(winnerText(data.winner), cls);
      } else {
        setStatus(`Your turn (${humanSymbol})`);
      }
    } catch (err) {
      console.error(err);
      setStatus('Network error', 'loss');
    }
  }

  // ---------------------------
  // Event bindings
  // ---------------------------
  newGameBtn.addEventListener('click', resetBoard);
  humanSymbolSelect.addEventListener('change', resetBoard);

  // ---------------------------
  // Initial game start
  // ---------------------------
  window.addEventListener('load', resetBoard);
})();
