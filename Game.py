import copy
import numpy as np

from GameState import GameState
from GameStates import GameStates
from Analyzer import Analyzer
from Agent import Agent


class Game:
  def __init__(self):
    self.gameState = GameState()
    self.gameStates = GameStates()
    self.analyzer = Analyzer()

  def play(self, *agents, max_moves=100):#np.inf):
    player = 0
    counter = 0
    while self.analyzer.findPossibleMoves(self.gameState, self.gameStates) and counter < max_moves:
      self.makeMove(agents[player])
      # self.gameState.show()
      # print(self.gameState.whiteStonesCaptured, self.gameState.blackStonesCaptured)
      counter += 1
      player = not player
      self.gameState.flip()
    return self.analyzer.calculatePoints(self.gameState) * (player*-2+1)
  
  def makeMove(self, agent):
    bestMoveID = agent.findBestMove(self.gameStates)
    self.gameState = copy.deepcopy(self.gameStates.stateStack[bestMoveID])

  def playVerbose(self, *agents, max_moves=100):
    gameStates = []
    player = 0
    counter = 0
    while self.analyzer.findPossibleMoves(self.gameState, self.gameStates) and counter < max_moves:
      self.makeMove(agents[player])
      # self.gameState.show()
      # print(self.gameState.whiteStonesCaptured, self.gameState.blackStonesCaptured)
      counter += 1
      player = not player
      self.gameState.flip()
      gameStates.append(copy.deepcopy(gameState))
    return gameStates

def unitTestGame():
  game = Game()
  # game.gameState.board.fill(-1)
  game.gameState.board[0,0,0] = 0
  game.gameState.board[0,0,1] = 1
  agent0 = Agent()
  agent1 = Agent()
  print(game.play(agent0, agent1))
  game.gameState.show()
  
if __name__ == "__main__":
  unitTestGame()
# %timeit unitTestGame()