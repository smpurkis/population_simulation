from WorldBoard import WorldBoard


def game_loop(board_size, initial_populations):
    """
    Create the World Board, spawn the entities and run the simulation.
    :param board_size:
    :param initial_populations:
    :return:
    """
    board = WorldBoard(
        board_size=board_size, show_plot=True, initial_populations=initial_populations
    )
    board.run()


if __name__ == "__main__":
    # initial conditions
    board_size = (60.0, 60.0)

    initial_spawns = dict(grass=10, pig=10, fox=1)

    game_loop(board_size, initial_spawns)
