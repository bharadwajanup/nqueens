# nrooks.py : Solve the N-Rooks problem!
# D. Crandall, August 2016
#
# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.

import sys
import time

#Looks for the command line arguments for N. 
# Improvised on a solution in stack overflow which detects if an argument is a number or not: 
#http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float-in-python	
def supply_n_from_arg():
	if len(sys.argv)<=1:
		return False
	try:
		val = int(sys.argv[1])
		return val
	except ValueError:
		return False

# This is N, the size of the board.

N = supply_n_from_arg()
counter=0
if N:
	print "N value = " + str(N)
else:
	N = 2
	print "Please provide the N value in the argument.\nNo or invalid argument supplied. Setting default N = "+str(N)
	
		

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] )

def count_on_row_bitwise(board,row):
	0 if board[row] == 0 else 1 
	#Should have counted the number of 1's in the else part, but since I'm using 2 ** x values, I think there should be only one '1' in a row.

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

def count_on_col_bitwise(board, val):
	return board.count(val)
#val is an integer and the number of instances of the integer will be the number of pieces in the given column as the '1' represents a piece.
	

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

def count_pieces_bitwise(board):
	return sum(0 if row == 0 else bin(row).count('1') for row in board)

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join([ " ".join([ "Q" if col else "_" for col in row ]) for row in board])

#wrapper method to pass the list of list to the printable_board function.
def printable_board_bitwise(board):
	compatible_board = [[int(y) for y in bin(x)[2:].zfill(N)] for x in board]
	return printable_board(compatible_board)
		
		

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

def add_piece_bitwise(board,row,val):
	new_board = board[:]
	new_board[row] = val
	return new_board

def successors_bitwise_nrooks(board):
	succ = []
	current_state = board
	for row in range(0,N):
		if board[row] == 0:
			value = get_next_value(board,row)
			if value ==0:
				return succ
			succ.append(add_piece_bitwise(board,row,value))
			return succ
	
	return succ

def successors_bitwise_nqueens(board):
	succ = []
	current_state = board
	if count_pieces_bitwise(board) == 0:
		temp2 = 1#2**(N-1)
		while temp2 <= 2 ** N-1:
			next_state = add_piece_bitwise(board,0,temp2)
			succ.append(next_state)
			temp2 = temp2<<1
		return succ
	
	
	for row in range(0,N):
		if board[row] == 0:
			#print "row "+str(row)+" was zero"
			queen_values = get_next_values_nqueens(board,row-1)
			#print queen_values
			for v in queen_values:
				succ.append(add_piece_bitwise(board,row,v))
			return succ
	print succ
	return succ

def get_next_value(board,index):
	proposed_value = 2**(N-1-index)
	temp = proposed_value
	
	while temp >=0:
		if board.count(temp) == 0:
			return temp
		else:
			temp = temp>>1
	return 0;

	
def get_next_values_nqueens(board,prev_index):
	prev_val = board[prev_index]
	#print prev_val
	next_values = []
	
	if prev_index >= N-1:
		return next_values
	
	current_queen_row = prev_index + 1
	
	temp_right = prev_val >> 2

	while temp_right > 0:
		if is_valid_bitwise(board,current_queen_row,temp_right):
			next_values.append(temp_right)
		temp_right = temp_right>>1

	temp_left = prev_val<<2
	
	while temp_left <= 2 ** (N-1):
		if is_valid_bitwise(board,current_queen_row,temp_left):
			next_values.append(temp_left)
		temp_left = temp_left<<1
	return next_values

def is_valid_bitwise(board,queen_row,val):
	if board.count(val) != 0:
		return False
	temp_row = queen_row
	temp_val = val
	#quad 1
	while temp_row>0 and temp_val>1:
		temp_row-=1
		
		temp_val = temp_val>>1
		if board[temp_row] == temp_val:
			return False
	
	temp_row = queen_row
	temp_val = val
	#quad 2
	while temp_row>0:
		temp_row-=1
		temp_val = temp_val<<1
		if board[temp_row] == temp_val:
			#print "2"
			return False
	
	temp_row = queen_row
	temp_val = val
	while temp_row < N-1 and temp_val>1:
		temp_row +=1
		temp_val = temp_val>>1
		if board[temp_row] == temp_val:
			return False
	
	temp_row = queen_row
	temp_val = val
	while temp_row < N-1:
		temp_row +=1
		temp_val = temp_val<<1
		if board[temp_row] == temp_val:
			return False
	
	return True

