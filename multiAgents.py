"""
Introduction to Artificial Intelligence, 89570, Bar Ilan University, ISRAEL

Student name: Osher Elhadad
Student ID: 318969748

"""

# multiAgents.py
# --------------
# Attribution Information: part of the code were created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# http://ai.berkeley.edu.
# We thank them for that! :)


import random, util, math
import sys

import gameUtil as u

from connect4 import Agent


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 1 # agent is always index 1
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class BestRandom(MultiAgentSearchAgent):

    def getAction(self, gameState):

        return gameState.pick_best_move()


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 1)
    """

    def minimax(self, gameState, depth):
        if gameState.is_terminal() or depth == 0:
            return -1, self.evaluationFunction(gameState)
        children = gameState.getLegalActions(gameState.turn)
        if gameState.turn == u.AI:

            # Minimum integer value
            cur_max = ~sys.maxsize
            max_action = -1
            for child in children:
                newGameState = gameState.generateSuccessor(gameState.turn, child)
                newGameState.switch_turn(gameState.turn)

                # Recursive call with new state (next turn) and with max_depth - 1
                _, v = self.minimax(newGameState, depth - 1)

                # Switch cur_max to be the new max- v, and save its action
                if v > cur_max:
                    cur_max = v
                    max_action = child
            return max_action, cur_max
        else:

            # Maximum integer value
            cur_min = sys.maxsize
            min_action = -1
            for child in children:
                newGameState = gameState.generateSuccessor(gameState.turn, child)
                newGameState.switch_turn(gameState.turn)

                # Recursive call with new state (next turn) and with max_depth - 1
                _, v = self.minimax(newGameState, depth - 1)

                # Switch cur_min to be the new min- v, and save its action
                if v < cur_min:
                    cur_min = v
                    min_action = child
            return min_action, cur_min

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.isWin():
        Returns whether or not the game state is a winning state for the current turn player

        gameState.isLose():
        Returns whether or not the game state is a losing state for the current turn player

        gameState.is_terminal()
        Return whether or not that state is terminal
        """

        best_action, _ = self.minimax(gameState, self.depth)
        return best_action


class AlphaBetaAgent(MultiAgentSearchAgent):

    def bestValue(self, gameState, depth, alpha, beta):
        if gameState.is_terminal() or depth == 0:
            return -1, self.evaluationFunction(gameState)
        if gameState.turn == u.AI:
            return self.maxValue(gameState, depth, alpha, beta)
        return self.minValue(gameState, depth, alpha, beta)

    def maxValue(self, gameState, depth, alpha, beta):

        # Minimum integer value
        cur_max = ~sys.maxsize
        max_action = -1
        for child in gameState.getLegalActions(gameState.turn):
            newGameState = gameState.generateSuccessor(gameState.turn, child)
            newGameState.switch_turn(gameState.turn)

            # Recursive call with new state (next turn) and with max_depth - 1
            _, v = self.bestValue(newGameState, depth - 1, alpha, beta)

            # Switch cur_max to be the new max- v, and save its action
            if v > cur_max:
                cur_max = v
                max_action = child
            if cur_max > beta:
                return max_action, cur_max
            alpha = max(alpha, cur_max)
        return max_action, cur_max


    def minValue(self, gameState, depth, alpha, beta):

        # Minimum integer value
        cur_min = sys.maxsize
        min_action = -1
        for child in gameState.getLegalActions(gameState.turn):
            newGameState = gameState.generateSuccessor(gameState.turn, child)
            newGameState.switch_turn(gameState.turn)

            # Recursive call with new state (next turn) and with max_depth - 1
            _, v = self.bestValue(newGameState, depth - 1, alpha, beta)

            # Switch cur_min to be the new min- v, and save its action
            if v < cur_min:
                cur_min = v
                min_action = child
            if cur_min < alpha:
                return min_action, cur_min
            beta = min(beta, cur_min)
        return min_action, cur_min


    def getAction(self, gameState):
        """
            Your minimax agent with alpha-beta pruning (question 2)
        """
        best_action, _ = self.bestValue(gameState, self.depth, ~sys.maxsize, sys.maxsize)
        return best_action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 3)
    """

    def bestVal(self, gameState, depth):
        if gameState.is_terminal() or depth == 0:
            return -1, self.evaluationFunction(gameState)
        if gameState.turn == u.AI:
            return self.maxVal(gameState, depth)
        return self.expVal(gameState, depth)


    def maxVal(self, gameState, depth):

        # Minimum integer value
        cur_max = ~sys.maxsize
        max_action = -1
        for child in gameState.getLegalActions(gameState.turn):
            newGameState = gameState.generateSuccessor(gameState.turn, child)
            newGameState.switch_turn(gameState.turn)

            # Recursive call with new state (next turn) and with max_depth - 1
            _, v = self.bestVal(newGameState, depth - 1)

            # Switch cur_max to be the new max- v, and save its action
            if v > cur_max:
                cur_max = v
                max_action = child
        return max_action, cur_max


    def expVal(self, gameState, depth):
        total = 0

        # Uniform probability
        probability = 1.0 / len(gameState.getLegalActions(gameState.turn))
        for child in gameState.getLegalActions(gameState.turn):
            newGameState = gameState.generateSuccessor(gameState.turn, child)
            newGameState.switch_turn(gameState.turn)

            # Recursive call with new state (next turn) and with max_depth - 1
            _, v = self.bestVal(newGameState, depth - 1)
            total += probability * v
        return _, total


    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction
        """
        best_action, _ = self.bestVal(gameState, self.depth)
        return best_action
