import math

# import numba
import numpy as np
from numpy import ndarray


# @numba.njit(fastmath=True, boundscheck=False, inline="always")
def distance_between_points(point_1: ndarray, point_2: ndarray, board_size: ndarray):
    # pythran export distance_between_points(float [], float [], float [])
    """
    Calculates the distance between two points on the board.
    Taking into account wrapping around the board
    :param point_1:
    :param point_2:
    :param board_size:
    :return:
    """
    abs_diff_0 = abs(point_1[0] - point_2[0])
    abs_diff_1 = abs(point_1[1] - point_2[1])

    x_distance = min(abs_diff_0, board_size[0] - abs_diff_0)
    y_distance = min(abs_diff_1, board_size[1] - abs_diff_1)
    distance = math.sqrt(x_distance ** 2 + y_distance ** 2)
    return distance


# @numba.njit(fastmath=True, boundscheck=False, inline="always")
def angle_between(position_1, position_2) -> float:
    # pythran export angle_between(float [], float [])
    """
    Calculates the angle to the position
    :param position:
    :return:
    """
    x_diff = position_1[0] - position_2[0]
    y_diff = position_1[1] - position_2[1]
    angle = rad2deg(math.atan2(y_diff, x_diff))
    return angle


# @numba.njit(fastmath=True, boundscheck=False, inline="always")
def deg2rad(x: float) -> float:
    # pythran export deg2rad(float)
    return x * math.pi / 180.0


# @numba.njit(fastmath=True, boundscheck=False, inline="always")
def rad2deg(x: float) -> float:
    # pythran export rad2deg(float)
    return x * 180.0 / math.pi


# @numba.njit(fastmath=True, boundscheck=False, inline="always")
def correct_boundaries(new_position: ndarray, board_size: ndarray) -> ndarray:
    # pythran export correct_boundaries(float [], float [])
    """
    Checks if the new position is valid
    Ensures it wraps the position
    :param new_position:
    :param board_size:
    :return:
    """
    if new_position[0] < 0:
        new_position[0] = board_size[0] - 1
    elif new_position[0] >= board_size[0]:
        new_position[0] = 0
    if new_position[1] < 0:
        new_position[1] = board_size[1] - 1
    elif new_position[1] >= board_size[1]:
        new_position[1] = 0
    return new_position


# @numba.njit(fastmath=True, boundscheck=False, inline="always")
def distance_between_points_vectorized(
        entity_position: ndarray, positions: ndarray, board_size: ndarray
) -> ndarray:
    # pythran export distance_between_points_vectorized(float [], float [][], float [])
    abs_diff = np.abs(positions - entity_position)

    x_distance = np.minimum(abs_diff[:, 0], board_size[0] - abs_diff[:, 0])
    y_distance = np.minimum(abs_diff[:, 1], board_size[1] - abs_diff[:, 1])

    distances = np.sqrt(x_distance ** 2 + y_distance ** 2)
    return distances


# @numba.njit(fastmath=True, parallel=True, boundscheck=False, inline="always")
def calculate_all_distance_between_animals_and_points(animal_positions: ndarray, positions: ndarray,
                                                      board_size: ndarray):
    # pythran export calculate_all_distance_between_animals_and_points(float [][], float [][], float [])
    all_distances = np.zeros(shape=(animal_positions.shape[0], positions.shape[0]))

    # omp parallel for
    for animal_index in range(animal_positions.shape[0]):
        animal_pos = animal_positions[animal_index]
        for other_index in range(positions.shape[0]):
            other_pos = positions[other_index]
            dist = distance_between_points(animal_pos, other_pos, board_size)
            all_distances[animal_index, other_index] = dist
    return all_distances


# @numba.njit(fastmath=True, parallel=True, boundscheck=False, inline="always")
def calculate_all_distance_between_points(positions: ndarray, board_size: ndarray):
    # pythran export calculate_all_distance_between_points(float [][], float [])
    all_distances = np.zeros(shape=(positions.shape[0], positions.shape[0]))

    # omp parallel for
    for i in range((positions.shape[0] // 2) + 1):
        for j in range(positions.shape[0]):
            if i == j:
                # all_distances[i, j] = 0
                continue
            pos_1 = positions[i]
            pos_2 = positions[j]
            dist = distance_between_points(pos_1, pos_2, board_size)
            all_distances[i, j] = dist
            all_distances[j, i] = dist
    return all_distances
