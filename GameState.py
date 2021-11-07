import numpy as np
import matplotlib.pyplot as plt

class GameState:
  def __init__(self, board=None):
    self.board = np.zeros((9,9,2), dtype=np.float32) if board is None else board
    self.whiteStonesCaptured = 0
    self.blackStonesCaptured = 0
    self.passedStreak = 0

  def reset(self):
    self.board.fill(0)
    self.whiteStonesCaptured = 0
    self.blackStonesCaptured = 0
    self.passedStreak = 0
  
  def resetKo(self):
    self.board[:,:,1].fill(0)

  def randomize(self):
    randomLayer = np.random.randint(-1,2, (9, 9)).astype(np.float32)
    koLayer = np.zeros((9,9), dtype='f')
    self.board = np.dstack((randomLayer, koLayer))
    self.whiteStonesCaptured = np.random.randint(0,20)
    self.blackStonesCaptured = np.random.randint(0,20)

  def flip(self): #unit tested and working
    np.negative(self.board[:,:,0], out=self.board[:,:,0])
    temp = self.whiteStonesCaptured
    self.whiteStonesCaptured = self.blackStonesCaptured
    self.blackStonesCaptured = temp

  def findNeighbors(self, pos):
    dirs = [(1,0),(0,1),(-1,0),(0,-1)]
    min_x, min_y = 0,0
    max_x, max_y = len(self.board), len(self.board[0])
    for dir in dirs:
      x,y = (pos[0] - dir[0], pos[1] - dir[1])
      if not (min_x <= x < max_x and min_y <= y < max_y):
        pass
      else:
        yield (x,y)

  def show(self, ax=None):
    if ax is None:
      fig, ax = plt.subplots(1,1)
    ax.imshow(self.board[:,:,0], cmap='gray', vmin=-1, vmax=1)
    ax.set_xticks(np.arange(0, 9))
    ax.set_yticks(np.arange(0, 9))
    ax.tick_params(labeltop=True, labelright=True,length=0)
    ax.set_yticklabels(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'][:9])
    ax.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
  
  def __str__(self):
    return f"GameState with {self.board.shape} board, {self.whiteStonesCaptured} white stones captured, {self.blackStonesCaptured} black stones captured, and {self.passedStreak} passes."


if __name__ == "__main__":
    gameState = GameState()
    # %timeit gameState.findNeighbors((3,3))
    print(list(gameState.findNeighbors((3,3))))
    gameState.show()
    plt.show()