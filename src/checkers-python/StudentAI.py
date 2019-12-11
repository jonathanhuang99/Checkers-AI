
from BoardClasses import Move
from BoardClasses import Board
import math
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():
    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
        self.maxKingCounter = 0
        self.minKingCounter = 0
        self.turnCounter = 0
        self.aiDepth = 4

    # turn = true, means it is our turn    
    def count_pieces(self):
##        if(self.color == 1):
##            return  (3*(self.board.white_count - self.board.black_count)) + (self.maxKingCounter - self.minKingCounter)
##        else:
##            return (3*(self.board.black_count - self.board.white_count)) + (self.maxKingCounter - self.minKingCounter)
        black_count = 0
        white_count = 0

        for x in range(self.row):
            for y in range(self.col):
                checker_piece = self.board.board[x][y]
                if(checker_piece.color == 'B'):
                    if(checker_piece.is_king):
                        black_count += 5 + self.row + 2 + (self.row - x)
                    else:
                        black_count += 5 + x
                elif(checker_piece.color == 'W'):
                    if (checker_piece.is_king):
                        white_count += 5 + self.row + 2 + x
                    else:
                        white_count += 5 + (self.row - x - 1)
        if(self.color == 1):
            #our ai is black count
            return black_count - white_count
        return white_count - black_count

    def is_king_helper(self, coord):
        return self.board.board[coord[0]][coord[1]].is_king
        
    # takes in a move object, returns int array coordinate rep
    def return_move_coord(self, move):
        moves = str(move).split("-")
        finalMove = moves[len(moves) - 1]
        finalMove = finalMove.strip('()')
        strRepOfCoords = finalMove.split(",")
        intRepOfCoords = [ int(strRepOfCoords[0]), int(strRepOfCoords[1]) ]
        return intRepOfCoords

    # edge case heuristic
    def edge_case_heuristic(self, coord):
        if(coord[0] == 0 or coord[0] == self.board.row or coord[1] == 0 or coord[1] == self.board.col):
            return True

    def minimax(self,move, depth, turn, alpha, beta):
        if depth == 0:
            return self.count_pieces()
        elif turn == True: # our turn
            maxValue = -9999
            moves = self.board.get_all_possible_moves(self.color)
            for i in range(len(moves)):
                for j in range(len(moves[i])):
                    # move + preliminary variables
                    action = moves[i][j]
                    self.board.make_move(action, self.color)

                    # call recursive minimax and obtain value of alpha
                    currMax = self.minimax(action, depth - 1, not turn, alpha, beta)
                    maxValue = max(currMax, maxValue)
                    alpha = max(alpha, maxValue)

                    self.board.undo()

                    #prune
                    if(beta <= alpha):
                        break   
            return maxValue
        else: # looking for min
            minValue = 9999
            moves = self.board.get_all_possible_moves(self.opponent[self.color])
            for i in range(len(moves)):
                for j in range(len(moves[i])):

                    # move + preliminary variables
                    action = moves[i][j]
                    self.board.make_move(action, self.opponent[self.color])

                    # call recursive minimax and obtain value of beta
                    currMin = self.minimax(action, depth - 1, not turn, alpha, beta)
                    minValue = min(currMin, minValue)
                    beta = min(beta, minValue)

                    self.board.undo()

                    #prune
                    if(beta <= alpha):
                        break
            return minValue
            

    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)
        totalMax = -9999
        if(len(moves) == 0 or len(moves[0]) == 0):
            return
        maxMove = moves[0][0]
        currAlpha = -9999
        for i in range(len(moves)):
            for j in range(len(moves[i])):
                move = moves[i][j]
                self.board.make_move(move, self.color)
                if(self.row == 7 and self.col == 7):
                    newDepth = self.aiDepth + math.floor(self.turnCounter/2)
                    if(newDepth > 8):
                        newDepth = 9
                    currMax = self.minimax(move, newDepth, False, currAlpha, 9999)
                else:
                    currMax = self.minimax(move, 5, False, currAlpha, 9999)
                self.board.undo()
                currAlpha = max(currMax, currAlpha)
                if currMax > totalMax:
                    totalMax = currMax
                    maxMove = move
                

        
        self.board.make_move(maxMove,self.color)
        self.turnCounter += 1
        return maxMove
    
