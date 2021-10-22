from pprint import pprint

from WorldBoard import WorldBoard

if __name__ == '__main__':

    # initial conditions
    board_size = (10, 10)

    initial_grass_to_spawn = 10

    board = WorldBoard(size=board_size)
    board.spawn_plants(number_to_spawn=initial_grass_to_spawn)
    print(board)
    i = 0
