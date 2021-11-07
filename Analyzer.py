import copy
import numpy as np

from GameStates import GameStates
from GameState import GameState
from Group import Group


class Analyzer:
  def __init__(self):
    pass

  def findPossibleMoves(self, gameState, gameStates):
    if gameState.passedStreak == 2:
      return False
    move = -1 # set constant, always black
    # skip first board to play passing move
    gameStates.copyToIndex(0, gameState)
    gameStates.stateStack[0].passedStreak += 1
    board_counter = 1 

    testGameState = GameState()
    for x in range(len(gameState.board)):
      for y in range(len(gameState.board[0])):
        testGameState.board = np.copy(gameState.board)
        testGameState.whiteStonesCaptured = gameState.whiteStonesCaptured
        testGameState.blackStonesCaptured = gameState.blackStonesCaptured
        testGameState.passedStreak = 0
        if testGameState.board[x][y][0] != 0 or testGameState.board[x,y,1] == 1: # Check if empty and not Ko
          pass
        else:
          testGameState.resetKo()
          testGameState.board[x][y][0] = move
          self.captures(testGameState, (x,y))
          if self.suicide(testGameState, (x,y)):
            pass
          else:
            gameStates.copyToIndex(board_counter, testGameState)
            board_counter += 1
    gameStates.boardCount = board_counter
    return True
    
  def captures(self, gameState, position):
    position_color = gameState.board[position[0],position[1], 0]
    for neighbor in gameState.findNeighbors(position):
      neighbor_color = gameState.board[neighbor[0],neighbor[1], 0]
      if neighbor_color == -position_color:
        neighbor_group = Group(gameState, neighbor)
        if neighbor_group.liberties:
          pass
        else:
          if len(neighbor_group.stones) == 1: # If Ko:
            for stone in neighbor_group.stones:
              gameState.board[stone][1] = 1 
          for stone in neighbor_group.stones:
            gameState.board[stone[0],stone[1],0] = 0
            if position_color == -1:
              gameState.whiteStonesCaptured += 1
            else:
              gameState.blackStonesCaptured += 1
  
  def suicide(self, gameState, pos):
    group = Group(gameState, pos)
    if not group.liberties:
      return True
    return False

  def calculatePoints(self, gameState):
    eyes = [set(),set()]
    for x in range(len(gameState.board)):
      for y in range(len(gameState.board[0])):
        if gameState.board[x,y,0] == 0:
          group = Group(gameState, (x,y))
          neighbors = list(group.groupNeighbors)
          if len(neighbors) == 0:
            continue
          col = gameState.board[neighbors[0]][0]
          equal = True
          for n in neighbors:
            if gameState.board[n][0] != col:
              equal = False
          if equal is True:
            eyes[int((col+1)/2)].update(group.stones)
    # Return the difference in points. Blacks points are negative.
    return len(eyes[1])-len(eyes[0]) - gameState.whiteStonesCaptured + gameState.blackStonesCaptured

def testAnalyzer():
  game_states = GameStates()
  analyzer = Analyzer()
  game_state = GameState()
  # game_state.randomize()
  game_state.board[3,2:5,0] = 1
  game_state.board[2:5,3,0] = 1
  game_state.board[3,3,0] = 0
  print(analyzer.calculatePoints(game_state))
  game_state.board[3,3,0] = -1
  game_state.board[4,6,0] = -1
  game_state.board[4,3,1] = 1
  game_state.flip()
  analyzer.findPossibleMoves(game_state, game_states)
  # game_states.show()

  game_state.board.fill(1)
  analyzer.findPossibleMoves(game_state, game_states)
  new_game_state = copy.deepcopy(game_states.stateStack[0])
  analyzer.findPossibleMoves(new_game_state, game_states)
  print("pass state", game_states.stateStack[0])

if __name__ == "__main__":
  testAnalyzer()