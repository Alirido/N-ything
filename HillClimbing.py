from copy import deepcopy

from ChessBoard import ChessBoard

def HillClimbingAlgorithm(chessboard):
    print('Inisialisasi')
    chessboard.printBoardInfo()
    empty_loc = EmptyLocation(chessboard)
    piece_list = Pieces(chessboard)
    successor = BestNeighbor(chessboard, empty_loc, piece_list)
    while(heuristic(successor) > heuristic(chessboard)):
        chessboard = successor
        empty_loc = EmptyLocation(chessboard)
        piece_list = Pieces(chessboard)
        successor = BestNeighbor(chessboard, empty_loc, piece_list)
    print()
    print('Hasil')
    chessboard.printBoardInfo()
    '''for row in chessboard.board:
        for bidak in row:
            if(bidak!={}):
                print(bidak)'''

def EmptyLocation(chessboard):
    empty_loc = []
    for row in range(8):
        for col in range(8):
            if(chessboard.board[row][col]=={}):
                empty_loc.append((row,col))
    return empty_loc

def Pieces(chessboard):
    piece_list = []
    for row in chessboard.board:
        for piece in row:
            if(piece!={}):
                piece_list.append(piece)
    return piece_list

def heuristic(chessboard):
    #if(chessboard.count_white_pieces() == chessboard.count_white_pieces() + chessboard.count_black_pieces()):
     #   return chessboard.countSameHeuristic()
    return chessboard.countDiffHeuristic() - chessboard.countSameHeuristic()

def BestNeighbor(chessboard, empty_loc, piece_list):
    max_heuristic = heuristic(chessboard)
    best_board = chessboard
    for piece in piece_list:
        for loc in empty_loc:
            temp_piece = deepcopy(piece)
            temp_board = deepcopy(chessboard)
            temp_board.movePiece(temp_piece, loc)
            temp_heuristic = heuristic(temp_board)
            if(temp_heuristic > max_heuristic):
                best_board = temp_board
                max_heuristic = temp_heuristic
    '''print('chessboard')
    chessboard.printBoardInfo()
    print('best_board')
    best_board.printBoardInfo()'''
    return best_board

if __name__ == '__main__':
    chess = ChessBoard('input3.txt')
    chess.randomizeBoard()
    #print('genetic algorithm')
    HillClimbingAlgorithm(chess)