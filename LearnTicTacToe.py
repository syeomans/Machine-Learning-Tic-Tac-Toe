# Imports
from random import randint
import time
import pickle

##### Class definitions #####
class LearnTicTacToe:
	def __init__(self):
		"""
		Initialize the board states

		states: dictionary of dictionaries. The board begins clear (i.e., "---------"). 
			Terms of the outer dictionary are strings representing the current board state.
				Each square on the board is read top-to-bottom, left-to-right. If the square is unoccupied, it's
				represented with a dash. If it's occupied by an x, it's represented with an x. By an o, an o.
			Terms of the inner dictionary (definitions of the outer) are the 9 squares on the board, numbered 1-9.
			Definitions of the inner dictionary contain an integer representing the weight of chosing that square as a 
				next move. Higher weights are more likely to be chosen. An illegal move always has a weight of 0. All 
				legal moves begin at 2. Each time a game is won, this number is increased by 3. Each time a game is lost,
				this number decreases by 1. 

		moves: list of dictionaries.
			Each item in the list is a move that the computer made.
			Terms of the dictionaries are: "state", "square".
				"state": the state of the board for that given move
				"square": the move chosen during this state
		"""
		self.states = {"---------":{1:1, 2:1, 3:1, 4:1, 5:1, 6:1, 7:1, 8:1, 9:1}}
		self.moves = []

	def addState(self, stateToAdd):
		"""
		Add a board state to the states dictionary. 

		stateToAdd: string representing the state of the board.
			for example, if o has the top left corner and x has the bottom left and bottom right corners,
			the string is "o-----x-x"

		A move is only legal if there is neither an x nor an o in a space.
		"""
		# Start with a dictionary of all moves, legal and illegal.
		tempDict = {1:1, 2:1, 3:1, 4:1, 5:1, 6:1, 7:1, 8:1, 9:1}

		# Remove illegal moves
		for i in range(0,9):
			if stateToAdd[i] != "-":
				tempDict[i+1] = 0

		# Add dictionary of legal moves to the board states.
		self.states[stateToAdd] = tempDict

	def getStates(self):
		return(self.states)

	def getMoves(self):
		return(self.moves)

	def win(self):
		"""
		If this object wins, add three to the weights of all the moves that led to this win.
		"""
		for i in self.moves:
			thisState = i["state"]
			thisSquare = i["square"]
			self.states[thisState][thisSquare] += 3
		self.moves = []

	def lose(self):
		"""
		If this object loses, subtract one from the weights of all the moves that led to this loss.  
		"""
		for i in self.moves:
			thisState = i["state"]
			thisSquare = i["square"]
			self.states[thisState][thisSquare] -= 1
		self.moves = []

	def draw(self):
		"""
		If this object draws, add one to the weights of all the moves that led to this win.
		"""
		for i in self.moves:
			thisState = i["state"]
			thisSquare = i["square"]
			self.states[thisState][thisSquare] += 1
		self.moves = []

	def move(self, currentState, xo):
		"""
		Decide on a move to make and make it.

		Returns the board state of the next move as a string

		Using the weights of each square, pick randomly from the set of each possible move.
		Track the decision so that it can be scored later. 

		Also records the move in self.moves
		"""
		# Check if the given state or any symmetric form of the given state already exists. 
		numRotations = 0
		numMirrors = 0
		# If the current state doesn't match an existing state, rotate it to see if it matches a symmetric state
		if currentState not in self.states.keys():
			# rotate up to 4 times clockwise until a match is found, keeping track of the number of rotations
			for i in range(0,4):
				currentState = rotateRight(currentState)
				numRotations += 1
				if currentState in self.states.keys():
					break
			# If no match is found, mirror and repeat rotations until a match is found
			if currentState not in self.states.keys():
				currentState = mirror(currentState)
				numMirrors += 1
				for i in range(0,4):
					currentState = rotateRight(currentState)
					numRotations += 1
					if currentState in self.states.keys():
						break
			# If a match is still not found, undo rotations and add the state
			if currentState not in self.states.keys():
				currentState = mirror(currentState)
				numRotations = 0
				numMirrors = 0
				self.addState(currentState)

		# Find total weight by summing the weights of each square. (Illegal moves have weight 0.)
		totalWeight = 0
		while totalWeight == 0:
			for i in range(1, 10):
				totalWeight += self.states[currentState][i]
			# If no moves left, re-make the state
			if totalWeight == 0:
				self.addState(currentState)
		
		# Pick a weight between 1 and the total weight
		pickedWeight = randint(1,totalWeight)

		# Determine which square holds that weight
		# (Imagine the weights as beads in a matchbox. Pick one of the beads and see what color it is.)
		pickedSquare = 0
		while pickedWeight >0:
			pickedSquare += 1
			pickedWeight -= self.states[currentState][pickedSquare]

		# Generate the next state string
		nextStateList = list(currentState)
		nextStateList[pickedSquare - 1] = xo
		nextStateString = "".join(nextStateList)		

		# Record the move
		moveDict = {"state": currentState, "square": pickedSquare}
		self.moves.append(moveDict)

		# Undo any transformations
		for i in range(0,numRotations%4):
			nextStateString = rotateLeft(nextStateString)
		if numMirrors%2 == 1:
			nextStateString = mirror(nextStateString)

		# Return the string representing the next state
		return(nextStateString)

