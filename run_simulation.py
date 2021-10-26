from WorldBoard import WorldBoard


def game_loop(board_size, initial_spawns):
    board = WorldBoard(size=board_size)
    board.spawn_plants(number_to_spawn=initial_spawns["grass"])
    board.spawn_pigs(number_to_spawn=initial_spawns["pigs"])
    board.spawn_foxes(number_to_spawn=initial_spawns["foxes"])
    while True:
        print()
        print(board)
        board.move_foxes()
        i = 0


if __name__ == '__main__':
    # initial conditions
    board_size = (10, 10)

    initial_spawns = dict(
        grass=10,
        pigs=5,
        foxes=2
    )

    game_loop(board_size, initial_spawns)
