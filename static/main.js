const startBtn = document.getElementById("startBtn");
const guessBtn = document.getElementById("guessBtn");
const guessInput = document.getElementById("guessInput");
const status = document.getElementById("status");
const attemptsEl = document.getElementById("attempts");
const historyEl = document.getElementById("history");
const gameArea = document.getElementById("gameArea");

async function startGame() {
  const resp = await fetch("/start", { method: "POST" });
  const data = await resp.json();
  if (data.status === "ok") {
    status.textContent = data.message;
    attemptsEl.textContent = "Attempts: 0";
    historyEl.textContent = "";
    gameArea.classList.remove("hidden");
    guessInput.focus();
  } else {
    status.textContent = "Failed to start game.";
  }
}

async function makeGuess() {
  const guess = guessInput.value;
  if (!guess) return;
  const resp = await fetch("/guess", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ guess })
  });

  const data = await resp.json();
  if (!resp.ok) {
    status.textContent = data.message || "Error";
    return;
  }

  if (data.status === "correct") {
    status.textContent = data.message;
    attemptsEl.textContent = `Attempts: ${data.attempts}`;
    historyEl.textContent += `You guessed ${guess} — correct!\n`;
    gameArea.classList.add("hidden");
  } else {
    status.textContent = data.message;
    attemptsEl.textContent = `Attempts: ${data.attempts}`;
    historyEl.textContent += `Tried ${guess} → ${data.message}\n`;
    guessInput.value = "";
    guessInput.focus();
  }
}

startBtn.addEventListener("click", startGame);
guessBtn.addEventListener("click", makeGuess);
guessInput.addEventListener("keyup", (e) => {
  if (e.key === "Enter") makeGuess();
});
