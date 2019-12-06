import sys
import random
import time
from copy import deepcopy

board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
columns = ["1", "2", "3"]
rows = ["A", "B", "C"]


def print_board(board):
    print("")
    print("    " + "   ".join(str(column) for column in columns))
    horizontal_line = ""
    for row in range(len(rows)):
        print(horizontal_line)
        print(rows[row], end="   ")
        print(" | ".join(str(board[row][column]) for column in range(len(columns))))
        horizontal_line = "   -----------"
    print("")


def validate_user_answer(user_answer):
    valid_answer_length = 2
    while user_answer:
        if user_answer.upper() == "CLOSE":
            sys.exit()
        elif len(user_answer) != valid_answer_length: 
            user_answer = input("Your answer should have 2 characters. Please try again: ").upper()
        elif user_answer[0] not in rows or user_answer[1] not in columns:
            user_answer = input("Your coordinates should be between A1 and C3. Please choose a new, correct field: ").upper()
        else:
            return(user_answer)


def turn_answer_into_coordinates(user_answer):
    row = rows.index(user_answer[0])
    col = columns.index(user_answer[1])
    return(row,col)


def is_field_available(a, b):
    if board[a][b] == ".":
        return True
    else:
        return False


def get_move_from(player):
    move_coordinates = input("What's your move player " + player + "? Please specify coordinates between A1 and C3: ").upper()
    while move_coordinates:
        move_coordinates = validate_user_answer(move_coordinates)
        move_coordinates = turn_answer_into_coordinates(move_coordinates)
        if is_field_available(*move_coordinates) == True:
            break
        else:
            move_coordinates = input("This spot is already taken. Please choose a different one: ").upper()
            continue
    return(move_coordinates)
    

def next_player(player, player_1, player_2):
    if player == player_1:
        return(player_2)
    else:
        return(player_1)


def mark(board, player, row, col):
    board[row][col] = player
    return(board)


def list_all_current_results_from(board):
    current_results = []
    for row in rows:
        current_results.append(board[rows.index(row)])
        current_results.append([board[0][rows.index(row)], board[1][rows.index(row)], board[2][rows.index(row)]])
    
    diagonal_1 = [board[0][0], board[1][1], board[2][2]]
    diagonal_2 = [board[0][2], board[1][1], board[2][0]]

    current_results.append(diagonal_1)
    current_results.append(diagonal_2)

    return current_results


def has_won(board, player):
    current_results = list_all_current_results_from(board)
    if [player, player, player] in current_results:
        return True
    else:
        return False


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

def specify_possible_moves_list():
    possible_moves_list = []
    for row in range(len(rows)):
        for col in range(len(columns)):
            if is_field_available(row, col):
                possible_moves_list.append([row, col])
    return(possible_moves_list)


def specify_winning_moves_list(board, temporary_board, player):
    winning_moves_list = []
    for row in range(len(rows)):
        for col in range(len(columns)):
            if is_field_available(row, col):
                mark(temporary_board, player, row, col)
                if has_won(temporary_board, player):
                    winning_moves_list.append([row, col])
                temporary_board = deepcopy(board)
    temporary_board = deepcopy(board)
    return winning_moves_list, temporary_board


def specify_opponents_winning_moves_list(board, temporary_board, player):
    player = next_player(player, "X", "0")
    opponents_winning_moves_list = []
    opponents_winning_moves_list, temporary_board = specify_winning_moves_list(board, temporary_board, player)
    return opponents_winning_moves_list, temporary_board


def specify_possible_corner_field_moves():
    corner_fields = [[0, 0], [0, 2], [2, 0], [2, 2]]
    possible_corner_field_moves = []
    for field in corner_fields:
        if is_field_available(field[0], field[1]):
            possible_corner_field_moves.append(field)
    return(possible_corner_field_moves)


def get_ai_move(player):
    temporary_board = deepcopy(board)
    possible_moves_list = specify_possible_moves_list()
    winning_moves_list, temporary_board = specify_winning_moves_list(board, temporary_board, player)
    opponents_winning_moves_list, temporary_board = specify_opponents_winning_moves_list(board, temporary_board, player)
    possible_corner_field_moves = specify_possible_corner_field_moves()
    center_field = [1, 1]
        
    if len(winning_moves_list) > 0:
        move_coordinates = winning_moves_list[0]
    elif len(opponents_winning_moves_list) > 0:
        move_coordinates = opponents_winning_moves_list[0]
    elif board[1][1] == ".":
        move_coordinates = center_field
    elif len(possible_corner_field_moves) > 0:
        move_coordinates = random.choice(possible_corner_field_moves)
    else:
        move_coordinates = random.choice(possible_moves_list)

    time.sleep(1)
    return(move_coordinates)


# TRIGGERING A GAME

def play_game_with_other_human():
    player = "X"
    number_of_moves = 0
    number_of_possible_moves = 9
    print_board(board)
    while number_of_moves < number_of_possible_moves:
        move_coordinates = get_move_from(player)
        row = move_coordinates[0]
        col = move_coordinates[1]
        mark(board, player, row, col)
        print_board(board)

        if has_won(board, player) == True:
            print("Player " + player + " has won. Congratulations!")
            break

        player = next_player(player, "X", "0")
        number_of_moves += 1
    else:
        print("It's a tie!")
    
    decide_if_play_again()


def play_game_with_ai():
    player = "X"
    number_of_moves = 0
    number_of_possible_moves = 9
    print_board(board)

    while number_of_moves < number_of_possible_moves:
        if player == "X":
            move_coordinates = get_move_from(player)
        else:
            move_coordinates = get_ai_move(player)
        
        row = move_coordinates[0]
        col = move_coordinates[1]
        mark(board, player, row, col)
        print_board(board)

        if has_won(board, player) == True:
            print("Player " + player + " has won. Congratulations!")
            break

        player = next_player(player, "X", "0")
        number_of_moves += 1
    else:
        print("It's a tie!")
    
    decide_if_play_again()


def clear_board():
    global board
    board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
    return(board)


def tictactoe_game():
    print("Welcome!")
    print("If you want to play against another person, press 1")
    print("If you want to play with computer, press 2")
    print("If you want to close the game, type \"close\"")
    users_answer = input("")

    while users_answer:
        if users_answer == "1":
            board = clear_board()
            play_game_with_other_human()
            
        elif users_answer == "2":
            board = clear_board()
            play_game_with_ai()
            
        elif users_answer.upper() == "CLOSE":
            sys.exit()
        else:
            users_answer = input("Wrong answer. Try again: ")
            continue


tictactoe_game()