import random
from this import d
from click import getchar
import os

######################################################################
###                            METHODS                             ###
######################################################################


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def display_board(board):
    clearConsole()
    tempboard = ''
    for r in range(0,3):
        tempboard += ' | '.join(board[r*3:r*3+3]) + '\n'
    
    print(tempboard)


def choose_player():
    player1 = input("Enter player 1's name: ")
    player2 = input("Enter player 2's name: ")
    return ({'name': player1, 'score': 0}, {'name': player2, 'score': 0}) #return player name and score


def choose_markers(players):
    starting_player = random.choice(players)
    print(f"{starting_player['name']} goes first! (Note: First player is always X)")

    if starting_player == players[0]:
        players[0]['marker'] = 'X'
        players[1]['marker'] = 'O'
    else:
        players[0]['marker'] = 'O'
        players[1]['marker'] = 'X'
    return starting_player


def pick_and_place_marker(board, player):
    valid = False
    markers = ['X','O']

    while not valid:  
        print(f"\nPick a cell to place '{player['marker']}'(1-9): ")
        picked_cell = getchar()
        if picked_cell.isdigit():  
            picked_cell_index = int(picked_cell)-1
            if picked_cell_index in range(0,9) : 

                if board[picked_cell_index] not in markers:
                    board[picked_cell_index] = player['marker']
                    valid = True
                else:
                    print("**That cell has already been picked :( **") 
            else:
                print("**picked cell must be within the range (1-9) :( **") 
        else:
            print("**Picked cell is not an integer :( **")

    return board

def playersTurn(players, turn):
    if turn % 2 == 0:
        return next(filter(lambda x: x['marker'] == 'X', players), None)
    else:
        return next(filter(lambda x: x['marker'] == 'O', players), None)


def winning_condition(board, player):
    def calculate_win():
        print(f"{player['name']} '{player['marker']}' wins!!! ")
        player['score'] += 1 
    
    game_on = True

    #check board full
    if all([cell in ['X','O'] for cell in board]):
        print("Tie game! :/")
        return not game_on

    #checks rows
    for row in [0,3,6]:
        if all([cell == player['marker'] for cell in board[row:row+3]]):
            calculate_win()
            return not game_on

    #check columns
    for col in range(0,3):
        if all([cell == player['marker'] for cell in board[col::3]]):
            calculate_win()
            return not game_on

    #check diagnals
    if all([cell == player['marker'] for cell in board[0::4]]):
        calculate_win()
        return not game_on

    if all([cell == player['marker'] for cell in board[2:7:2]]):
        calculate_win()
        return not game_on
        
    return game_on

def reset_board():
    return [str(n) for n in range(1,10)]


def end_game(players):
    print('\nScore:')
    for player in players:
        print(f"{player['name']}: {player['score']}")

    valid = False
    user_input = ''
    while not valid:
        print("\nWould you like to play again? (Y/N)")
        user_input = getchar(True).upper()
        valid = user_input in ['Y', 'N']
    
    print('\n')
    return 'Y' == user_input

######################################################################
###                          START GAME                            ###
######################################################################

board = reset_board()
display_board(board)
players = choose_player()

replay = True
turn = 0
while replay:
    #reset board
    board = reset_board()

    display_board(board) 

    #return players in order of who goes first
    choose_markers(players)

    game_on = True
    while game_on:
        #checks whos turn it is and returns player 
        player = playersTurn(players, turn)

        #sends players, starting player and turn to find
        pick_and_place_marker(board, player)

        display_board(board)

        #check winning condition, increment score, print winner
        game_on = winning_condition(board, player)

        #increment turns
        turn += 1

    #Show score and ask if they would like to play again 
    replay = end_game(players)


