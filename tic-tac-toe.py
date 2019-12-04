import sys
import random
import time
from copy import deepcopy

board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
columns = ["1", "2", "3"]
rows = ["A", "B", "C"]

"""Returns a 3-by-3 board."""
def show_board(board):
    print("")
    print("    " + "   ".join(str(column) for column in columns))
    horizontal_line = ""
    for row in range(0, len(rows)):
        print(horizontal_line)
        print(rows[row], end="   ")
        print(" | ".join(str(board[row][column]) for column in range(0, len(columns))))
        horizontal_line = "   -----------"
    print("")


"""Validates user's answer"""
def validate_answer(user_answer):
    while user_answer:
        if user_answer.upper() == "CLOSE":
            sys.exit()
        elif len(user_answer) != 2: 
            user_answer = input("Your answer should have 2 characters. Please try again: ").upper()
            continue
        elif user_answer[0] not in rows or user_answer[1] not in columns:
            user_answer = input("Your coordinates should be between A1 and C3. Please choose a new, correct field: ").upper()
            continue
        break
    return(user_answer)


"""Turns string into coordinates"""
def turn_into_coordinates(user_answer):
    row = rows.index(user_answer[0])
    col = columns.index(user_answer[1])
    return(row,col)


"""Checking if a user can choose this field"""
def is_field_available(a, b):
    if board[a][b] != ".":
        return False
    else:
        return True


"""Asks user for answer"""
def get_move(player):
    move_coordinates = input("What's your move player " + player + "? Please specify coordinates between A1 and C3: ").upper()
    while move_coordinates:
        move_coordinates = validate_answer(move_coordinates)
        move_coordinates = turn_into_coordinates(move_coordinates)
        if is_field_available(*move_coordinates) == True:
            break
        else:
            move_coordinates = input("This spot is already taken. Please choose a different one: ").upper()
            continue
    return(move_coordinates)
    

"""Specifies which user will play next"""
def next_player(player, player_1, player_2):
    if player == player_1:
        return(player_2)
    else:
        return(player_1)


"""changes specified fields into X or 0"""
def mark(board, player, row, col):
    board[row][col] = player
    return(board)


"""makes a list of columns, rows and diagonals in our board"""
def get_current_results(board):
    current_results = []
    for row in rows:
        current_results.append(board[rows.index(row)])
        current_results.append([board[0][rows.index(row)], board[1][rows.index(row)], board[2][rows.index(row)]])
    
    diagonal_1 = [board[0][0], board[1][1], board[2][2]]
    diagonal_2 = [board[0][2], board[1][1], board[2][0]]

    current_results.append(diagonal_1)
    current_results.append(diagonal_2)

    return current_results


"""checks the previous list to find if there is any 3x0 or 3xX there"""
def has_won(board, player):
    current_results = get_current_results(board)
    if [player, player, player] in current_results:
        return True
    else:
        return False


"""after game player decides if they want to play again or exit the game"""
def decide_if_play_again():
    users_decision = input("Type \"play\" if you want to try again. Type \"close\" if you don't want to play any more. ")
    while users_decision:
        if users_decision.upper() == "PLAY":
            tictactoe_game()
        elif users_decision.upper() == "CLOSE":
            sys.exit()
        else:
            users_decision = input("Wrong answer. Try again: ")
            continue


# AI IMPLEMENTATION

"""Defines a list of possible moves"""
def possible_moves(board):
    possible_moves_list = []
    for row in range(len(rows)):
        for col in range(len(columns)):
            if is_field_available(row, col):
                possible_moves_list.append([row, col])
    return(possible_moves_list)
"""nawiasy kwadratowe a okragle!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1"""

"""Defines a next AI's move"""
def get_ai_move(player):
    possible_moves_list = possible_moves(board)
    winning_moves_list = []
    for move in possible_moves_list:
        temporary_board = deepcopy(board)
        mark(temporary_board, player, move[0], move[1])
        if has_won(temporary_board, player) == True:
            winning_moves_list.append([move[0], move[1]])
    
    opponents_winning_moves_list = []
    for move in possible_moves_list:
        temporary_board = deepcopy(board)
        player = next_player(player, "X", "0")
        mark(temporary_board, player, move[0], move[1])
        if has_won(temporary_board, player) == True:
            opponents_winning_moves_list.append([move[0], move[1]])

    center_field = [1, 1]
    corner_fields = [[0, 0], [0, 2], [2, 0], [2, 2]]
    possible_corner_field_moves = []
    for field in range(len(corner_fields)):
        if corner_fields[field] in possible_moves_list:
            possible_corner_field_moves.append(corner_fields[field])


    for moves in possible_moves_list:
        if len(winning_moves_list) > 0:
            move_coordinates = winning_moves_list[0]
            print("winning move")
            break
        elif len(opponents_winning_moves_list) > 0:
            move_coordinates = opponents_winning_moves_list[0]
            print("prevent win")
            break
        elif len(possible_corner_field_moves) > 0:
            move_coordinates = random.choice(possible_corner_field_moves)
            print("corner")
            print(possible_moves_list)
            print(possible_corner_field_moves)
            print(move_coordinates)
            break
        elif center_field in possible_moves_list:
            move_coordinates = center_field
            print("center")
            break
        else:
            move_coordinates = random.choice(possible_moves_list)
            print("random")
            break
    
    time.sleep(1)
    return(move_coordinates)


# TRIGGERING A GAME

"""main function for enabling game with other user"""
def play_game_with_human():
    player = "X"
    number_of_moves = 0
    show_board(board)
    while number_of_moves < 9:
        move_coordinates = get_move(player)
        row = move_coordinates[0]
        col = move_coordinates[1]
        mark(board, player, row, col)
        show_board(board)

        if has_won(board, player) == True:
            print("Player " + player + " has won. Congratulations!")
            break

        player = next_player(player, "X", "0")
        number_of_moves += 1
    else:
        print("It's a tie!")
    
    decide_if_play_again()


"""main function for enabling game with AI"""
def play_game_with_ai():
    player = "X"
    number_of_moves = 0
    show_board(board)

    while number_of_moves < 9:
        if player == "X":
            move_coordinates = get_move(player)
        else:
            move_coordinates = get_ai_move(player)
        
        row = move_coordinates[0]
        col = move_coordinates[1]
        mark(board, player, row, col)
        show_board(board)

        if has_won(board, player) == True:
            print("Player " + player + " has won. Congratulations!")
            break

        player = next_player(player, "X", "0")
        number_of_moves += 1
    else:
        print("It's a tie!")
    decide_if_play_again()


"""clearing board"""
def clear_board():
    global board
    board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
    return(board)


"""main menu of the game"""
def tictactoe_game():
    print("Welcome!")
    print("If you want to play against another person, press 1")
    print("If you want to play with computer, press 2")
    print("If you want to close the game, type \"close\"")
    users_answer = input("")

    while users_answer:
        if users_answer == "1":
            board = clear_board()
            play_game_with_human()
            
        elif users_answer == "2":
            board = clear_board()
            play_game_with_ai()
            
        elif users_answer.upper() == "CLOSE":
            sys.exit()
        else:
            users_answer = input("Wrong answer. Try again: ")
            continue


tictactoe_game()
    

# Na etapie SI przewidującej następny ruch człowieka - przetestować i dopisać resztę













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