# Get list of successors of given board state
def successors(board):
    return [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) ]


def successors2(board):
	succ = []
	board_count = count_pieces(board)
	for r in range(0,N):
		for c in range(0,N):
			next_possibility = add_piece(board,r,c)
			count_next_possibility = count_pieces(next_possibility)
			if count_next_possibility <= N and count_next_possibility > board_count:# and r == c: Hack that could help arrive at the nrooks solution faster.
				succ.append(next_possibility)
				global counter
				counter = counter + 1;
	return succ

def successors3(board):
	succ = []
	board_count = count_pieces(board)
	avail_rows = get_available_slots("row",board)
	avail_cols = get_available_slots("col",board)
	for r in avail_rows:
		for c in avail_cols:
			next_possibility = add_piece(board,r,c)
			count_next_possibility = count_pieces(next_possibility)
			if count_next_possibility <= N and count_next_possibility > board_count: # and r == c:
				succ.append(next_possibility)
				global counter
				counter = counter + 1;
				return succ;
	return succ	

#DeprecationWarning: Function is deprecated	
'''def successors4(board):
	global counter
	succ = []
	board_count = count_pieces(board)
	avail_rows = get_available_slots("row",board)
	avail_cols = get_available_slots("col",board)
	for r in avail_rows:
		for c in avail_cols:
			next_possibility = add_piece(board,r,c)
			count_next_possibility = count_pieces(next_possibility)
			if count_next_possibility <= N and count_next_possibility > board_count and no_queen_in_diagonal(r,c,board): # and r == c:
				succ.append(next_possibility)

				counter = counter + 1;
	return succ

#DeprecationWarning: Function is deprecated	
def successors6(board):
	succ = []
	global counter
	if count_pieces(board) == 0:
		for c in range(0,N):
			succ.append(add_piece(board,0,c))
			counter = counter+1
		return succ
	for r in range(0,N):
		for c in range(0,N):
			if board[r][c] == 1:
				possible_hops = get_possible_hops(board,r,c)
				for hop in possible_hops:
					succ.append(add_piece(board,hop[0],hop[1]))
					counter = counter + 1
				break;
	return succ
'''
def nqueens_successors(board):
	succ = []
	qr=0
	qc=0
	global counter
	if count_pieces(board) == 0:
		for c in range(0,N):
			succ.append(add_piece(board,0,c))
			counter = counter+1
		return succ
	for r in range(0,N):
		if count_on_row(board,r) == 0 and count_pieces(board) < N:
			next_possibility = get_next_queen(board,qr,qc)
			#if next_possibility:
			#	succ.append(add_piece(board,next_possibility[0],next_possibility[1]))
			#	counter = counter+1
			for possibility in next_possibility:
				succ.append(add_piece(board,possibility[0],possibility[1]))
				counter = counter+1
			return succ
				
		for c in range(0,N):
			if board[r][c] == 1:
				qr = r
				qc = c
				break;
	return succ
			

def get_next_queen(board,from_row,from_col):
	next_queens = []
	global N
	#print "From row: "+ str(from_row) + "From col "+ str(from_col)
	if from_row >=N or from_col >= N:
		print "End of board"
		return next_queens
	next_col = (from_col + 2) % N
	next_row = (from_row + 1) % N
	while True:
		if next_col == from_col:
			break
		if is_valid(board, next_row, next_col):
			#print "found row %s col %s" %(next_row,next_col)
			#return [next_row,next_col]
			next_queens.append([next_row,next_col])
		next_col = (next_col + 1) % N
	return next_queens

