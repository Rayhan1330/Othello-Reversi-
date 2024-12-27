import numpy as np

def create_board():
    board = np.full((8, 8), ' ')
    board[3:5, 3:5] = [['O', 'X'], ['X', 'O']]
    return board

def print_board(board):
    print("   0   1   2   3   4   5   6   7")
    print(" +---+---+---+---+---+---+---+---+")
    for i, row in enumerate(board):
        print(f"{i}|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print("\n +---+---+---+---+---+---+---+---+")

def is_valid_move(board, row, col, player):
    if board[row, col] != ' ':
        return False

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        temp = []
        while 0 <= r < 8 and 0 <= c < 8:
            if board[r, c] == ' ':
                break
            if board[r, c] == player:
                return True
            temp.append((r, c))
            r, c = r + dr, c + dc

    return False

def make_move(board, row, col, player):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    board[row, col] = player

    for dr, dc in directions:
        r, c = row + dr, col + dc
        temp = []
        while 0 <= r < 8 and 0 <= c < 8:
            if board[r, c] == ' ':
                break
            if board[r, c] == player:
                for tr, tc in temp:
                    board[tr, tc] = player
                break
            temp.append((r, c))
            r, c = r + dr, c + dc

def count_discs(board, player):
    return np.sum(board == player)

def switch_player(player):
    return 'X' if player == 'O' else 'O'

def get_user_move():
    while True:
        try:
            move = input("Enter your move (row col): ").split()
            row, col = map(int, move)
            if 0 <= row < 8 and 0 <= col < 8:
                return row, col
            else:
                print("Invalid move. Please enter valid row and column values.")
        except ValueError:
            print("Invalid input. Please enter two integers separated by a space.")

def get_cpu_move(board, player):
    best_score = -float('inf')
    best_move = None

    for i in range(8):
        for j in range(8):
            if board[i, j] == ' ' and is_valid_move(board, i, j, player):
                board_copy = np.copy(board)
                make_move(board_copy, i, j, player)
                score = minimax(board_copy, 0, False, -float('inf'), float('inf'), switch_player(player))
                
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    return best_move

def minimax(board, depth, maximizing_player, alpha, beta, player):
    scores = {'X': count_discs(board, 'X'), 'O': count_discs(board, 'O')}

    result = game_over(board)
    if result:
        return scores[result]

    if depth == 5:  # Adjust the depth of the search based on performance
        return scores[player]

    if maximizing_player:
        max_eval = -float('inf')
        for i in range(8):
            for j in range(8):
                if board[i, j] == ' ' and is_valid_move(board, i, j, player):
                    board[i, j] = player
                    eval = minimax(board, depth + 1, False, alpha, beta, switch_player(player))
                    board[i, j] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break

        return max_eval

    else:
        min_eval = float('inf')
        for i in range(8):
            for j in range(8):
                if board[i, j] == ' ' and is_valid_move(board, i, j, player):
                    board[i, j] = player
                    eval = minimax(board, depth + 1, True, alpha, beta, switch_player(player))
                    board[i, j] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break

        return min_eval

def game_over(board):
    x_count = count_discs(board, 'X')
    o_count = count_discs(board, 'O')

    if x_count + o_count == 64:
        if x_count > o_count:
            return 'X'
        elif o_count > x_count:
            return 'O'
        else:
            return 'Draw'
    else:
        return None

def main():
    board = create_board()
    player = 'X'

    while True:
        print_board(board)
        print(f"\nCurrent Score - X: {count_discs(board, 'X')} | O: {count_discs(board, 'O')}\n")

        if np.count_nonzero(board == ' ') == 0:
            print("The game is a draw!")
            break

        if np.count_nonzero(board == player) == 0:
            print(f"No valid moves for {player}. Switching to the other player.")
            player = switch_player(player)
            continue

        print(f"It's {player}'s turn.")

        if player == 'X':
            row, col = get_user_move()
        else:
            print("CPU is thinking...")
            row, col = get_cpu_move(board, player)

        if is_valid_move(board, row, col, player):
            make_move(board, row, col, player)
            player = switch_player(player)
        else:
            print("Invalid move. Try again.")

        winner = game_over(board)
        if winner:
            print(f"\nThe game is over! Winner: {winner}")
            break

if __name__ == "__main__":
    main()