class RandomStrategy:
	def move(self, currentState, xo):
		# Make list of all legal moves
		stateList = list(currentState)
		legalMoves = []
		for i in range(0,9):
			if stateList[i] == "-":
				legalMoves.append(i)

		# Pick randomly from list of legal moves
		randNum = randint(0, len(legalMoves)-1)
		pick = legalMoves[randNum]

		# Generate the next state
		stateList[pick] = xo
		nextStateString = "".join(stateList)
		return(nextStateString)

class Human:
	def move(self, currentState, xo):
		# Get player's move 
		playerInput = str(raw_input("Pick a number 1-9:\n"))
		
		# Player input validation
		checking = True
		while checking:
			# Check if input is a number 1-9
			if playerInput not in str(range(1,10)):
				print("Invalid input. Pick a number 1-9")
				#printBoard(board)
				playerInput = str(raw_input("Pick a number 1-9:\n"))
				continue
			# Check if move was legal
			if currentState[int(playerInput)-1] != "-":
				print("Illegal move. Pick another square.")
				#printBoard(board)
				playerInput = str(raw_input("Pick a number 1-9:\n"))
				continue
			# Done checking. Break from loop.
			checking = False

		# Create new board state
		stateList = list(currentState)
		stateList[int(playerInput) -1] = xo
		currentState = "".join(stateList)
		return(currentState)

##### End class definitions #####

##### Function definitions #####

def rotateRight(board):
	boardList = list(board)
	newBoardList = [0, 1, 2, 3, 4, 5, 6, 7, 8]
	newBoardList[0] = boardList[6]
	newBoardList[1] = boardList[3]
	newBoardList[2] = boardList[0]
	newBoardList[3] = boardList[7]
	newBoardList[4] = boardList[4]
	newBoardList[5] = boardList[1]
	newBoardList[6] = boardList[8]
	newBoardList[7] = boardList[5]
	newBoardList[8] = boardList[2]
	newBoard = "".join(newBoardList)
	return(newBoard)

def rotateLeft(board):
	boardList = list(board)
	newBoardList = [0, 1, 2, 3, 4, 5, 6, 7, 8]
	newBoardList[0] = boardList[2]
	newBoardList[1] = boardList[5]
	newBoardList[2] = boardList[8]
	newBoardList[3] = boardList[1]
	newBoardList[4] = boardList[4]
	newBoardList[5] = boardList[7]
	newBoardList[6] = boardList[0]
	newBoardList[7] = boardList[3]
	newBoardList[8] = boardList[6]
	newBoard = "".join(newBoardList)
	return(newBoard)

def mirror(board):
	boardList = list(board)
	boardList[0],boardList[2] = boardList[2], boardList[0]
	boardList[3],boardList[5] = boardList[5], boardList[3]
	boardList[6],boardList[8] = boardList[8], boardList[6]
	newBoard = "".join(boardList)
	return(newBoard)

def saveObject(obj, name, printConfirmation = False):
	"""
	Save an object as [name].pickle

	obj: an object to be saved
	name: string to name file
	"""
	if printConfirmation:
		print("\nLearning from this experience")
		saveFile = open(name + ".pickle", "wb")
		pickle.dump(obj, saveFile)
		saveFile.close()
		print("Learned")
	else:
		saveFile = open(name + ".pickle", "wb")
		pickle.dump(obj, saveFile)
		saveFile.close()

def loadObject(name):
	"""
	Load a saved object

	name: string containing the beginning of the file name. 
		i.e. [name].pickle
	"""
	saveFile = open(name + ".pickle", "rb")
	obj = pickle.load(saveFile)
	saveFile.close()
	return(obj)

def printBoard(boardString):
	for i in range(0,3):
		print(boardString[0+3*i : 3+3*i])

def checkVictory(boardString):
	# Lists are easier to work with than strings
	board = list(boardString)
	
	# Check rows (0, 1, 2 and 3, 4, 5 and 6, 7, 8)
	for i in range(0,3):
		if board[0+i*3] == board[1+i*3] and board[1+i*3] == board[2+i*3]:
			victor = board[0+i*3]
			if victor != "-":
				return(victor)

	# Check columns (0, 3, 6 and 1, 4, 7 and 2, 5, 8)
	for i in range(0,3):
		if board[0+i] == board[3+i] and board[3+i] == board[6+i]:
			victor = board[0+i]
			if victor != "-":
				return(victor)

	# Check diagonals (0, 4, 8 and 2, 4, 6)
	if board[0] == board[4] and board[4] == board[8]:
		victor = board[0]
		if victor != "-":
			return(victor)
	elif board[2] == board[4] and board[4] == board[6]:
		victor = board[2]
		if victor != "-":
			return(victor)

	# If board is full and no one won, it's a draw
	if not "-" in board:
		return("d")

	# At this point, it's neither a win, nor a loss, nor a draw
	else:
		return("n")