#DeprecationWarning: Function deprecated
'''	
def get_possible_hops(board,r,c):
	hops = []
	if r-2 >=0 and c+1 < N and is_valid(board,r-2,c+1):
		hops.append([r-2,c+1])
	if r+2 < N and c+1 < N and is_valid(board,r+2,c+1):
		hops.append([r+2,c+1])
	if r+2 < N and c-1 >= 0 and is_valid(board,r+2,c-1):
		hops.append([r+2,c-1])
	if r-2 >=0 and c-1 >= 0 and is_valid(board,r-2,c-1):
		hops.append([r-2,c-1])
	if r-1 >=0 and c-2 >= 0 and is_valid(board,r-1,c-2):
		hops.append([r-1,c-2])
	if r-1 >=0 and c+2 < N and is_valid(board,r-1,c+2):
		hops.append([r-1,c+2])
	if r+1 < N and c+2 < N and is_valid(board,r+1,c+2):
		hops.append([r+1,c+2])
	if r+1 < N and c-2 >= 0 and is_valid(board,r+1,c-2):
		hops.append([r+1,c-2])
	
	return hops
'''

#checks if a given piece at position (r,c) for the given board is a valid state for n-queens
def is_valid(board,r,c):
	if count_on_row(board,r) == 0 and count_on_col(board,c) == 0 and no_queen_in_diagonal(r,c,board):
		return True
	return False
	
	
#Checks if there are no queens in the diagonal			
def no_queen_in_diagonal(row,col,board):
	global N
	temp_row = row
	temp_col = col
	
	#quad 1
	while temp_row < N and temp_col < N:

		if board[temp_row][temp_col] == 1:
			return False
		temp_row+=1
		temp_col+=1
	
	temp_row = row
	temp_col = col
	
	#quad 2
	while temp_row >= 0 and temp_col < N:
		if board[temp_row][temp_col] == 1:
			return False
		temp_row-=1
		temp_col+=1
	
	temp_row = row
	temp_col = col
	#quad 3
	while temp_row >=0 and temp_col >=0:
		if board[temp_row][temp_col] == 1:
			return False
		temp_row-=1
		temp_col-=1
	
	temp_row = row
	temp_col = col
	
	#quad 4
	while temp_row < N and temp_col >= 0:
		if board[temp_row][temp_col] == 1:
			return False
		temp_row+=1
		temp_col-=1

	return True
		

def get_available_slots(type, board):
	temp = []
	if(type == "row"):	
		for r in range(0,N):
			if(count_on_row(board,r)==0):
				temp.append(r)
	else:
		for r in range(0,N):
			if(count_on_col(board,r)==0):
				temp.append(r)
	return temp	

			
			
# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )

def is_goal_bitwise(board):
	return count_pieces_bitwise(board) == N

# Solve n-rooks!
def solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors3( fringe.pop() ):
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False

def solve_bitwise_nrooks(initial_board):
	fringe = [initial_board]
	while len(fringe)>0:
		for s in successors_bitwise_nrooks(fringe.pop()):
			if is_goal_bitwise(s):
				return (s)
			fringe.insert(0,s)
	return False

def solve_bitwise_nqueens(initial_board):
	fringe = [initial_board]
	while len(fringe)>0:
		for s in successors_bitwise_nqueens(fringe.pop()):
			if is_goal_bitwise(s):
				return (s)
			#fringe.insert(0,s)
			fringe.append(s)
	return False 

#Uncomment the following lines to see the output for the bitwise operations approach
'''initial_board_bitwise = [0]*N
print ("Starting from initial board:\n" + printable_board_bitwise(initial_board_bitwise) + "\n\nLooking for solution...\n")
print ("Solution for bitwise start")
solution_bitwise = solve_bitwise_nrooks(initial_board_bitwise)
if solution_bitwise:
	print "Found solution"
print (printable_board_bitwise(solution_bitwise) if solution_bitwise else "Sorry, no solution found. :( ")
print ("End Bitwise")'''


def nqueens_solve(initial_board):
    fringe = [initial_board]
	
    while len(fringe) > 0:
        for s in nqueens_successors( fringe.pop() ):
            if is_goal(s):
                return(s)
            fringe.append(s)#fringe.insert(0,s)
			#fringe.append(s)
    return False

# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
initial_board = [[0]*N]*N
print ("Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n")


#solves n-rooks
#solution = solve(initial_board)

#solves n-queens
solution = nqueens_solve(initial_board)


print (printable_board(solution) if solution else "Sorry, no solution found. :( ")
#print "\n number of successors "+str(counter)



