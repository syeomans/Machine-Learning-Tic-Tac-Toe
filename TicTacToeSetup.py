from LearnTicTacToe import *

# Create player 1 object
# player1Name = "mlttt" # Only used if player is a LearnTicTacToe object
# player1 = loadObject(player1Name) # use loadObject([name]), Human(), LearnTicTacToe(), or Random()
player1Name = "Randy"
player1 = loadObject(player1Name)
#player1 = RandomStrategy()
#player1 = LearnTicTacToe()

# Create player 2 object
player2Name = "Randy" # Only used if player is a LearnTicTacToe object
#player2 = loadObject(player2Name) # use loadObject([name]), Human(), LearnTicTacToe(), or RandomStrategy()
#player2 = RandomStrategy()
player2 = Human()
# Display tutorial?
# The board is numbered like this:
# 123
# 456
# 789
giveTutorial = False

# Print options
printPlayer1States = False
printPlayer1Moves = False

printPlayer2States = False
printPlayer2Moves = False

printPlayer1NumStates = False
printPlayer2NumStates = False

printWinLoseDraw = True
printWinLoseDrawPercent = False

printi = True

# Number of games
numGames = 1