

class NeighborFinder:
  def __init__(self, boardDims):
    self.neighborLookupTable = []
    self.lookupNeighbors(boardDims)
    
  def lookupNeighbors(self, boardDims):
    dirs = [(1,0),(0,1),(-1,0),(0,-1)]
    for h in range(0, boardDims[0]):
      self.neighborLookupTable.append([])
      for v in range(0,boardDims[1]):
        self.neighborLookupTable[-1].append([])
        for dir in dirs:
          x,y = (h - dir[0], v - dir[1])
          if not (0 <= x < boardDims[0] and 0 <= y < boardDims[1]):
            pass
          else:
            self.neighborLookupTable[-1][-1].append((x,y))

if __name__ == "__main__":
    neighborFinder99 = NeighborFinder([9,9])
    print(neighborFinder99.neighborLookupTable)