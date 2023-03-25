import numpy as np

import random, util
import gameUtil as u
import graphics as g

class Agent:
    """
    An agent must define a getAction method, but may also define the
    following methods which will be called if they exist:

    def registerInitialState(self, state): # inspects the starting state
    """

    def __init__(self, index=0):
        self.index = index

    def getAction(self, state, piece):
        """
        The Agent will receive a GameState and piece and must return an action
        """
        util.raiseNotDefined()

class GameStateData:

    def __init__(self, prevState=None):
        """
        Generates a new data packet by copying information from its predecessor.
        """
        if prevState == None:
            self._agentMoved = None
            self._lose = False
            self._win = False
            self.scoreChange = 0

    def deepCopy(self):
        state = GameStateData(self)
        state._agentMoved = self._agentMoved
        state._capsuleEaten = self._capsuleEaten
        return state

    def copyAgentStates(self, agentStates):
        copiedStates = []
        for agentState in agentStates:
            copiedStates.append(agentState.copy())
        return copiedStates


    def initialize(self):
        """
        Creates an initial game state from a layout array (see layout.py).
        """
        self.agentStates = []

class GameState:
    # static variable keeps track of which states have had getLegalActions called
    explored = set()

    def __init__(self, prevState=None):
        """
        Generates a new state by copying information from its predecessor.
        """
        if prevState != None:  # Initial state
            self.data = GameStateData(prevState.data)
            self.board = prevState.board.copy()
            self.turn = prevState.turn
        else:
            self.data = GameStateData()
            self.board = self.create_board()
            self.turn = random.randint(u.PLAYER, u.AI)

    def set_board_AIturn(self, board):
        self.board = board
        self.turn = u.AI

    def create_board(self):
        '''
        create the board game and return it
        '''
        board = np.zeros((u.ROW_COUNT, u.COLUMN_COUNT))
        return board

    def getAndResetExplored():
        tmp = GameState.explored.copy()
        GameState.explored = set()
        return tmp

    getAndResetExplored = staticmethod(getAndResetExplored)

    def getLegalActions(self, agentIndex=0):
        """
        Returns the legal actions for the agent specified.
        """
        actions = []
        if not self.isWin() and not self.isLose():
            for col in range(u.COLUMN_COUNT):
                if(self.is_valid_location(col)):
                    actions.append(col)
        return actions

    def get_piece_player(self):
        '''
        return: the current player piece
        '''
        if self.turn == 0:
            return u.PLAYER_PIECE
        return u.AI_PIECE


    def winning(self, piece):
        # Check horizontal locations for win
        for c in range(u.COLUMN_COUNT - 3):
            for r in range(u.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and self.board[r][c + 2] == piece and \
                        self.board[r][
                            c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(u.COLUMN_COUNT):
            for r in range(u.ROW_COUNT - 3):
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and self.board[r + 2][c] == piece and \
                        self.board[r + 3][
                            c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(u.COLUMN_COUNT - 3):
            for r in range(u.ROW_COUNT - 3):
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and self.board[r + 2][
                    c + 2] == piece and \
                        self.board[r + 3][
                            c + 3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(u.COLUMN_COUNT - 3):
            for r in range(3, u.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and self.board[r - 2][
                    c + 2] == piece and \
                        self.board[r - 3][
                            c + 3] == piece:
                    return True

        return False

    def isWin(self):
        '''Return is the current player is winning'''
        return self.winning(self.get_piece_player())

    def isLose(self):
        '''Return is the opponent player is winning'''
        return self.winning(self.get_opp_piece(self.get_piece_player()))

    def is_terminal(self):
        '''
        Return whether or not that state is terminal
        '''
        return self.isWin() or self.isLose() or len(self.getLegalActions()) == 0

    def pick_best_move(self):

        best_score = -10000
        valid_location = self.getLegalActions()
        best_col = random.choice(valid_location)
        for col in valid_location:
            temp_state = self.generateSuccessor(self.get_piece_player(), col)
            score = temp_state.getScore()
            if score > best_score:
                best_score = score
                best_col = col

        return best_col

    def evaluate_window(self, window, piece):
        '''
        Evaluate the chance of winning for thae specific piece in window in size 4
        '''
        score = 0
        opp_piece = self.get_opp_piece(piece)

        if window.count(piece) == 4:
            score += 1000
        elif window.count(piece) == 3 and window.count(u.EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(u.EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(u.EMPTY) == 1:
            score -= 4
        if window.count(opp_piece) == 4:
            score -= 1000
        return score

    def getScore(self):
        '''
        :return: score of the board for the current player
        '''
        score = 0
        piece = self.get_piece_player()
        ## Score center column
        center_array = [int(i) for i in list(self.board[:, u.COLUMN_COUNT // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(u.ROW_COUNT):
            row_array = [int(i) for i in list(self.board[r, :])]
            for c in range(u.COLUMN_COUNT - 3):
                window = row_array[c:c + u.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(u.COLUMN_COUNT):
            col_array = [int(i) for i in list(self.board[:, c])]
            for r in range(u.ROW_COUNT - 3):
                window = col_array[r:r + u.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score posiive sloped diagonal
        for r in range(u.ROW_COUNT - 3):
            for c in range(u.COLUMN_COUNT - 3):
                window = [self.board[r + i][c + i] for i in range(u.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(u.ROW_COUNT - 3):
            for c in range(u.COLUMN_COUNT - 3):
                window = [self.board[r + 3 - i][c + i] for i in range(u.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    def is_valid_location(self, col):
        '''
        Return if insert a piece to the specific col is valid
        '''
        return self.board[u.ROW_COUNT-1][col] == 0

    def get_next_open_row(self, col):
        '''
        Return the first empty row in the specific col
        '''
        for r in range(u.ROW_COUNT):
            if self.board[r][col] == 0:
                return r

    def drop_piece(self, row, col, piece):
        '''
        Change the board in the current state with the action of dropping piece in the specific row,col.
        '''
        self.board[row][col] = piece

    def get_opp_piece(self, piece):
        '''
        return: the opponent player piece
        '''
        if piece == u.AI_PIECE:
            return u.PLAYER_PIECE
        return u.AI_PIECE

    def switch_turn(self, piece):
        '''
        switch the turn in the state and return the updated player turn
        '''
        self.turn = (piece +1) % 2
        return self.turn



    def generateSuccessor(self, agentIndex, action):
        """
        Returns the successor state after the specified agent takes the action.
        """
        # Copy current state
        state = GameState(self)

        row = state.get_next_open_row(action)
        piece = self.get_piece_player()
        # Let agent's logic deal with its action's effects on the board
        state.drop_piece(row, action, piece)

        # Book keeping
        state.data._agentMoved = agentIndex
        GameState.explored.add(self)
        GameState.explored.add(state)
        return state




def runGames(graphicMode, gameMode, agent):
    state = GameState()
    print(state.board)
    if graphicMode:
        g.setScreen()
        g.draw_board(state.board)

    game_over = False


    while not game_over:
        # ask for player 1 input
        if state.turn == u.PLAYER:
            if graphicMode:
                col = g.eventListener(state.turn)
                if col != None:
                    print(col)
            else:
                col = int(input("Player 1 make your selection (0-6:)"))
                print(col)

            if col != None:
                if state.is_valid_location(col):
                    state = state.generateSuccessor(u.PLAYER_PIECE, col)

                    if state.isWin():
                        if graphicMode:
                            g.winning(u.PLAYER_PIECE,u.RED)
                        else:
                            print("Player 1 wins!")
                        game_over = True

                    if not graphicMode:
                        print(state.board)

                    state.switch_turn(state.turn)
                    print("*************************************************************")

        # ask for player 2 input
        else:
            if gameMode == 2:
                if graphicMode:
                    col = g.eventListener(state.turn)
                    if col != None:
                        print(col)
                else:
                    col = int(input("Player 2 make your selection (0-6:)"))
                    print(col)
            else: #in case we use AI agent
                col = agent.getAction(state)

            if col != None:
                if state.is_valid_location(col):
                    state = state.generateSuccessor(u.AI_PIECE, col)

                    if state.isWin():
                        if graphicMode:
                            g.winning(u.AI_PIECE,u.YELLOW)
                        else:
                            print("Player 2 wins!")
                        game_over = True

                    if not graphicMode:
                        print(state.board)

                    state.switch_turn(state.turn)
                    print("*************************************************************")


        if graphicMode:
            g.draw_board(state.board)

        if (game_over):
            g.wait_to_end()






if __name__ == '__main__':
    # graphicMode - True- for graphic mode. False- for textual mode
    # gameMode  - get the value 2- for player vs. player or 1- for palyer vs. AI_agent
    # depth - the max depth to explore the minimax tree
    # type - the name of the agent will play as AI_agent (one of "BestRandom", "MinimaxAgent", "AlphaBetaAgent", "ExpectimaxAgent")

    graphicMode = True
    gameMode  = 1
    depth = 5 # must be at least 3 with different agent then Random
    type = "ExpectimaxAgent"

    agent = None
    if gameMode  == 1:
        agentType = util.loadAgent(type)
        agent = agentType(**{"depth": depth})  # Instantiate agent with agentArgs

    runGames(graphicMode, gameMode , agent)
