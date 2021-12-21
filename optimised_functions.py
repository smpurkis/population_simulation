import math

# import numba
from numpy import ndarray
import numpy as np


# @numba.njit(fastmath=True)
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


def deg2rad(x: float) -> float:
    # pythran export deg2rad(float)
    return x * math.pi / 180.0


def rad2deg(x: float) -> float:
    # pythran export rad2deg(float)
    return x * 180.0 / math.pi


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


# @numba.njit(fastmath=True, parallel=False)
def distance_between_points_parallel(
    entity_position: ndarray,
    positions: ndarray,
    board_size: ndarray,
    area_radius: float,
):
    # pythran export distance_between_points_parallel(float [], float [][], float [], float)
    distances = np.empty(shape=(positions.shape[0]), dtype=np.float32)

    # omp parallel for
    for i in range(positions.shape[0]):
        pos = positions[i]
        distances[i] = distance_between_points(entity_position, pos, board_size)
    distances_sorted = distances.argsort()
    last_index_in_radius = np.searchsorted(distances[distances_sorted], area_radius)
    return distances_sorted, last_index_in_radius


# @numba.njit(fastmath=True)
def distance_between_points_vectorized(
    entity_position: ndarray, positions: ndarray, board_size: ndarray
) -> ndarray:
    # pythran export distance_between_points_vectorized(float [], float [][], float [])
    abs_diff = np.abs(positions - entity_position)

    x_distance = np.minimum(abs_diff[:, 0], board_size[0] - abs_diff[:, 0])
    y_distance = np.minimum(abs_diff[:, 1], board_size[1] - abs_diff[:, 1])

    distances = np.sqrt(x_distance ** 2 + y_distance ** 2)
    return distances
