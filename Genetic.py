from copy import deepcopy
from random import randint, seed, randrange
from os import urandom

from ChessBoard import ChessBoard


def geneticAlgorithm(chessboard):
    # generating the population
    init_chessboard = deepcopy(chessboard)
    fitness_string_population = []
    population_count = 6 * (chessboard.count_black_pieces + chessboard.count_white_pieces)
    for _ in range(population_count):
        chessboard.randomizeBoard()
        fitness = chessboard.countDiffHeuristic() - chessboard.countSameHeuristic()  # this is the fitness function
        fitness_string_population.append([fitness, _ChessboardToString(chessboard.board)])
    # sort the inviiduals based on fitness function
    fitness_string_population = sorted(fitness_string_population, key=lambda x: x[0], reverse=True)

    # start of genetic algorithm iteration
    fittest_individual = fitness_string_population[0]
    fittest_count = 1

    iteration = 1

    # start of iteration of genetic algorithm
    while fittest_count < (population_count*3):
        print('iteration', iteration)
        iteration += 1
        print('fittest individual:', fittest_individual)
        print('fittest count:', fittest_count)
        fitness_string_population = _GeneticMutation(fitness_string_population)
        for i in range(len(fitness_string_population)):
            fitness_string_population[i] = [_fitnessFunction(fitness_string_population[i], deepcopy(init_chessboard)), fitness_string_population[i]]
        # sort the inviiduals based on fitness function
        fitness_string_population = sorted(fitness_string_population, key=lambda x: x[0], reverse=True)
        print()

        # checking whether the result have become convergent or not
        if fittest_individual[0] <= fitness_string_population[0][0]:
            if fittest_individual[0] == fitness_string_population[0][0]:
                fittest_count += 1
            else:
                fittest_count = 0
            fittest_individual = fitness_string_population[0]
        else:
            fittest_count += 1

    return _translateBoardWithFinalResult(fittest_individual[1], init_chessboard)

def _ChessboardToString(board):
    piece_arr = []
    for row in board:
        for piece in row:
            if piece != {}:
                loc_str = str(piece['location'][0]) + str(piece['location'][1])
                piece_arr.append([piece['id'], loc_str])
    piece_arr = sorted(piece_arr, key=lambda p: p[0])
    return ''.join([i[1] for i in piece_arr])


def _GeneticMutation(fitness_string):
    """
    the iterative steps of genetic algorithm
    """

    # selecting mates
    str_couples = []
    while fitness_string != []:
        seed(urandom(100))
        if len(fitness_string) > 2:
            index_1 = randint(0, len(fitness_string) - 1)
            index_2 = randint(0, len(fitness_string) - 1)
            while index_1 == index_2:
                index_1 = randint(0, len(fitness_string) - 1)
                index_2 = randint(0, len(fitness_string) - 1)
        else:
            index_1 = 0
            index_2 = 1
        string_1 = fitness_string[index_1]
        string_2 = fitness_string[index_2]
        str_couples.append([string_1[1], string_2[1]])
        fitness_string.remove(string_1)
        fitness_string.remove(string_2)

    string_length = len(str_couples[0][0])
    string_result = []
    # split and cross
    for i in range(len(str_couples)):
        seed(urandom(100))
        split_index = randrange(2, string_length-2, 2)  # choose split position
        substring_1 = str_couples[i][0][:split_index]
        substring_2 = str_couples[i][1][:split_index]
        string_result.append(substring_2 + str_couples[i][0][split_index:])
        string_result.append(substring_1 + str_couples[i][1][split_index:])

    # mutation
    for i in range(len(string_result)):
        seed(urandom(100))
        probability = randint(1, 10)
        if probability < 4:  # probability of mutation = 0.4
            str_temp = list(string_result[i])
            str_temp[randint(0, len(str_temp) - 1)] = str(randint(0, 7))
            str_temp = ''.join(str_temp)
            while not(_isStringUnique(str_temp)) and (probability < 4):
                str_temp = list(string_result[i])
                str_temp[randint(0, len(str_temp) - 1)] = str(randint(0, 7))
                str_temp = ''.join(str_temp)
                probability = randint(1, 10)
            if probability < 4:
                string_result[i] = str_temp

    # return the modified strings
    return string_result


def _isStringUnique(string):
    str_arr = [string[i:i + 2] for i in range(0, len(string), 2)]
    for i in range(len(str_arr)-1):
        for j in range(i+1, len(str_arr)):
            if str_arr[i] == str_arr[j]:
                return False
    return True


def _fitnessFunction(string, chessboard):
    # print('FITNESS FUNCTION')
    # print('string:', string)
    board_temp = deepcopy(chessboard)
    amount_of_piece = chessboard.count_white_pieces + chessboard.count_black_pieces
    for piece_id in range(amount_of_piece):
        # chessboard.printBoardInfo()
        # print('id', piece_id)
        row = int(string[piece_id * 2])
        col = int(string[piece_id * 2 + 1])
        piece = board_temp.findPieceById(piece_id)
        chessboard.movePiece(piece, (row, col))
    return chessboard.countDiffHeuristic() - chessboard.countSameHeuristic()

def _translateBoardWithFinalResult(string, chessboard):
    board_temp = deepcopy(chessboard)
    amount_of_piece = chessboard.count_white_pieces + chessboard.count_black_pieces
    for piece_id in range(amount_of_piece):
        # chessboard.printBoardInfo()
        # print('id', piece_id)
        row = int(string[piece_id * 2])
        col = int(string[piece_id * 2 + 1])
        piece = board_temp.findPieceById(piece_id)
        chessboard.movePiece(piece, (row, col))
    return chessboard

if __name__ == '__main__':
    chess = ChessBoard('n-queen.txt')

    print('genetic algorithm')
    geneticAlgorithm(chess).printBoardInfo()

