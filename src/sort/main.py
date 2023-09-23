import pygame
import random
import sys
import tkinter as tk
from tkinter import messagebox

# Constants
WIDTH = 800
HEIGHT = 600
ARRAY_SIZE = 100
BACKGROUND_COLOR = (255, 255, 255)
BAR_COLOR = (0, 0, 255)
RESET_KEY = pygame.K_r
bSORT_KEY = pygame.K_b
sSORT_KEY = pygame.K_s

# Pygame setup
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Algorithm Visualizer")
clock = pygame.time.Clock()

# Create an initial random array


def create_random_array(size):
    return [random.randint(50, 450) for _ in range(size)]

# Bubble Sort function as a generator


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                yield arr


def select_sort(arr):
    for i in range(len(arr)):
        # Find the minimum element in remaining
        # unsorted array
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j

        # Swap the found minimum element with
        # the first element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr


def main():
    # Initialize variables
    array = create_random_array(ARRAY_SIZE)
    sorting = False
    sort_generator = None

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == RESET_KEY and not sorting:
                    array = create_random_array(ARRAY_SIZE)
                elif event.key == bSORT_KEY and not sorting:
                    sorting = True
                    array_copy = array.copy()
                    sort_generator = bubble_sort(array_copy)
                elif event.key == sSORT_KEY and not sorting:
                    sorting = True
                    array_copy = array.copy()
                    sort_generator = select_sort(array_copy)

        window.fill(BACKGROUND_COLOR)

        # Sorting animation
        if sorting:
            try:
                array = next(sort_generator)
            except StopIteration:
                sorting = False

        # Draw the bars
        bar_width = WIDTH // len(array)
        for i, height in enumerate(array):
            pygame.draw.rect(window, BAR_COLOR, (i * bar_width,
                             HEIGHT - height, bar_width, height))

        pygame.display.update()
        clock.tick(120)

    pygame.quit()
    sys.exit()


def display_controls_popup():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    messagebox.showinfo("Controls", """
    Controls:
    - r key: Reset Array
    - b key: Run bubble sort algorithm
    - s key: Run selection sort algorithm
    - Esc key: Quit the program
    """)


if __name__ == "__main__":
    display_controls_popup()
    main()
