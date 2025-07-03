import math

HUMAN_PLAYER = 'O'
AI_PLAYER = 'X'
EMPTY_CELL = ' '

game_board = [EMPTY_CELL] * 9

def display_board(board):
    for row in range(3):
        row_cells = [board[row * 3 + col] for col in range(3)]
        print(" | ".join(row_cells))
        if row < 2:
            print("--+---+--")

def check_winner(board, player_symbol):
    winning_combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]
    for combination in winning_combinations:
        if all(board[index] == player_symbol for index in combination):
            return True
    return False

def board_is_full(board):
    return all(cell != EMPTY_CELL for cell in board)

def get_empty_positions(board):
    return [index for index, cell in enumerate(board) if cell == EMPTY_CELL]

def minimax(board, is_ai_turn, alpha, beta):
    if check_winner(board, AI_PLAYER):
        return 1
    if check_winner(board, HUMAN_PLAYER):
        return -1
    if board_is_full(board):
        return 0

    if is_ai_turn:
        max_score = -math.inf
        for position in get_empty_positions(board):
            board[position] = AI_PLAYER
            score = minimax(board, False, alpha, beta)
            board[position] = EMPTY_CELL
            max_score = max(max_score, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return max_score
    else:
        min_score = math.inf
        for position in get_empty_positions(board):
            board[position] = HUMAN_PLAYER
            score = minimax(board, True, alpha, beta)
            board[position] = EMPTY_CELL
            min_score = min(min_score, score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return min_score

def ai_make_move():
    best_score = -math.inf
    best_position = None
    for position in get_empty_positions(game_board):
        game_board[position] = AI_PLAYER
        move_score = minimax(game_board, False, -math.inf, math.inf)
        game_board[position] = EMPTY_CELL
        if move_score > best_score:
            best_score = move_score
            best_position = position
    game_board[best_position] = AI_PLAYER
    print(f"\nAI chooses position {best_position}.\n")

def play_game():
    print("Welcome to Tic-Tac-Toe!")
    print("You are O, the AI is X.")
    print("Positions are numbered 0 to 8 as follows:")
    print("0 | 1 | 2")
    print("--+---+--")
    print("3 | 4 | 5")
    print("--+---+--")
    print("6 | 7 | 8\n")

    display_board(game_board)

    while True:
        user_input = input("\nEnter your move (0-8): ")
        try:
            move = int(user_input)
        except ValueError:
            print("Invalid input. Please enter a number from 0 to 8.")
            continue

        if move < 0 or move > 8 or game_board[move] != EMPTY_CELL:
            print("Invalid move. Try again.")
            continue

        game_board[move] = HUMAN_PLAYER
        display_board(game_board)

        if check_winner(game_board, HUMAN_PLAYER):
            print("\nCongratulations! You win!")
            break

        if board_is_full(game_board):
            print("\nIt's a draw!")
            break

        ai_make_move()
        display_board(game_board)

        if check_winner(game_board, AI_PLAYER):
            print("\nAI wins! Better luck next time.")
            break

        if board_is_full(game_board):
            print("\nIt's a draw!")
            break

if __name__ == "__main__":
    play_game()
