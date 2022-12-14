# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from curses.ascii import NUL
from os import curdir
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # print(newFood)
        x,y=newPos
        isFood=0
        if currentGameState.getFood()[x][y]: # must use currentGameState, the food is eaten in successor
            isFood=1
        
        newGhostPositions=successorGameState.getGhostPositions()
        isGhost=0
        for ghost in newGhostPositions:
            if newPos==ghost:
                isGhost=1
        disToGhosts=0
        for ghost in newGhostPositions:
            gx,gy=ghost
            disToGhosts+=abs(x-gx)+abs(y-gy)    # bigger is better
        row=newFood.height
        col=newFood.width
        minDis=9999
        for i in range(1,col-1):
            for j in range(1,row-1):
                if newFood[i][j]:
                    minDis=min(minDis,abs(x-i)+abs(y-j))
        if minDis==9999: minDis=0   # for the last food
        scare=0
        for i in newScaredTimes:
            scare+=i
        return successorGameState.getScore()+scare+isFood*300-minDis-1000*isGhost

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        v=float("-inf")
        res=None
        pacLegalActions=gameState.getLegalActions(0)
        for action in pacLegalActions:
            val=self.min_value(gameState.generateSuccessor(0,action))
            if v<val:
                v=val
                res=action
        return res

    def min_value(self,state,depth=0,agentID=1):
        v=float("inf")
        actions=state.getLegalActions(agentID)
        if depth==self.depth or len(actions)==0:
            return self.evaluationFunction(state)
        for action in actions:
            if agentID==state.getNumAgents()-1: # the last ghost
                val=self.max_value(state.generateSuccessor(agentID,action),depth+1)
            else:
                val=self.min_value(state.generateSuccessor(agentID,action),depth,agentID+1)
            v=min(v,val)
        return v

    def max_value(self,state,depth):
        v=float("-inf")
        actions=state.getLegalActions(0)
        if depth==self.depth or len(actions)==0:
            return self.evaluationFunction(state)
        for action in actions:
            val=self.min_value(state.generateSuccessor(0,action),depth)
            v=max(v,val)
        return v






class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        v=float("-inf")
        res=None
        alpha=float('-inf')
        beta=float('inf')
        pacLegalActions=gameState.getLegalActions(0)
        for action in pacLegalActions:
            val=self.min_value(gameState.generateSuccessor(0,action),0,1,alpha,beta)
            if v<val:
                v=val
                res=action
            alpha=max(v,alpha)
        return res

    def min_value(self,state,depth=0,agentID=1,alpha=float('-inf'),beta=float('inf')):
        v=float("inf")
        actions=state.getLegalActions(agentID)
        if depth==self.depth or len(actions)==0:
            return self.evaluationFunction(state)
        for action in actions:
            if agentID==state.getNumAgents()-1: # the last ghost
                val=self.max_value(state.generateSuccessor(agentID,action),depth+1,alpha,beta)
            else:
                val=self.min_value(state.generateSuccessor(agentID,action),depth,agentID+1,alpha,beta)
            v=min(v,val)
            if v<alpha:
                return v
            beta=min(beta,v)
        return v

    def max_value(self,state,depth,alpha=float('-inf'),beta=float('inf')):
        v=float("-inf")
        actions=state.getLegalActions(0)
        if depth==self.depth or len(actions)==0:
            return self.evaluationFunction(state)
        for action in actions:
            val=self.min_value(state.generateSuccessor(0,action),depth,1,alpha,beta)
            v=max(v,val)
            if v>beta:
                return v
            alpha=max(v,alpha)
        return v
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        v=float("-inf")
        res=None
        pacLegalActions=gameState.getLegalActions(0)
        for action in pacLegalActions:
            val=self.exp_value(gameState.generateSuccessor(0,action))
            if v<val:
                v=val
                res=action
        return res

    def exp_value(self,state,depth=0,agentID=1):
        v=float("inf")
        actions=state.getLegalActions(agentID)
        if depth==self.depth or len(actions)==0:
            return self.evaluationFunction(state)
        totalVal=0
        for action in actions:
            if agentID==state.getNumAgents()-1: # the last ghost
                totalVal+=self.max_value(state.generateSuccessor(agentID,action),depth+1)
            else:
                totalVal+=self.exp_value(state.generateSuccessor(agentID,action),depth,agentID+1)
        v=totalVal/len(actions)
        return v

    def max_value(self,state,depth):
        v=float("-inf")
        actions=state.getLegalActions(0)
        if depth==self.depth or len(actions)==0:
            return self.evaluationFunction(state)
        for action in actions:
            val=self.exp_value(state.generateSuccessor(0,action),depth)
            v=max(v,val)
        return v
        

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    x,y = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostPositions=currentGameState.getGhostPositions()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    scare=0
    for i in scaredTimes:
        scare+=i
    disToGhosts=0
    for ghost in ghostPositions:
        gx,gy=ghost
        disToGhosts+=abs(x-gx)+abs(y-gy)    # bigger is better
    row=food.height
    col=food.width
    minDis=9999
    for i in range(1,col-1):
        for j in range(1,row-1):
            if food[i][j]:
                minDis=min(minDis,abs(x-i)+abs(y-j))
    if minDis==9999: minDis=0   # for the last food
    return currentGameState.getScore()+scare+disToGhosts-minDis
    

# Abbreviation
better = betterEvaluationFunction
