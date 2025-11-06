import random

board = [" "] * 9

# Symbols will be assigned at runtime based on who goes first
AI_SYMBOL = "O"
HUMAN_SYMBOL = "X"


def print_board(current_board):
    for r in range(3):
        row = current_board[3 * r : 3 * r + 3]
        print("|".join(row))
        if r < 2:
            print("-----")


def make_move(board, position, symbol):
    # If the chosen cell is empty, place the symbol there
    if board[position] == " ":
        board[position] = symbol
        return True
    else:
        return False


def human_move(board, symbol):
    while True:
        try:
            move = int(input(f"Enter your move (0-8): "))
            if move < 0 or move > 8:
                print("Invalid move. Please enter a number between 0 and 8.")
                continue
            if make_move(board, move, symbol):
                break
            else:
                print("Cell already taken. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 8.")


def check_winner(board):
    win_positions = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),  # rows
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),  # columns
        (0, 4, 8),
        (2, 4, 6),  # diagonals
    ]
    for a, b, c in win_positions:
        # Check if all three are same symbol and not blank
        if board[a] == board[b] == board[c] != " ":
            return board[a]  # return 'X' or 'O'
    if " " not in board:
        return "Draw"
    return None


def computer_move(board, symbol):
    available = [i for i, cell in enumerate(board) if cell == " "]
    move = best_move(board, symbol)
    make_move(board, symbol)
    print(f"Computer placed {symbol} at position {move}")
    print_board(board)


def choose_first_player():
    while True:
        choice = input("Who goes first? (human/ai): ").strip().lower()
        if choice in ("human", "ai"):
            return choice
        print("Please type 'human' or 'ai'.")


def main():
    global AI_SYMBOL, HUMAN_SYMBOL
    # Reset board for a fresh game
    for i in range(9):
        board[i] = " "
    first = choose_first_player()
    if first == "human":
        HUMAN_SYMBOL, AI_SYMBOL = "X", "O"
        current = "human"
    else:
        AI_SYMBOL, HUMAN_SYMBOL = "X", "O"
        current = "ai"
    print("Symbols assigned:")
    print(f"  Human: {HUMAN_SYMBOL}")
    print(f"  AI:    {AI_SYMBOL}")
    print_board(board)
    while True:
        if current == "human":
            human_move(board, HUMAN_SYMBOL)
        else:
            computer_move(board, AI_SYMBOL)
        winner = check_winner(board)
        if winner is not None:
            if winner == "Draw":
                print("It's a draw!")
            else:
                print(f"{winner} wins!")
            break
        current = "ai" if current == "human" else "human"


def evaluate(board, ai_symbol):
    """Evaluate the board and return a score from the AI's perspective."""
    winner = check_winner(board)  # check_winner needs the board to work
    human_symbol = "O" if ai_symbol == "X" else "X"
    if winner == ai_symbol:
        return 1  # AI wins
    elif winner == human_symbol:
        return -1  # Human wins
    elif winner == "Draw":
        return 0  # Draw
    # Non-terminal state (placeholder until Minimax integration)
    return 0


def minimax(board, depth, is_maximizing, ai_symbol):
    human_symbol = "O" if ai_symbol == "X" else "X"
    winner = check_winner(board)
    if winner is not None:
        if winner == ai_symbol:
            return 10 - depth
        if winner == human_symbol:
            return depth - 10
        return 0  # Draw

    if is_maximizing:
        best_score = float("-inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = ai_symbol
                value = minimax(board, depth + 1, False, ai_symbol)
                board[i] = " "
                best_score = max(best_score, value)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = human_symbol
                value = minimax(board, depth + 1, True, ai_symbol)
                board[i] = " "
                best_score = min(best_score, value)
        return best_score

def best_move(board, ai_symbol):
    best_score = float("-inf")
    move_index = None
    for i in range(9):
        if board[i] == " ":
            board[i] = ai_symbol
            score = minimax(board, 0, False, ai_symbol)
            board[i] = " "
            if score > best_score:
                best_score = score
                move_index = i
    if move_index is None:
        for i in range(9):
            if board[i] == " ":
                return i
    return move_index