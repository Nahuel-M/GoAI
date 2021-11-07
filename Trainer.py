import copy
import numpy as np

from GameState import GameState
from GameStates import GameStates
from Analyzer import Analyzer
from Agent import Agent
from Game import Game



class Trainer:
  def __init__(self, n_agents):
    self.agents = [Agent() for _ in range(n_agents)]
    self.noobs = [Agent() for _ in range(5)]
    
  def setMatches(self):
    rng.shuffle(self.agents)

  def knockoutRound(self):
    game = Game()
    if int(len(self.agents)/2) != len(self.agents)/2:
      raise Exception("Agent count not even")
    self.setMatches()
    winnerID = []
    for i in range(0,len(self.agents), 2):
      score = game.play(self.agents[i], self.agents[i+1])
      winnerID.append(i+1*(score>0))
    self.agents = list( self.agents[i] for i in winnerID)

  def playStarters(self):
    results = []
    return results

  def dethroneYourParents(self, n_children, variance):
    game = Game()
    children = [child for agent in self.agents for child in agent.procreate(n_children, variance)]
    for child in children:
      results = self.playAgents(game, child)
      results = self.calculateEffectiveScores(results)
      if sum(result > 0 for result in results) >= 2:
        self.agents[results.index(max(results))] = child
        print("Replacing agent", results.index(max(results)))
      print("Results: ", results)

  def calculateEffectiveScores(self, scores):
    def transformScore(score):
      result1, result2 = score
      return (result1 < 0 and result2 > 0) * (result2 - result1)
    return list(map(transformScore, scores))

  def playAgents(self, game, child):
    return self.playGroup(game, child, self.agents)
        
  def playGroup(self, game, player, group):
    results = []
    for agent in group:
      result1 = game.play(player, agent)
      game.gameState.reset()
      result2 = game.play(agent, player)
      score = (result1, result2)
      results.append(score)
    return results

  def calculatePerformance(self):
    game = Game()
    results = []
    for agent in self.agents:
      performance = self.playNoobs(game, agent)
      results.append(performance)
    return np.array(results).mean(axis=0).mean(axis=0)

  def playNoobs(self, game, player):
    return self.playGroup(game, player, self.noobs)

  def procreateAgents(self, children, variance):
    self.agents = [child for agent in self.agents for child in agent.procreate(children, variance)]
    # self.agents = [agent in agents for agents in self.agents]

def testKnockoutRound():
  trainer = Trainer(16)
  trainer.knockoutRound()
  print(len(trainer.agents))

# testKnockoutRound()

def testTrainer():
  trainer = Trainer(5)
  for i in range(1,100):
    print("performance:", trainer.calculatePerformance())
    print("TRAINING ROUND", i)
    trainer.dethroneYourParents(5, 0.001/(float(i)/10))
  plt.plot(scoreHistory)
  plt.show()
 
if __name__ == "__main__":
  testTrainer()