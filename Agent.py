

import tensorflow as tf
from tensorflow import keras
import numpy as np
from numpy.random import default_rng
rng = default_rng()

from GameState import GameState
from GameStates import GameStates
from Analyzer import Analyzer


class Agent:
    def __init__(self, weights=None):
      if weights == None:
        self.model = self.makeModel()
      else:
        self.model = self.makeModel(weights)

    def makeModel(self, weights=None):
      inputLayer = keras.Input(shape=(9,9,2))
      x = keras.layers.Conv2D(80, kernel_size=(3,3), activation='relu', input_shape=(9,9,2))(inputLayer)
      x = keras.layers.Conv2D(80, kernel_size=(3,3), activation='relu')(x)
      x = keras.layers.Conv2D(80, kernel_size=(3,3), activation='relu')(x)
      x = keras.layers.Conv2D(80, kernel_size=(3,3), activation='relu')(x)
      x = keras.layers.Flatten()(x)
      x = keras.layers.Dense(50, activation='relu')(x)
      x = keras.layers.Dense(50, activation='relu')(x)
      x = keras.layers.Dense(1)(x)
      model = keras.Model(inputLayer, x)
      if not (weights is None):
        model.set_weights(weights) 
      return model

    def findBestMove(self, gameStates):
      boardStack = tf.convert_to_tensor(gameStates.boardStack[0:gameStates.boardCount], dtype=tf.int8)
      scores = self.model(boardStack, training=False)
      captureScores = np.array([gameState.whiteStonesCaptured - gameState.blackStonesCaptured for gameState in gameStates.stateStack[0:gameStates.boardCount]])
      print(scores,captureScores)
      scores = np.add(scores[:,0], captureScores)
      # print(scores)
      return np.argmax(scores)
    
    def procreate(self, n_children=16, variance=.1):
      weights = self.model.get_weights()
      randomizer = lambda x: rng.normal(x, np.full(x.shape, variance))
      children = []
      for _ in range(n_children):
        randomized_weights = [randomizer(weights_layer) for weights_layer in weights]
        agent = Agent(randomized_weights)
        children.append(agent)
      return children
    
    def __str__(self):
      return f"Agent with weights[0:20]: {self.model.get_weights()[:2][0]}"

def testAgent():
  game_state = GameState()
  game_state.randomize()
  game_states = GameStates()
  analyzer = Analyzer()
  analyzer.findPossibleMoves(game_state, game_states)
  agent = Agent()
  print(agent.findBestMove(game_states))
# testAgent()

def testProcreate():
  agent = Agent()
  children = agent.procreate()
  print(list(map(str, children)))

if __name__ == "__main__":
  testAgent()
  testProcreate()