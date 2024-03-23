"""
Author: Parisa Arbab
Date: March 12, 2024,
Statement:“I have not given or received any unauthorized assistance on this assignment.”
YouTube Link: https://youtu.be/0nG01hJcnfc

answered this question in the above link:
• Show how you created the NumPy array.
• Show your logic in updating the board.
• Which values for s and p did you find to create an interesting colony of cells.
"""


import numpy as np
import random

def conway(s, p=0.1):
    """
    Generates a square two-dimensional NumPy array representing the Conway board.

    Parameters:
    - s (int): Size of the board (s x s).
    - p (float): Probability of a cell being alive initially (default is 0.1).

    Returns:
    - board (numpy.ndarray): The generated Conway board.
    """
    # Initialize an empty board filled with zeros
    board = np.zeros((s, s), dtype=int)

    # Determine the total number of cells that should be alive
    num_live_cells = int(s * s * p)

    # Randomly select num_live_cells cells to be alive
    live_cells_indices = random.sample(range(s * s), num_live_cells)
    for index in live_cells_indices:
        i = index // s
        j = index % s
        board[i, j] = 1

    return board

def count_neighbors(board):
    """
    Counts the number of live neighbors for each cell on the board.

    Parameters:
    - board (numpy.ndarray): The Conway board.

    Returns:
    - neighbor_count (numpy.ndarray): The number of live neighbors for each cell.
    """
    # Define a kernel for counting neighbors
    kernel = np.array([[1, 1, 1],
                       [1, 0, 1],
                       [1, 1, 1]])

    # Create an empty array to store the neighbor counts
    neighbor_count = np.zeros_like(board)

    # Iterate over each cell in the board
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            # Define the boundaries for slicing
            i_start = max(0, i - 1)
            i_end = min(board.shape[0], i + 2)
            j_start = max(0, j - 1)
            j_end = min(board.shape[1], j + 2)

            # Perform the slicing operation and calculate the neighbor count
            neighbors_slice = board[i_start:i_end, j_start:j_end]
            neighbor_count[i, j] = np.sum(neighbors_slice * kernel[:i_end-i_start, :j_end-j_start])

    # Subtract the center cell value to account for self-counting
    neighbor_count -= board

    return neighbor_count


def advance(b, t):
    """
    Advances the Conway board t time steps according to the game rules.

    Parameters:
    - b (numpy.ndarray): The Conway board.
    - t (int): Number of time steps .

    Returns:
    - advanced_board (numpy.ndarray): The advanced Conway board after t time steps.
    """
    advanced_board = np.copy(b)  # Create a copy to avoid modifying the input board

    for _ in range(t):
        neighbor_count = count_neighbors(advanced_board)

        # Apply the game rules
        advanced_board = np.where((advanced_board == 1) & (neighbor_count < 2), 0, advanced_board)  # Dies from underpopulation
        advanced_board = np.where((advanced_board == 1) & ((neighbor_count == 2) | (neighbor_count == 3)), 1, advanced_board)  # Lives on
        advanced_board = np.where((advanced_board == 1) & (neighbor_count > 3), 0, advanced_board)  # Dies from overpopulation
        advanced_board = np.where((advanced_board == 0) & (neighbor_count == 3), 1, advanced_board)  # Reproduction

    return advanced_board

def display_board(board):
    """
    Displays the Conway board.

    Parameters:
    - board (numpy.ndarray): The Conway board to display.
    """
    for row in board:
        print(' '.join(['1' if cell == 1 else '0' for cell in row]))
def calculate_live_cells_percentage(board):
    total_cells = board.size
    live_cells = np.sum(board)
    percentage = (live_cells / total_cells) * 100
    return percentage

    # Usage:



# Example usage:
size = 50
probability = 0.1
initial_board = conway(size, probability)
print("Initial Board:")
display_board(initial_board)

for time_steps in range(1, 6):
    advanced_board = advance(initial_board, time_steps)
    print("\nBoard after", time_steps, "time steps:")
    display_board(advanced_board)


percentage = calculate_live_cells_percentage(initial_board)
print(f"The percentage of live cells in the initial board is {percentage}%")