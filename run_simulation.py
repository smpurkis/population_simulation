from WorldBoard import WorldBoard


def game_loop(board_size, initial_spawns):
    board = WorldBoard(board_size=board_size)
    board.spawn_plants(number_to_spawn=initial_spawns["grass"])
    board.spawn_pigs(number_to_spawn=initial_spawns["pigs"])
    board.spawn_foxes(number_to_spawn=initial_spawns["foxes"])
    board.plot_world()
    while True:
        board.step()
        board.plot_world()


if __name__ == '__main__':
    # initial conditions
    board_size = (100, 100)

    initial_spawns = dict(
        grass=20,
        pigs=5,
        foxes=2
    )

    game_loop(board_size, initial_spawns)
