from WorldBoard import WorldBoard


def game_loop(board_size, initial_populations):
    board = WorldBoard(board_size=board_size)
    board.spawn_all_entities(initial_populations)
    board.plot_world()
    while True:
        board.step()
        board.plot_world()


if __name__ == "__main__":
    # initial conditions
    board_size = (100, 100)

    initial_spawns = dict(grass=10, pig=10, fox=1)

    game_loop(board_size, initial_spawns)
