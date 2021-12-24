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


# @numba.njit
def generate_self_distance_identity_array(self_distances, animal_position_indices):
    for animal_position_index in animal_position_indices:
        self_distances[animal_position_index[0], animal_position_index[1]] = np.inf
    return self_distances


# @numba.njit(fastmath=True, parallel=True, boundscheck=False, inline="always")
def calculate_all_distance_between_animals_and_points_vectorized(
    animal_positions: ndarray,
    positions: ndarray,
    board_size: ndarray,
    animal_position_indices: ndarray,
):
    # pythran export calculate_all_distance_between_animals_and_points(float [][], float [][], float [], int [][])
    tiled_positions = np.tile(positions, (animal_positions.shape[0], 1, 1)).swapaxes(
        0, 1
    )
    tiles_animal_positions = np.tile(animal_positions, (positions.shape[0], 1, 1))
    x_abs = np.abs(tiled_positions[:, :, 0] - tiles_animal_positions[:, :, 0])
    x_distance = np.minimum(x_abs, board_size[0] - x_abs)
    y_abs = np.abs(tiled_positions[:, :, 1] - tiles_animal_positions[:, :, 1])
    y_distance = np.minimum(y_abs, board_size[1] - y_abs)
    all_distances = np.sqrt(x_distance ** 2 + y_distance ** 2).swapaxes(0, 1)
    self_distances = np.zeros(shape=(all_distances.shape[1], all_distances.shape[1]))
    self_distances = self_distances[self_distances.shape[0] - all_distances.shape[0] :]
    self_distances = generate_self_distance_identity_array(
        self_distances, animal_position_indices
    )
    all_distances = all_distances + self_distances
    return all_distances


# @numba.njit(fastmath=True, parallel=True, boundscheck=False, inline="always")
def calculate_all_distance_between_animals_and_points(
    animal_positions: ndarray, positions: ndarray, board_size: ndarray
):
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


def calculate_all_nearest_ids_to_entity_vectorized(
    animal_entity_ids: ndarray,
    entity_ids: ndarray,
    all_distances: ndarray,
    entity_class_ids: ndarray,
    area_radiuses: ndarray,
) -> ndarray:
    nearest_entity_ids_per_entity_class = np.zeros(
        (animal_entity_ids.shape[0], 1 + entity_class_ids.max()), dtype=np.int64
    )
    nearest_distances_per_entity_class = np.zeros(
        (animal_entity_ids.shape[0], 1 + entity_class_ids.max()), dtype=np.float64
    )
    nearest_entity_ids_per_entity_class[:, 0] = animal_entity_ids
    for entity_class_id in set(entity_class_ids):
        indices = entity_class_ids == entity_class_id
        distances = all_distances[:, indices]
        # distances[distances == 0] = np.inf
        ids = entity_ids[indices]
        nearest_distances = np.min(distances, axis=1)
        not_in_radius = nearest_distances > area_radiuses
        nearest_ids_indices = np.argmin(distances, axis=1)
        nearest_ids = ids[nearest_ids_indices]
        nearest_ids[not_in_radius] = 0
        nearest_entity_ids_per_entity_class[:, entity_class_id] = nearest_ids
        nearest_distances_per_entity_class[:, entity_class_id] = nearest_distances
    return nearest_entity_ids_per_entity_class, nearest_distances_per_entity_class
