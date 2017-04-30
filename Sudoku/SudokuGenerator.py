import numpy as np
from timeit import default_timer as timer
# import cProfile
# 11% put ndarray


def verify_sequence(sequence):  # 20%, sorted: 9%
    return sorted(list(sequence)) == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def verify_grid(matrix2d):  # 12%, apply_along_axis: 19%, extend: 9%
    if False in np.apply_along_axis(verify_sequence, axis=1, arr=matrix2d):  # rows
        return False
    elif False in np.apply_along_axis(verify_sequence, axis=0, arr=matrix2d):  # columns
        return False
    # if False in np.apply_over_axes(verify_sequence, matrix2d, [0, 1]):
    #     return False
    else:
        chunks = []
        for column in range(3, 10, 3):
            for row in range(0, 9, 3):
                buffer = []
                for i in matrix2d[row:row + 3, column - 3:column]:
                    buffer.extend(i)
                chunks.append(buffer)

        result_chunks = []
        for chunk in chunks:
            result_chunks.append(verify_sequence(chunk))
        if False in result_chunks:
            return False
        else:
            return True


def create_random_grid(matrix2d):  # permutation: 5%
    global NB_RANDOM_GRID_GENERATED
    NB_RANDOM_GRID_GENERATED += 1
    random_grid = np.random.permutation(matrix2d)
    while verify_grid(random_grid) is False:
        NB_RANDOM_GRID_GENERATED += 1
        random_grid = np.random.permutation(matrix2d)
    return random_grid


def run():
    start = timer()
    global NB_VALID_GRID
    global GRID
    for i in range(NB_VALID_GRID):
        create_random_grid(GRID)
    return timer() - start

NB_RANDOM_GRID_GENERATED = 0
NB_VALID_GRID = 100
GRID = np.array([[9, 4, 5, 2, 3, 7, 6, 8, 1], [1, 2, 6, 8, 4, 9, 5, 7, 3], [8, 3, 7, 1, 6, 5, 4, 2, 9],
                 [7, 6, 4, 5, 9, 8, 3, 1, 2], [2, 8, 3, 4, 7, 1, 9, 5, 6], [5, 1, 9, 6, 2, 3, 8, 4, 7],
                 [4, 7, 1, 3, 8, 6, 2, 9, 5], [6, 5, 2, 9, 1, 4, 7, 3, 8], [3, 9, 8, 7, 5, 2, 1, 6, 4]])

# cProfile.run('run()')
# runtime = 5
runtime = run()

print("Runtime: {}".format(runtime))
print("Number of valid grid generated: {}".format(NB_VALID_GRID))
print("Number of random grid generated: {}".format(NB_RANDOM_GRID_GENERATED))
print("Number of random grid generated / number of valid grid: {}".format(NB_RANDOM_GRID_GENERATED / NB_VALID_GRID))
print("\nPerformance:")
print("\t- Number of valid grid generated per seconds: {}".format(NB_VALID_GRID / runtime))
print("\t- Number of random grid generated per seconds: {}".format(NB_RANDOM_GRID_GENERATED / runtime))
