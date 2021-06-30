import math
from collections import deque
import os
import time 
import copy
from collections import defaultdict
from time import process_time
import time as t

initial = process_time()

# minimax(0, 4, g_grid, True, MAX, MIN, color)
end = process_time()
# print("TIME: ", end - initial)

def read_input(input_file):
    with open(str(input_file), 'r') as file:
        input_line = [line.strip() for line in file]
    return input_line


def read(input_den):
    locations_grid = [['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'], 
                  ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'], 
                  ['a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6'], 
                  ['a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5'], 
                  ['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4'], 
                  ['a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3'], 
                  ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'], 
                  ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']]
    try:
    # input_den =  + str(1) + '.txt'
        input_lines = read_input(input_den)

        selected_algo = str(input_lines[0])

        color = str(input_lines[1])

        time = float(input_lines[2])

        g_grid = input_lines[3:]

        for locations in range(len(g_grid)):

            modified_loc = "".join(g_grid[locations])
            g_grid[locations] = list(modified_loc)

    except:
        formatted_output = 'FAIL'
    
    return selected_algo, color, time, g_grid, locations_grid


def accessible_locations_normal(starting_loc_i,
                                starting_loc_j,
                                color, given_grid):
    
    
    if color == 'BLACK':
        accessible_node_list = []
        current_node = [[starting_loc_i, starting_loc_j]]

        for j in range(starting_loc_j - 1, starting_loc_j + 2):
            if j != -1 and j < 8:
                current_col = j

                # diagonal

                for i in range(starting_loc_i+1, starting_loc_i + 2):
                    if i != -1 and i < 8 and i != starting_loc_i and j != starting_loc_j:
                        current_row = i
                        if [i, j, given_grid[i][j], locations_grid[i][j]] not in accessible_node_list:
                            accessible_node_list.append([i, j, given_grid[i][j], locations_grid[i][j]])
                            
    elif color == 'WHITE':
        accessible_node_list = []
        current_node = [[starting_loc_i, starting_loc_j]]

        for j in range(starting_loc_j - 1, starting_loc_j + 2):
            if j != -1 and j < 8:
                current_col = j

                # diagonal

                for i in range(starting_loc_i-1, starting_loc_i):
                    if i != -1 and i < 8 and i != starting_loc_i and j != starting_loc_j:
                        current_row = i
                        if [i, j, given_grid[i][j], locations_grid[i][j]] not in accessible_node_list:
                            accessible_node_list.append([i, j, given_grid[i][j], locations_grid[i][j]])
    
    return (accessible_node_list)

# accessible_locations_normal(1,1, color, g_grid)

def estimate(given_grid, color):
    
    black_Score = 0
    white_Score = 0
    
    # heuristics
    same_half = 0
    other_half = 0
    kings = 0               # kings value = 10
    normal_piece = 0        # normal_pieces = 1
    potential_king = 0       # about to become king in single move = 5
    opponent_kings = 0
    opponent_normal_pieces = 0
    opponent_potential_king = 0
    estimated_score = 0
    jumps = 0
    singles = 0
    opponent_jumps = 0
    opponent_singles = 0
    save_their_kings = 0
    save_my_kings = 0
    
    if given_grid == None:
        return estimated_score
    
    #check colour
    if color == 'BLACK':
        opponent_color = 'w'
        player_color = 'b'
    else:
        opponent_color = 'b'
        player_color = 'w'
    
    
#     moves = check_moves(given_grid, color)
    
#     if moves != [[]]:              #ask  that if moves empty
#         for move in moves:
#             if move[0] == 'J':
#                 count = 0
#                 for item,i in zip(move, range(len(move))):
    
#                     if type(item) == list:
#                         count += 1
                

#                 jumps_possible = count           
#                 # print("jumps possible: ", jumps_possible)
#                 jumps += (3 * jumps_possible)
                
#             elif move[0] == 'E':
#                 singles_possible = len(moves)
#                 singles += (0.1 * singles_possible)       
#                 break
                
#     opponent_moves = check_moves(given_grid,  'WHITE' if color == 'BLACK' else 'WHITE')
#     if opponent_moves != [[]]:
#         for move in opponent_moves:
#             if move[0] == 'J':
#                 count = 0
#                 for item,i in zip(move, range(len(move))):
    
#                     if type(item) == list:
#                         count += 1

#                 op_jumps_possible = count
#                 print(op_jumps_possible)
#                 opponent_jumps-= (3 * op_jumps_possible)

#             elif move[0] == 'E':
#                 op_singles_possible = len(moves)
#                 opponent_singles -= (0.1 * singles_possible)
#                 break
                
# ['.', 'b', 'b', '.', '.', '.', '.', '.']
# ['.', '.', 'b', '.', 'b', '.', '.', '.']
# ['.', '.', '.', '.', '.', '.', 'B', '.']
# ['.', '.', '.', '.', '.', '.', '.', '.']
# ['.', 'b', '.', '.', '.', '.', '.', '.']
# ['.', '.', '.', '.', '.', 'W', '.', '.']
# ['.', 'b', '.', '.', '.', 'b', '.', '.']
# ['.', '.', '.', 'b', 'w', '.', '.', '.']
    #loop to calculate score for each position in a 8*8 board
    for row in range(0,8):
        for col in range(0,8):
            piece_value = given_grid[row][col]
            if piece_value == '.':
                continue
            elif (piece_value == player_color or piece_value == (str.upper(player_color))):
                    if piece_value == (str.upper(player_color)):                                  # KING
                        kings += 7.75
                    elif row == 6 and piece_value == str(player_color) and color == 'BLACK':     # About to be king - BLACK
                        potential_king += 0.1
                    elif row == 1 and piece_value == str(player_color) and color == 'WHITE':     # About to be king - WHITE
                        potential_king += 0.1
                    elif piece_value == str(player_color):                                       # NORMAL PIECE         
                        normal_piece += 5
                        
                    elif piece_value == str.upper(opponent_color):                        # OPPONENT king
                        opponent_kings -= 7.75
                    elif row == 6 and piece_value == str(opponent_color) and color == 'WHITE':     # About to be king - BLACK AS OPPONENT TO WHITE
                        opponent_potential_king -= 0.1
                    elif row == 1 and piece_value == str(opponent_color) and color == 'BLACK':     # About to be king - WHITE AS OPPONENT TO BLACK
                        opponent_potential_king -= 0.1 
                        
                    elif piece_value == str(opponent_color):                              # OPPONENT NORMAL PIECE
                        opponent_normal_pieces -= 5
                        
#     for row in range(0,4):
#         for col in range(0,4):
#             piece_value = given_grid[row][col]
#             if color == 'BLACK' and (piece_value == opponent_color or piece_value == str.upper(opponent_color)):      #OPPONENT PIECES IN PLAYER HALF - BLACK
#                 same_half -= 0.6
#             elif color == 'WHITE' and (piece_value == player_color or piece_value == str.upper(player_color)):       # WHITE'S IN BLACK PORTION IF WHITE IS PLAYER
#                 other_half += 0.6
                
#     for row in range(4,8):
#         for col in range(4,8):
#             piece_value = given_grid[row][col]
#             if color == 'WHITE' and (piece_value == player_color or piece_value == str.upper(player_color)):      #OPPONENT PIECES IN PLAYER HALF - WHITE
#                 same_half -= 0.6
#             elif color == 'BLACK' and (piece_value == player_color or piece_value == str.upper(player_color)):       # BLACK'S IN WHITE PORTION IF BLACK IS PLAYER
#                 other_half += 0.6    
    
    for col in range(0,8):
        if color == 'WHITE':
            piece_value = given_grid[7][col]
            if piece_value == 'w' or piece_value == 'W':
                save_their_kings += 4
            opponent_piece_value = given_grid[0][col]
            if opponent_piece_value == 'b' or opponent_piece_value == 'B':
                save_my_kings -= 4
        elif color == 'BLACK':
            piece_value = given_grid[0][col]
            if piece_value == 'b' or piece_value == 'B':
                save_their_kings += 4
            opponent_piece_value = given_grid[7][col]
            if opponent_piece_value == 'w' or opponent_piece_value == 'W':
                save_my_kings -= 4        
    
    # TOTAL SCORE
    estimated_score =  same_half + other_half + kings + normal_piece + potential_king + opponent_kings + opponent_normal_pieces + opponent_potential_king + jumps + singles + opponent_jumps + opponent_singles + save_their_kings + save_my_kings  
                    
    # RETURN total estimated score
    return estimated_score

def accessible_locations_king(given_grid, starting_loc_i,
                        starting_loc_j):
    accessible_node_list = []
    current_node = [[starting_loc_i, starting_loc_j]]

    for j in range(starting_loc_j - 1, starting_loc_j + 2):
        if j != -1 and j < 8:
            current_col = j

            # diagonal

            for i in range(starting_loc_i - 1, starting_loc_i + 2):
                if i != -1 and i < 8 and i != starting_loc_i and j != starting_loc_j:
                    current_row = i
                    if [i, j, given_grid[i][j], locations_grid[i][j]] not in accessible_node_list:
                        accessible_node_list.append([i, j, given_grid[i][j], locations_grid[i][j]])

    return (accessible_node_list)

# accessible_locations_king(g_grid, 1,1)

def get_modified_board(original_board, move):
    if move == []:

        return original_board
    else:
        temp_board = copy.deepcopy(original_board)
        if move[0] == 'E':
            initial_row, initial_col = move[3][0], move[3][1]
            final_row, final_col = move[4][0], move[4][1]
            temp_board[initial_row][initial_col] = '.'
            temp_board[final_row][final_col] = move[-1]
            return temp_board
        elif move[0] == 'J':
            initial_row, initial_col = move[3][0], move[3][1]
            final_row, final_col = move[-2][0], move[-2][1]
            # middle_row, middle_col = move[5][0], move[5][1]
            temp_board[initial_row][initial_col] = '.'
            for i in move[4:-2]:
                middle_row, middle_col = i[0], i[1]
                temp_board[middle_row][middle_col] = '.'
            temp_board[final_row][final_col] = move[-1]
            return temp_board

def get_modified_boards(original_board, color, move):
    boards = []
    moves = check_moves(copy.deepcopy(original_board), color)
    # print(moves)
    if moves == None:
        return None, original_board
    else:
        for move in moves:
            if move == None:
                return original_board
            else:
                # print(move)
                temp_board = copy.deepcopy(original_board)
                if move[0] == 'E':
                    initial_row, initial_col = move[3][0], move[3][1]
                    final_row, final_col = move[4][0], move[4][1]
                    temp_board[initial_row][initial_col] = '.'
                    temp_board[final_row][final_col] = move[-1]
                    boards.append(temp_board)
                elif move[0] == 'J':
                    initial_row, initial_col = move[3][0], move[3][1]
                    final_row, final_col = move[4][0], move[4][1]

                    temp_board[initial_row][initial_col] = '.'
                    for i in move[4:-2]:
                        middle_row, middle_col = i[0], i[1]
                        temp_board[middle_row][middle_col] = '.'
                    temp_board[final_row][final_col] = move[-1]
                    boards.append(temp_board)

    return boards

# get_modified_boards(copy.deepcopy(g_grid), color, )
#                     print(move, temp_board)

def next_move_valid_black(given_grid, move, jumping = False, answer = [], temp_answer = []):
    color = 'BLACK'
    if move[2] == 'b':
        count = 0
        next_move_locations = accessible_locations_normal(move[0], move[1], color, given_grid)

        for next_MOVE in next_move_locations:
            # check if the adjacent diagonal node is opposite color
            if (next_MOVE[2] == "w" or next_MOVE[2] == 'W'):
                
                # check if it is a left diagonal and the row is not greater than 8 and column is not -1
                if next_MOVE[1] < move[1] and (next_MOVE[0] + 1) < 8 and (next_MOVE[1] - 1) > -1 and given_grid[(next_MOVE[0] + 1)][(next_MOVE[1] - 1)] == ".":
                    # store the value in jump to
                    JUMP_TO = locations_grid[(next_MOVE[0] + 1)][(next_MOVE[1] - 1)]
                   
                    temp_answer.append(["J", move[-1], JUMP_TO, (move[0], move[1]), (next_MOVE[0], next_MOVE[1]), [next_MOVE[0] + 1, next_MOVE[1] - 1], move[2]])
                    # path.append(answer)
                    # update the jumping as I jumped in the previous statement
                    jumping = True
                    # update the values in positions
                    count += 1
                    given_grid[next_MOVE[0] + 1][next_MOVE[1] - 1] = 'b'
                    given_grid[next_MOVE[0]][next_MOVE[1]] = "."
                    given_grid[move[0]][move[1]] = "."

                    # on the next of next check the next to it
                    next_next = [(next_MOVE[0] + 1), (next_MOVE[1] - 1), 
                                 'b', 
                                locations_grid[(next_MOVE[0] + 1)][(next_MOVE[1] - 1)]]

                    valid = next_move_valid_black(given_grid, move = next_next, jumping = True, answer = answer, temp_answer = temp_answer)
                    temp_answer.remove(temp_answer[-1])              
                # check if it is a right diagonal and the row is less than 8 and column is not greater than 8
                elif next_MOVE[1] > move[1] and (next_MOVE[0] + 1) < 8 and (next_MOVE[1] + 1) < 8 and given_grid[(next_MOVE[0] + 1)][(next_MOVE[1] + 1)] == ".":
                        JUMP_TO = locations_grid[(next_MOVE[0] + 1)][(next_MOVE[1] + 1)]
              
                        temp_answer.append(["J", move[-1], JUMP_TO, (move[0], move[1]), (next_MOVE[0], next_MOVE[1]), [next_MOVE[0] + 1,next_MOVE[1] + 1], move[2]])
                        # path.append(answer)
                        # update the jumping as I jumped in the previous statement
                        jumping = True
                        count += 1
                        # update the values in the cells
                        given_grid[next_MOVE[0] + 1][next_MOVE[1] + 1] = 'b'
                        given_grid[next_MOVE[0]][next_MOVE[1]] = "."
                        given_grid[move[0]][move[1]] = "."
                        
                        # check the move from next of next of next
                        next_next = [(next_MOVE[0] + 1), (next_MOVE[1] + 1), 
                                     'b', 
                                     locations_grid[(next_MOVE[0] + 1)][(next_MOVE[1] + 1)]]

                        valid = next_move_valid_black(given_grid, move = next_next, jumping = True, answer = answer, temp_answer = temp_answer) 
                        temp_answer.remove(temp_answer[-1])       
            elif next_MOVE[2] == '.' and jumping == False:
                # given_grid = 
                jump_to = next_MOVE
                given_grid[next_MOVE[0]][next_MOVE[1]] = 'b'
                given_grid[move[0]][move[1]] = '.'
                answer.append([["E", move[-1], jump_to[-1], (move[0], move[1]), (next_MOVE[0], next_MOVE[1]), move[2]]])
        if temp_answer != None and count == 0:
            answer.append(copy.deepcopy(temp_answer))
            return answer
        elif count > 0:
            return answer
        else:
            return []
    
    elif move[2] == 'B':
        count = 0
        # if it is king check all the four locations
        next_move_locations = accessible_locations_king(given_grid, move[0], move[1])
        

        for next_MOVE in next_move_locations:

            # if the adjacent diagonal move is of opposite color
            if next_MOVE[2] == "w" or next_MOVE[2] == "W":

                # check if it is a left down diagonal and the row is not greater than 8 and column is not -1
                if next_MOVE[1] < move[1] and next_MOVE[0] > move[0] and (next_MOVE[0] + 1) < 8  and (next_MOVE[1] - 1) > -1 and given_grid[(next_MOVE[0] + 1)][(next_MOVE[1] - 1)] == ".":
                    # store the value in jump to
                    JUMP_TO = locations_grid[(next_MOVE[0] + 1)][(next_MOVE[1] - 1)]
                    # print if we found empty 
                    temp_answer.append(["J", move[-1], JUMP_TO, (move[0], move[1]), (next_MOVE[0], next_MOVE[1]), [next_MOVE[0] + 1, next_MOVE[1] - 1], move[2]])
                    count += 1
                    # path.append(answer)
                    # update the jumping as I jumped in the previous statement
                    jumping = True
                    # update the values in positions
                    given_grid[next_MOVE[0] + 1][next_MOVE[1] - 1] = "B"
                    given_grid[next_MOVE[0]][next_MOVE[1]] = "."
                    given_grid[move[0]][move[1]] = "."

                    # on the next of next check the next to it
                    next_next = [(next_MOVE[0] + 1), (next_MOVE[1] - 1), 
                                 "B", 
                                locations_grid[(next_MOVE[0] + 1)][(next_MOVE[1] - 1)]]
       
                    valid = next_move_valid_black(given_grid, move = next_next, jumping = True, answer = answer, temp_answer = temp_answer)
                    temp_answer.remove(temp_answer[-1])
                          
                # check if it is a right up diagonal and the row is less than 8 and column is not greater than 8
                elif next_MOVE[1] > move[1] and next_MOVE[0] < move[0] and (next_MOVE[0] - 1) >= 0 and (next_MOVE[1] + 1) < 8 and given_grid[(next_MOVE[0] - 1)][(next_MOVE[1] + 1)] == ".":
                    # check if next of next is empty or not
                    JUMP_TO = locations_grid[(next_MOVE[0] - 1)][(next_MOVE[1] + 1)]
                    # print if we found empty
                    temp_answer.append(["J", move[-1], JUMP_TO, (move[0], move[1]), (next_MOVE[0], next_MOVE[1]), [next_MOVE[0] - 1, next_MOVE[1] + 1], move[2]])
                    count += 1
                    # print(grid)
                    # update the jumping as I jumped in the previous statement
                    jumping = True
                    # update the values in the cells
                    given_grid[next_MOVE[0] - 1][next_MOVE[1] + 1] = "B"
                    given_grid[next_MOVE[0]][next_MOVE[1]] = "."
                    given_grid[move[0]][move[1]] = "."

                    # on the next of next check the next to it
                    next_next = [(next_MOVE[0] - 1), (next_MOVE[1] + 1), 
                                 "B", 
                                locations_grid[(next_MOVE[0] - 1)][(next_MOVE[1] + 1)]]

                    valid = next_move_valid_black(given_grid, move = next_next, jumping = True, answer = answer, temp_answer = temp_answer)
                    temp_answer.remove(temp_answer[-1])
                # check if it is a right down diagonal and the row is not greater than 8 and column is not -1
                elif next_MOVE[1] > move[1] and next_MOVE[0] > move[0] and (next_MOVE[0] + 1) < 8 and (next_MOVE[1] + 1) < 8 and given_grid[(next_MOVE[0] + 1)][(next_MOVE[1] + 1)] == ".":
                    # store the value in jump to
                    JUMP_TO = locations_grid[(next_MOVE[0] + 1)][(next_MOVE[1] + 1)]
                    # print if we found empty 
                    temp_answer.append(["J", move[-1], JUMP_TO, (move[0], move[1]), (next_MOVE[0], next_MOVE[1]), [next_MOVE[0] + 1, next_MOVE[1] + 1], move[2]])
                    # path.append(answer)
                    # update the jumping as I jumped in the previous statement
                    jumping = True
                    count += 1
                    # update the values in positions
                    given_grid[next_MOVE[0] + 1][next_MOVE[1] + 1] = "B"
                    given_grid[next_MOVE[0]][next_MOVE[1]] = "."
                    given_grid[move[0]][move[1]] = "."

                    # on the next of next check the next to it
                    next_next = [(next_MOVE[0] + 1), (next_MOVE[1] + 1), 
                                 'B', 
                                locations_grid[(next_MOVE[0] + 1)][(next_MOVE[1] + 1)]]

                    valid = next_move_valid_black(given_grid, move = next_next, jumping = True, answer = answer, temp_answer = temp_answer)
                    temp_answer.remove(temp_answer[-1])               
                # check if it is a left up diagonal and the row is less than 8 and column is not greater than 8
                elif next_MOVE[1] < move[1] and next_MOVE[0] < move[0] and (next_MOVE[0] - 1) > -1 and (next_MOVE[1] - 1) > -1 and given_grid[(next_MOVE[0] - 1)][(next_MOVE[1] - 1)] == ".":

                    JUMP_TO = locations_grid[(next_MOVE[0] - 1)][(next_MOVE[1] - 1)]
                    # print if we found empty
                    temp_answer.append(["J", move[-1], JUMP_TO, (move[0], move[1]), (next_MOVE[0], next_MOVE[1]), [next_MOVE[0] - 1, next_MOVE[1] - 1], move[2]])
                    # path.append(answer)
                    # print(grid)
                    # update the jumping as I jumped in the previous statement
                    jumping = True
                    count += 1
                    # update the values in the cells
                    given_grid[(next_MOVE[0] - 1)][(next_MOVE[1] - 1)] = 'B'
                    given_grid[next_MOVE[0]][next_MOVE[1]] = "."
                    given_grid[move[0]][move[1]] = "."

                    # check the move from next of next of next
                    next_next = [(next_MOVE[0] - 1), (next_MOVE[1] - 1), 
                                 'B', 
                                 locations_grid[(next_MOVE[0] - 1)][(next_MOVE[1] - 1)]]

                    valid = next_move_valid_black(given_grid, move = next_next, jumping = True, answer = answer, temp_answer = temp_answer) 
                    temp_answer.remove(temp_answer[-1])
                
#                 elif temp_answer != None:
#                     answer.append(copy.deepcopy(temp_answer)) 

                    
            elif next_MOVE[2] == '.' and jumping == False:
                jump_to = next_MOVE
                given_grid[next_MOVE[0]][next_MOVE[1]] = 'B'
                given_grid[move[0]][move[1]] = '.'
                answer.append([["E", move[-1], jump_to[-1], (move[0], move[1]), (next_MOVE[0], next_MOVE[1]), move[2]]])
        if temp_answer != None and count == 0:
            answer.append(copy.deepcopy(temp_answer))
            return answer
        elif count > 0:
            return answer
        else:
            return []

def next_move_valid_white(given_grid, move, jumping = False, answer = [], temp_answer = []):
    color = 'WHITE'

    if move[2] == 'w':
        count = 0
        next_move_locations = accessible_locations_normal(move[0], move[1], color, given_grid)


        for next_MOVE in next_move_locations:
            # check if the adjacent diagonal node is opposite color
            if (next_MOVE[2] == "b" or next_MOVE[2] == 'B'):
                
                # check if it is a left diagonal and the row is not greater than 8 and column is not -1
                if next_MOVE[1] < move[1] and (next_MOVE[0] - 1) > -1 and (next_MOVE[1] - 1) > -1 and given_grid[(next_MOVE[0] - 1)][(next_MOVE[1] - 1)] == ".":
                    # store the value in jump to
                    JUMP_TO = locations_grid[(next_MOVE[0] - 1)][(next_MOVE[1] - 1)]
                    # print if we found empty
                    temp_answer.append(["J", move[-1], JUMP_TO, (move[0], move[1]), (next_MOVE[0], next_MOVE[1]), [next_MOVE[0] - 1, next_MOVE[1] - 1], move[2]])
                    # path.append(answer)
                    # update the jumping as I jumped in the previous statement
                    jumping = True
                    # update the values in positions
                    count += 1
                    given_grid[next_MOVE[0] - 1][next_MOVE[1] - 1] = 'w'
                    given_grid[next_MOVE[0]][next_MOVE[1]] = "."
                    given_grid[move[0]][move[1]] = "."

                    # on the next of next check the next to it
                    next_next = [(next_MOVE[0] - 1), (next_MOVE[1] - 1), 
                                 'w', 
                                locations_grid[(next_MOVE[0] - 1)][(next_MOVE[1] - 1)]]

                    valid = next_move_valid_white(given_grid, move = next_next, jumping = True, answer = answer, temp_answer = temp_answer)
                    temp_answer.remove(temp_answer[-1])              
                # check if it is a right diagonal and the row is less than 8 and column is not greater than 8
                elif next_MOVE[1] > move[1] and (next_MOVE[0] - 1) > -1 and (next_MOVE[1] + 1) < 8 and given_grid[(next_MOVE[0] - 1)][(next_MOVE[1] + 1)] == ".":
                        JUMP_TO = locations_grid[(next_MOVE[0] - 1)][(next_MOVE[1] + 1)]
                        # print if we found empty
                        temp_answer.append(["J", move[-1], JUMP_TO, (move[0], move[1]), (next_MOVE[0], next_MOVE[1]), [next_MOVE[0] - 1,next_MOVE[1] + 1], move[2]])
                        # path.append(answer)
                        # update the jumping as I jumped in the previous statement
                        jumping = True
                        count += 1
                        # update the values in the cells
                        given_grid[next_MOVE[0] - 1][next_MOVE[1] + 1] = 'w'
                        given_grid[next_MOVE[0]][next_MOVE[1]] = "."
                        given_grid[move[0]][move[1]] = "."
                        
                        # check the move from next of next of next
                        next_next = [(next_MOVE[0] - 1), (next_MOVE[1] + 1), 
                                     'w', 
                                     locations_grid[(next_MOVE[0] - 1)][(next_MOVE[1] + 1)]]

                        valid = next_move_valid_white(given_grid, move = next_next, jumping = True, answer = answer, temp_answer = temp_answer) 
                        temp_answer.remove(temp_answer[-1])       
            elif next_MOVE[2] == '.' and jumping == False:
                # given_grid = 
                jump_to = next_MOVE
                given_grid[next_MOVE[0]][next_MOVE[1]] = 'w'
                given_grid[move[0]][move[1]] = '.'
                answer.append([["E", move[-1], jump_to[-1], (move[0], move[1]), (next_MOVE[0], next_MOVE[1]), move[2]]])
        if temp_answer != None and count == 0:
            answer.append(copy.deepcopy(temp_answer))
            return answer
        elif count > 0:
            return answer
        else:
            return []
    
    elif move[2] == 'W':
        count = 0
        # if it is king check all the four locations
        next_move_locations = accessible_locations_king(given_grid, move[0], move[1])
        

        for next_MOVE in next_move_locations:

            # if the adjacent diagonal move is of opposite color
            if next_MOVE[2] == "b" or next_MOVE[2] == "B":

                # check if it is a left down diagonal and the row is not greater than 8 and column is not -1
                if next_MOVE[1] < move[1] and next_MOVE[0] > move[0] and (next_MOVE[0] + 1) < 8  and (next_MOVE[1] - 1) > -1 and given_grid[(next_MOVE[0] + 1)][(next_MOVE[1] - 1)] == ".":
                    # store the value in jump to
                    JUMP_TO = locations_grid[(next_MOVE[0] + 1)][(next_MOVE[1] - 1)]
                    # print if we found empty 
                    temp_answer.append(["J", move[-1], JUMP_TO, (move[0], move[1]), (next_MOVE[0], next_MOVE[1]), [next_MOVE[0] + 1, next_MOVE[1] - 1], move[2]])
                    count += 1
                    # path.append(answer)
                    # update the jumping as I jumped in the previous statement
                    jumping = True
                    # update the values in positions
                    given_grid[next_MOVE[0] + 1][next_MOVE[1] - 1] = "W"
                    given_grid[next_MOVE[0]][next_MOVE[1]] = "."
                    given_grid[move[0]][move[1]] = "."

                    # on the next of next check the next to it
                    next_next = [(next_MOVE[0] + 1), (next_MOVE[1] - 1), 
                                 "W", 
                                locations_grid[(next_MOVE[0] + 1)][(next_MOVE[1] - 1)]]
     
                    valid = next_move_valid_white(given_grid, move = next_next, jumping = True, answer = answer, temp_answer = temp_answer)
                    temp_answer.remove(temp_answer[-1])
                       
                # check if it is a right up diagonal and the row is less than 8 and column is not greater than 8
                elif next_MOVE[1] > move[1] and next_MOVE[0] < move[0] and (next_MOVE[0] - 1) >= 0 and (next_MOVE[1] + 1) < 8 and given_grid[(next_MOVE[0] - 1)][(next_MOVE[1] + 1)] == ".":
                    # check if next of next is empty or not
                    JUMP_TO = locations_grid[(next_MOVE[0] - 1)][(next_MOVE[1] + 1)]
                    # print if we found empty
                    temp_answer.append(["J", move[-1], JUMP_TO, (move[0], move[1]), (next_MOVE[0], next_MOVE[1]), [next_MOVE[0] - 1, next_MOVE[1] + 1], move[2]])
                    count += 1
           
                    # update the jumping as I jumped in the previous statement
                    jumping = True
                    # update the values in the cells
                    given_grid[next_MOVE[0] - 1][next_MOVE[1] + 1] = "W"
                    given_grid[next_MOVE[0]][next_MOVE[1]] = "."
                    given_grid[move[0]][move[1]] = "."

                    # on the next of next check the next to it
                    next_next = [(next_MOVE[0] - 1), (next_MOVE[1] + 1), 
                                 "W", 
                                locations_grid[(next_MOVE[0] - 1)][(next_MOVE[1] + 1)]]

                    valid = next_move_valid_white(given_grid, move = next_next, jumping = True, answer = answer, temp_answer = temp_answer)
                    temp_answer.remove(temp_answer[-1])
                # check if it is a right down diagonal and the row is not greater than 8 and column is not -1
                elif next_MOVE[1] > move[1] and next_MOVE[0] > move[0] and (next_MOVE[0] + 1) < 8 and (next_MOVE[1] + 1) < 8 and given_grid[(next_MOVE[0] + 1)][(next_MOVE[1] + 1)] == ".":
                    # store the value in jump to
                    JUMP_TO = locations_grid[(next_MOVE[0] + 1)][(next_MOVE[1] + 1)]
                    # print if we found empty 
                    temp_answer.append(["J", move[-1], JUMP_TO, (move[0], move[1]), (next_MOVE[0], next_MOVE[1]), [next_MOVE[0] + 1, next_MOVE[1] + 1], move[2]])
                    # path.append(answer)
                    # update the jumping as I jumped in the previous statement
                    jumping = True
                    count += 1
                    # update the values in positions
                    given_grid[next_MOVE[0] + 1][next_MOVE[1] + 1] = "W"
                    given_grid[next_MOVE[0]][next_MOVE[1]] = "."
                    given_grid[move[0]][move[1]] = "."

                    # on the next of next check the next to it
                    next_next = [(next_MOVE[0] + 1), (next_MOVE[1] + 1), 
                                 'W', 
                                locations_grid[(next_MOVE[0] + 1)][(next_MOVE[1] + 1)]]

                    valid = next_move_valid_white(given_grid, move = next_next, jumping = True, answer = answer, temp_answer = temp_answer)
                    temp_answer.remove(temp_answer[-1])               
                # check if it is a left up diagonal and the row is less than 8 and column is not greater than 8
                elif next_MOVE[1] < move[1] and next_MOVE[0] < move[0] and (next_MOVE[0] - 1) > -1 and (next_MOVE[1] - 1) > -1 and given_grid[(next_MOVE[0] - 1)][(next_MOVE[1] - 1)] == ".":

                    JUMP_TO = locations_grid[(next_MOVE[0] - 1)][(next_MOVE[1] - 1)]
                    # print if we found empty
                    temp_answer.append(["J", move[-1], JUMP_TO, (move[0], move[1]), (next_MOVE[0], next_MOVE[1]), [next_MOVE[0] - 1, next_MOVE[1] - 1], move[2]])
                    # path.append(answer)
          
                    # update the jumping as I jumped in the previous statement
                    jumping = True
                    count += 1
                    # update the values in the cells
                    given_grid[(next_MOVE[0] - 1)][(next_MOVE[1] - 1)] = 'W'
                    given_grid[next_MOVE[0]][next_MOVE[1]] = "."
                    given_grid[move[0]][move[1]] = "."

                    # check the move from next of next of next
                    next_next = [(next_MOVE[0] - 1), (next_MOVE[1] - 1), 
                                 'W', 
                                 locations_grid[(next_MOVE[0] - 1)][(next_MOVE[1] - 1)]]

                    valid = next_move_valid_white(given_grid, move = next_next, jumping = True, answer = answer, temp_answer = temp_answer) 
                    temp_answer.remove(temp_answer[-1])
                
#                 elif temp_answer != None:
#                     answer.append(copy.deepcopy(temp_answer)) 

                    
            elif next_MOVE[2] == '.' and jumping == False:
                jump_to = next_MOVE
                given_grid[next_MOVE[0]][next_MOVE[1]] = 'W'
                given_grid[move[0]][move[1]] = '.'
                answer.append([["E", move[-1], jump_to[-1], (move[0], move[1]), (next_MOVE[0], next_MOVE[1]), move[2]]])
        if temp_answer != None and count == 0:
            answer.append(copy.deepcopy(temp_answer))
            return answer
        elif count > 0:
            return answer
        else:
            return []

def join_moves(moves):
    path = []
    for move in moves:
        answer = move[0]
        for j in move[1:]:
            answer[2] = j[2]
            answer = list(answer[:-1]) + list(j[3:-1]) + list(answer[-1]) 

        path.append(answer)
    
    return sorted(path, key = len, reverse = True)

def check_moves(board, color):      # return all the umps on the boards else return all single moves
    moves_available_single = []
    moves_available_jump = []
    moves_available = []
    boards_amended = []
    for i in range(0, 8):
        for j in range(0, 8):
            try:
                initial_coin = [i, j, board[i][j], locations_grid[i][j]]
            except :
                print("Board is incomplete, error thrown")
            if color == 'BLACK' and (board[i][j] == 'b' or board[i][j] == 'B'):
                board_used = copy.deepcopy(board) 
                valid_moves = next_move_valid_black(board_used, initial_coin, False, [])

                for valid_move in valid_moves:

                    if (valid_moves != [[]] and valid_move != []) and valid_move[0][0] == 'J':
                        # valid = join_moves(valid_move)
                        moves_available_jump.append(valid_move)
                    elif (valid_moves != [[]] and valid_move != []) and valid_move[0] == 'J':
                        # valid = join_moves(valid_move)
                        moves_available_jump.append([valid_move])
                    elif (valid_moves != [[]] and valid_move != []) and valid_move[0][0] == 'E':
                        moves_available_single.append(valid_move)
                    elif valid_moves == [[[]]]:
                        continue

                
            elif color == 'WHITE' and (board[i][j] == 'w' or board[i][j] == 'W'):

                board_used = copy.deepcopy(board)                 
                valid_moves = next_move_valid_white(board_used, initial_coin, False, [])

                for valid_move in valid_moves:
                    if (valid_moves != [[]] and valid_move != []) and valid_move[0][0] == 'J':
                        moves_available_jump.append(valid_move)
                    elif (valid_moves != [[]] and valid_move != []) and valid_move[0] == 'J':

                        moves_available_jump.append([valid_move])
                    elif (valid_moves != [[]] and valid_move != []) and valid_move[0][0] == 'E':
                        moves_available_single.append(valid_move)
                    elif valid_moves == [[[]]] or valid_move == []:
                        continue

    if moves_available_jump != []:
        moves_available.append(join_moves(moves_available_jump))
        
    else:
        moves = []
        for (m) in (moves_available_single):
            for i in m:
                moves.append(i)
        if len(moves) > 0:
            return moves
        elif moves == [[]]:
            return [[]]


    if len(moves_available) == 0 or len(moves_available[0]) == 0:
        return [[]]
    
    else:
        move = []
        if len(moves_available) >= 1:
            for mov in moves_available:
                for m in mov:
                    move.append(m)
            return move

        elif moves_available == [[]]:

            return [[]]
    
# moves = check_moves(copy.deepcopy(g_grid), color)
# print(moves)

# Python3 program to demonstrate 
# working of Alpha-Beta Pruning 

# Initial values of Aplha and Beta 
# MIN, MAX = int(100000), int(-100000)

# Returns optimal value for current player 
#(Initially called for root and maximizer) 
flag = 1
def minimax(depth, depthLimit, parent_grid, maximizingPlayer, 
            alpha, beta, color): 
    # print("Depth: ", depth)
    if  t.time() < i_time + time_for_move - 0.2:
        
        # Terminating condition. i.e 
        # leaf node is reached 
        if depth == depthLimit: 
            score = estimate(parent_grid, max_color)
            return score

        if maximizingPlayer: 

            best = MAX
            temp_board = copy.deepcopy(parent_grid)  
            moves = check_moves(copy.deepcopy(parent_grid), max_color)
            if moves != [[]]:
                # Recur for left and right children 
                for move in range(len(moves)):
                    # print(moves[move])
                    temp_board = copy.deepcopy(parent_grid)      
                    new_board = get_modified_board(parent_grid, moves[move])
                    val = minimax(depth + 1, depthLimit, new_board, 
                                False, alpha, beta, min_color) 
                    parent_grid = copy.deepcopy(temp_board)
                    if val != None:
                        best = max(best, val) 
                        alpha = max(alpha, best) 
                    
                    estimated_moves.append([val, moves[move]])         #ask

                    # Alpha Beta Pruning 
                    if beta <= alpha: 
                        break

                return best
            else:
                return best

        else: 
            best = MIN
            temp_board = copy.deepcopy(parent_grid)           
            moves = check_moves(copy.deepcopy(parent_grid), min_color)
            if moves != [[]]:
                # Recur for left and 
                # right children 
                for move in moves:
                    temp_board = copy.deepcopy(parent_grid)
                    new_board = get_modified_board(parent_grid, move)

                    val = minimax(depth + 1,depthLimit, new_board, 
                                    True, alpha = alpha, beta = beta, color = max_color) 
                    parent_grid = copy.deepcopy(temp_board)
                    if val != None:
                        best = min(best, val) 
                        beta = min(beta, best) 
                    # estimated_moves.append([best, move])      #ask
                    # Alpha Beta Pruning 
                    if beta <= alpha: 
                        break

                return best 
            else:
                return best    #ask
    else:
        flag = 0
        return 

initial = t.process_time()                                         # SET INITIAL CLOCK

input_den = '/Users/kjindal/Downloads/Code/sample/input3.txt'         # input_path
playdata_den = '/Users/kjindal/Downloads/Code/sample/playdata.txt'    # playdata_path
output_den = '/Users/kjindal/Downloads/Code/sample/output.txt'    # playdata_path

# read input
selected_algo, color, time, g_grid, locations_grid = read(input_den)

# initial conditions
estimated_moves = []
MIN, MAX = int(100000), int(-100000)
max_color = color
min_color = 'BLACK' if color == 'WHITE' else 'WHITE'
elapsed_time = 0

# read or write to playdata.txt if it is the first move in game
with open(playdata_den, 'a+') as playdata:
    if color == 'BLACK':
        count = 0
        for i in range(0,3):
            for j in range(0,8):
                piece_value = g_grid[i][j]
                if piece_value == 'b':
                    count += 1
        if count == 12:
            playdata.truncate(0)
            playdata.write(str(time/60))
            time_for_move = time/60
            playdata.close()
        else:
            for x in playdata:
                time_for_move = float(x)
            playdata.close()

    elif color == 'WHITE':
        count = 0
        for i in range(5,8):
            for j in range(0,8):
                piece_value = g_grid[i][j]
                if piece_value == 'w':
                    count += 1
        if count == 12:
            playdata.truncate(0)
            playdata.write(str(time/60))
            time_for_move = time/60
            playdata.close()
        else:
            for x in playdata:
                time_for_move = float(x)
            playdata.close()

# single moves
formatted_output = []

# print("time_for_move: ", time_for_move)
if selected_algo == 'SINGLE':
    moves = check_moves(g_grid, color)   
    # print(moves)
    answer = (moves[0])
    # print(answer)
    if answer[0] == 'E':
        formatted_output = str(answer[0]) + ' ' + str(answer[1]) + ' ' + str(answer[2])
    elif answer[0] == 'J':
        formatted_output_new = str(answer[0]) + ' ' + str(answer[1])
        for item,i in zip(answer[3:], range(len(answer[3:]))):
            if type(item) == list:
                formatted_output.append(str(formatted_output_new + ' ' + str(locations_grid[item[0]][item[1]])))
                formatted_output_new = str(answer[0]) + ' ' + str(locations_grid[item[0]][item[1]])            
                
elif selected_algo == 'GAME':
    val = MAX
    i_time = t.time()
    for dL in range(1,3):
        if t.time() < i_time + time_for_move - 0.2:
            # print("minimax: ", dL)
            curr_val = minimax(0, dL , copy.deepcopy(g_grid), True, MAX, MIN, color) 
            if flag == 0:
                break
            val = curr_val
            moves = check_moves(g_grid, color)
            # print("moves: ", moves)
            f_time = t.process_time()
            elapsed_time = f_time
            matches = list()
            for sublist in estimated_moves:
                if sublist[0] == val and sublist[1] in moves:
                    matches.append(sublist)
            got_moves = sorted(matches, key = lambda x: len(x[1]), reverse = True)
            # print("after minimax")
            answer = (got_moves[0])
            # print(answer)
    
    
    if val == MAX or val == MIN:
        moves = check_moves(copy.deepcopy(g_grid), color)
        # print("max min")
        answer = (moves[0])
        if answer[0][0] == 'E':
            formatted_output = str(answer[0][0]) + ' ' + str(answer[0][1]) + ' ' + str(answer[0][2])
        elif answer[0][0] == 'J':
            formatted_output_new = str(answer[1][0]) + ' ' + str(answer[1][1])
            for item,i in zip(answer, range(len(answer))):
                if type(item) == list:
                    formatted_output.append(str(formatted_output_new + ' ' + str(locations_grid[item[0]][item[1]])))
                    formatted_output_new = str(answer[1][0]) + ' ' + str(locations_grid[item[0]][item[1]])            

        
    else:
        matches = list()
        for sublist in estimated_moves:
            if sublist[0] == val and sublist[1] in moves:
                matches.append(sublist)
        got_moves = sorted(matches, key = lambda x: len(x[1]), reverse = True)
        
        answer = (got_moves[0])
        
        required_string = set()
        if answer[1][0] == 'E':
            formatted_output = str(answer[1][0]) + ' ' + str(answer[1][1]) + ' ' + str(answer[1][2])  
        elif answer[1][0] == "J":
            formatted_output_new = str(answer[1][0]) + ' ' + str(answer[1][1])
            for item,i in zip(answer[1], range(len(answer[1]))):
                if type(item) == list:
                    formatted_output.append(str(formatted_output_new + ' ' + str(locations_grid[item[0]][item[1]])))
                    formatted_output_new = str(answer[1][0]) + ' ' + str(locations_grid[item[0]][item[1]])
            

# print(len(formatted_output))

with open(output_den, 'w') as f1:
    if formatted_output[0][0] == 'J':
        for output in formatted_output:
            f1.write(output + "\n")
    else:
        # print(formatted_output)
        f1.write(formatted_output)    
f1.close()

# with open(output_den, 'a+') as f1:
#     for i in formatted_output: 
        
