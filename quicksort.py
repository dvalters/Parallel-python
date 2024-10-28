"""
A parallel implementation of quicksort using MPI"""

from mpi4py import MPI
import numpy as np

# Initialize the MPI environment
comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # Current process rank
size = comm.Get_size()  # Total number of processes

def quicksort(arr):
    """Serial Quicksort Algorithm."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)


def parallel_quicksort(arr, depth=0):
    """Parallel Quicksort using MPI."""
    n = len(arr)

    # If there's only one process or the array is small enough, perform serial quicksort
    if size == 1 or n <= 1:
        return quicksort(arr)

    # If there's only one element or only one process, there's nothing to sort in parallel
    if n <= 1:
        return arr

    # Choose the pivot as the middle element
    pivot = arr[len(arr) // 2]

    # Partition the data into three parts
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    # Split the processes in two groups
    color = rank // (size // 2)
    new_comm = comm.Split(color)

    if color == 0:
        # If in the left group, recursively sort the left part
        left_sorted = new_comm.bcast(left, root=0)
        return parallel_quicksort(left_sorted, depth + 1) + middle
    else:
        # If in the right group, recursively sort the right part
        right_sorted = new_comm.bcast(right, root=0)
        return middle + parallel_quicksort(right_sorted, depth + 1)

if __name__=="__main__":
    if rank == 0:
        # Master process initializes the array
        n = 100  # Length of the array to sort
        arr = np.random.randint(0, 1000, size=n)
        print(f"Unsorted array: {arr}")

        # Divide the array among all processes
        chunks = np.array_split(arr, size)
    else:
        chunks = None

    # Scatter chunks of data to all processes
    data = comm.scatter(chunks, root=0)

    # Each process sorts its chunk locally using quicksort
    sorted_chunk = quicksort(data)

    # Gather sorted chunks at the root process
    gathered_data = comm.gather(sorted_chunk, root=0)

    if rank == 0:
        # Merge all sorted chunks at the root process
        sorted_arr = np.concatenate(gathered_data)
        print(f"Sorted array: {sorted_arr}")
