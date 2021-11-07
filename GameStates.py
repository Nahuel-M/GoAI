import numpy as np
import matplotlib.pyplot as plt

from GameState import GameState

class GameStates:
  def __init__(self):
    self.boardStack = np.zeros((82, 9, 9, 2), dtype=np.float32)
    self.stateStack = [GameState(board) for board in self.boardStack]
    self.boardCount = 82

  def __str__(self):
    return f"Boardstack shape: {self.boardStack.shape}. stateStack shape: {len(self.stateStack)}"
  
  def copyToIndex(self, index, gameState):
    self.boardStack[index] = np.copy(gameState.board)
    self.stateStack[index].blackStonesCaptured = gameState.blackStonesCaptured
    self.stateStack[index].whiteStonesCaptured = gameState.whiteStonesCaptured
    self.stateStack[index].passedStreak = gameState.passedStreak

  def show(self):
    fig, axs = plt.subplots(9,9, figsize=(18, 19))
    axs = axs.flatten()
    for i in range(self.boardCount - 1):
      self.stateStack[i+1].show(axs[i])


def unitTestGameStates():
  gameStates = GameStates()
  gameStates.show()
  print(gameStates)
  plt.show()
#unitTestGameStates()

if __name__ == "__main__":
    unitTestGameStates()