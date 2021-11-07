import numpy as np
import matplotlib.pyplot as plt

from GameState import GameState
from NeighborFinder import NeighborFinder


neighborFinder99 = NeighborFinder((9,9))

class Group:
  def __init__(self, game_state, pos):
    self.start_pos = pos
    self.stones = {pos}
    self.liberties = set()
    self.groupNeighbors = set()
    self.color = game_state.board[pos[0],pos[1],0]
    self.findGroup(game_state, pos)
    if self.color == 0:
      self.findGroupNeighbors(game_state)
    else:
      self.findGroupLiberties(game_state)
    
  def findGroup(self, game_state, pos):
    for neighbor in neighborFinder99.neighborLookupTable[pos[0]][pos[1]]:
      if neighbor in self.stones:
        pass
      elif game_state.board[neighbor][0] == self.color:
        self.stones.update({neighbor})
        self.findGroup(game_state, neighbor)

  def findGroupNeighbors(self, game_state):
    for pos in self.stones:
      for neighbor in neighborFinder99.neighborLookupTable[pos[0]][pos[1]]:
        if neighbor not in self.stones:
          self.groupNeighbors.update({neighbor})

  def findLibertiesStone(self, game_state, pos):
    color = game_state.board[pos[0],pos[1],0]
    # if color == 0:
      # return 0
    min_x, min_y = 0,0
    max_x, max_y = len(game_state.board), len(game_state.board[0])
    liberties = set()
    for neighbor in neighborFinder99.neighborLookupTable[pos[0]][pos[1]]:
      if game_state.board[neighbor[0],neighbor[1],0] == 0:
        liberties.update({neighbor})
    return liberties

  def findGroupLiberties(self, game_state):
    self.liberties = set()
    for stone in self.stones:
      stonelibs = self.findLibertiesStone(game_state, stone)
      self.liberties.update(stonelibs)

  def __str__(self):
    color = "white" if self.color == 1 else "black"
    return f"{color} group with stones on {self.stones} and {len(self.liberties)} liberties: {self.liberties}"

  def show(self, game_state, plotax=None):
    if plotax is None:
      fig, plotax = plt.subplots(1,1)
    plotax.imshow(game_state.board[:,:,0], cmap='gray', vmin=-1, vmax=1)
    stone_array = np.array(list(self.stones)).T
    plotax.scatter(stone_array[1,:],stone_array[0,:])
    if self.liberties:
      liberties_array = np.array(list(self.liberties)).T
      plotax.scatter(liberties_array[1,:],liberties_array[0,:])
    plotax.set_xticks(np.arange(0, 9))
    plotax.set_yticks(np.arange(0, 9))
    plotax.tick_params(labeltop=True, labelright=True, length=0)
    plotax.set_yticklabels(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'][:9])
    plotax.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9'])

def testshow():
  game_state = GameState()
  game_state.randomize()
  group = Group(game_state, (3,3))
  group.show(game_state)

if __name__ == "__main__":
  testshow()
  plt.show()