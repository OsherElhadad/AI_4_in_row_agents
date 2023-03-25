# import required module
import os
import numpy as np
import util
from connect4 import GameState


def readFile(file):
    file1 = open(file)
    Lines = file1.readlines()

    count = 0
    board = []
    # Strips the newline character
    for line in Lines:
        count += 1

        if count ==1:
            depth = int(line.strip())
        if count == 2:
            agentName = line.strip()
        if count == 3:
            row_column = line.strip().split(',')
            row = int(row_column[0])
            column = int(row_column[1])
        if count == 4:
            result = int(line.strip())
        if count >= 5 and count < row+5:
            l = line.strip().split(',')
            board.append([int(i) for i in l])

    return depth,agentName,np.array(board),result

def startTest(depth,agentName,board):
    agentType = util.loadAgent(agentName)
    agent = agentType(**{"depth": depth})
    state = GameState()
    state.set_board_AIturn(board)

    col = agent.getAction(state)
    return col

    print(col)

if __name__ == '__main__':

    # assign directory
    directory = 'test_yourself'

    # iterate over files in
    # that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            depth, agentName, board, result = readFile(f)
            studentResult = startTest(depth, agentName, board)

            if result == studentResult:
                print("Test file:   ***"+f.split('\\')[1] + "***   Good! :)")
            else:
                print("Test file:   ***"+f.split('\\')[1] + "***   Something went wromg... ")
