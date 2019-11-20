board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
columns = ["1", "2", "3"]
rows = ["A", "B", "C"]

"""Returns a 3-by-3 board."""
def show_board():
    print("")
    print("    " + "   ".join(str(column) for column in columns))
    horizontal_line = ""
    for row in range(0, len(rows)):
        print(horizontal_line)
        print(rows[row], end="   ")
        print(" | ".join(str(board[row][column]) for column in range(0, len(columns))))
        horizontal_line = "   -----------"
    print("")


def get_move():
    move_coordinates = input("What's your move? Please specify coordinates between A1 and C3: ").upper()
   
    def validate_coordinates(user_coordinates):
        if len(user_coordinates) != 2: 
            user_coordinates = input("Your answer should have 2 characters. Please try again:").upper()
            validate_coordinates(user_coordinates)
        elif user_coordinates[0] not in rows or user_coordinates[1] not in columns:
            user_coordinates = input("Your coordinates should be between A1 and C3. Please choose a new, correct field:").upper()
            validate_coordinates(user_coordinates)
        
        return(user_coordinates)
    
    move_coordinates = validate_coordinates(move_coordinates)
    print(move_coordinates)



show_board()
get_move()










# def get_move(board, player):
#     """Returns the coordinates of a valid move for player on board."""
#     row, col = 0, 0
#     return row, col


# def get_ai_move(board, player):
#     """Returns the coordinates of a valid move for player on board."""
#     row, col = 0, 0
#     return row, col


# def mark(board, player, row, col):
#     """Marks the element at row & col on the board for player."""
#     pass


# def has_won(board, player):
#     """Returns True if player has won the game."""
#     return False


# def is_full(board):
#     """Returns True if board is full."""
#     return False


# def print_board(board):
#     """Prints a 3-by-3 board on the screen with borders."""
#     pass


# def print_result(winner):
#     """Congratulates winner or proclaims tie (if winner equals zero)."""
#     pass


# def tictactoe_game(mode='HUMAN-HUMAN'):
#     board = init_board()

#     # use get_move(), mark(), has_won(), is_full(), and print_board() to create game logic
#     print_board(board)
#     row, col = get_move(board, 1)
#     mark(board, 1, row, col)

#     winner = 0
#     print_result(winner)


# def main_menu():
#     tictactoe_game('HUMAN-HUMAN')


# if __name__ == '__main__':
#     main_menu()