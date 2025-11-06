import random

board = [' '] * 9

def print_board(current_board):
    for r in range(3):
        row = current_board[3*r:3*r+3]
        print('|'.join(row))
        if r < 2:
            print('-----')

def make_move(board, position, symbol):
    # If the chosen cell is empty, place the symbol there
    if board[position] == ' ':
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
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6)              # diagonals
    ]
    for a, b, c in win_positions:
        # Check if all three are same symbol and not blank
        if board[a] == board[b] == board[c] != ' ':
            return board[a]  # return 'X' or 'O'
    if ' ' not in board:
        return 'Draw'
    return None

def computer_move(board, symbol):
    available = [i for i, cell in enumerate(board) if cell == ' ']
    move = random.choice(available)
    make_move(board,move,symbol)
    print(f"Computer placed {symbol} at position {move}")
    print_board(board)

