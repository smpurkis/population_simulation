from WorldBoard import WorldBoard


def game_loop(board_size, initial_populations):
    """
    Create the World Board, spawn the entities and run the simulation.
    :param board_size:
    :param initial_populations:
    :return:
    """
    board = WorldBoard(
        board_size=board_size, initial_populations=initial_populations, show_plot=False
    )
    board.run()


if __name__ == "__main__":
    # initial conditions
    board_size = (300.0, 300.0)

    initial_spawns = dict(grass=100, pig=300, fox=2)

    game_loop(board_size, initial_spawns)
