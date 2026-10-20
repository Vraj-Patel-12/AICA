
ROWS = 6
COLS = 7
EMPTY = "."

HUMAN = "X"
AI = "O"

WIN_SCORE = 100000


board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def display():
    print()
    print("  0 1 2 3 4 5 6")

    for row in board:
        print("| " + " ".join(row) + " |")

    print("-----------------")
    print()


def drop_piece(col, piece):
    """Place a piece in the lowest available row."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            board[row][col] = piece
            return row

    return -1


def undo_move(row, col):
    """Undo the exact move that was simulated."""
    board[row][col] = EMPTY


def check_win(piece):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    # Vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    # Diagonal: down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    # Diagonal: up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    return False


def is_draw():
    """A draw occurs when the top row is completely occupied."""
    return all(board[0][c] != EMPTY for c in range(COLS))


def score_board():
    """Evaluate terminal game positions."""
    if check_win(AI):
        return WIN_SCORE

    if check_win(HUMAN):
        return -WIN_SCORE

    return 0


def minimax(depth, maximizing, alpha, beta):
    """
    Minimax with alpha-beta pruning.

    AI maximizes the score.
    Human minimizes the score.
    """

    score = score_board()

    # Terminal position
    if score == WIN_SCORE:
        return score + depth

    if score == -WIN_SCORE:
        return score - depth

    if is_draw():
        return 0

    if depth == 0:
        return 0

    if maximizing:
        best_score = -float("inf")

        for col in range(COLS):
            if board[0][col] != EMPTY:
                continue

            row = drop_piece(col, AI)

            value = minimax(depth - 1, False, alpha, beta)

            undo_move(row, col)

            best_score = max(best_score, value)
            alpha = max(alpha, best_score)

            # Alpha-beta pruning
            if alpha >= beta:
                break

        return best_score

    else:
        best_score = float("inf")

        for col in range(COLS):
            if board[0][col] != EMPTY:
                continue

            row = drop_piece(col, HUMAN)

            value = minimax(depth - 1, True, alpha, beta)

            undo_move(row, col)

            best_score = min(best_score, value)
            beta = min(beta, best_score)

            # Alpha-beta pruning
            if alpha >= beta:
                break

        return best_score


def ai_move():
    """Choose the best column for the AI."""
    best_score = -float("inf")
    best_col = None

    # Prefer the center column when scores are equal.
    column_order = [3, 2, 4, 1, 5, 0, 6]

    for col in column_order:
        if board[0][col] != EMPTY:
            continue

        row = drop_piece(col, AI)

        score = minimax(
            depth=4,
            maximizing=False,
            alpha=-float("inf"),
            beta=float("inf")
        )

        undo_move(row, col)

        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def play():
    print("CONNECT FOUR AI")
    print("You = X | Computer = O")
    print("Connect four pieces horizontally, vertically, or diagonally!")

    while True:
        display()

        # Human move
        try:
            col = int(input("Enter column (0-6): "))
        except ValueError:
            print("Please enter a valid integer.")
            continue

        if col < 0 or col >= COLS:
            print("Invalid column. Choose between 0 and 6.")
            continue

        row = drop_piece(col, HUMAN)

        if row == -1:
            print("That column is full. Try another.")
            continue

        if check_win(HUMAN):
            display()
            print("Congratulations! You win!")
            break

        if is_draw():
            display()
            print("The game is a draw!")
            break

        # AI move
        col = ai_move()

        if col is None:
            display()
            print("The game is a draw!")
            break

        drop_piece(col, AI)

        print("Computer chose column:", col)

        if check_win(AI):
            display()
            print("Computer wins!")
            break

        if is_draw():
            display()
            print("The game is a draw!")
            break


if __name__ == "__main__":
    play()

