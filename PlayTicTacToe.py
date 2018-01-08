# Imports
from LearnTicTacToe import * # (contains classes and functions)
from TicTacToeSetup import * # (setup file)
from random import randint
import time
import pickle

def PlayTicTacToe():

	# Global variables
	player1Wins = 0
	player2Wins = 0
	draws = 0

	# Play game numGames times (variable in setup file)
	for i in range(0,numGames):
		# Initializations
		victor = "n"
		playing = True
		firstRound = True
		board = "---------"

		# Tutorial
		if giveTutorial:
			print("\nThe board is numbered like this:")
			print("123")
			print("456")
			print("789")
			time.sleep(4)

		# Game loop 
		while playing:
			# Player 1 moves
			if isinstance(player1,Human) or isinstance(player2,Human):
				printBoard(board)
				print("\nPlayer 1's move (x)")
			board = player1.move(board, "x")

			# Check for victory
			victor = checkVictory(board)
			if victor != "n":
				playing = False
				break

			# Player 2 moves
			if isinstance(player1,Human) or isinstance(player2,Human):
				printBoard(board)
				print("\nPlayer 2's move (o)")
			board = player2.move(board, "o")

			# Check for victory
			victor = checkVictory(board)
			if victor != "n":
				playing = False
				break

		# Post-game
		if isinstance(player1,Human) or isinstance(player2,Human):
			printBoard(board)
			if victor == "x":
				print("Player 1 wins!")
				player1Wins += 1
			elif victor == "o":
				print("Player 2 wins!")
				player2Wins += 1
			else:
				print("Draw")
				draws += 1
		else:
			if victor == "x":
				player1Wins += 1
			elif victor == "o":
				player2Wins += 1
			else:
				draws += 1

		# Reward machine learning algorithm accordingly (if one played)
		if isinstance(player1, LearnTicTacToe):
			if victor == "x":
				player1.win()
			elif victor == "o":
				player1.lose()
			else:
				player1.draw()
			saveObject(player1, player1Name)
		if isinstance(player2, LearnTicTacToe):
			if victor == "x":
				player2.lose()
			elif victor == "o":
				player2.win()
			else:
				player2.draw()
			saveObject(player2, player2Name)
		if printi:
			print("Game " + str(i+1) + " complete")

	# Print desired objects
	if printPlayer1States:
		print("\nPlayer 1 states:")
		for state in player1.getStates():
			print(state + " " + str(player1.getStates()[state]))
	if printPlayer1Moves:
		print("\nPlayer 1 moves:")
		for move in player1.getMoves():
			print(move)
	if printPlayer2States:
		print("\nPlayer 2 states:")
		for state in player2.getStates():
			print(state + " " + str(player2.getStates()[state]))
	if printPlayer2Moves:
		print("\nPlayer 2 moves:")
		for move in player2.getMoves():
			print(move)
	if printPlayer1NumStates:
		print("\nPlayer 1 NumStates: " + str( len(player1.getStates()) ))
	if printPlayer2NumStates:
		print("\nPlayer 2 NumStates: " + str( len(player2.getStates()) ))
	if printWinLoseDraw:
		print("\nPlayer 1 wins: " + str(player1Wins))
		print("Player 2 wins: " + str(player2Wins))
		print("Draws: " + str(draws))
	if printWinLoseDrawPercent:
		print("\nPlayer 1 wins: " + str(round(player1Wins*100.0/numGames, 2)) + "%")
		print("Player 2 wins: " + str(round(player2Wins*100.0/numGames, 2))+ "%")
		print("Draws: " + str(round(draws*100.0/numGames, 2))+ "%")

	f = open("mltttData.txt", "a")
	f.write("\t" + str(round(player1Wins*100.0/numGames, 2)) + "%")
	f.write("\t" + str(round(player2Wins*100.0/numGames, 2))+ "%")
	f.write("\t" + str(round(draws*100.0/numGames, 2))+ "%")
	f.write("\n")
	f.close()
#PlayTicTacToe()