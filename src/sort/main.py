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
RESET_KEY = 'r'
bSORT_KEY = 'b'
sSORT_KEY = 's'

# Pygame setup
pygame.init()
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
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr


def main():
    # Initialize variables
    array = create_random_array(ARRAY_SIZE)
    sorting = False
    sort_generator = None

    def on_key(event):
        nonlocal sorting, sort_generator, array
        key = event.keysym
        if key == RESET_KEY and not sorting:
            array = create_random_array(ARRAY_SIZE)
        elif key == bSORT_KEY and not sorting:
            sorting = True
            array_copy = array.copy()
            sort_generator = bubble_sort(array_copy)
        elif key == sSORT_KEY and not sorting:
            sorting = True
            array_copy = array.copy()
            sort_generator = select_sort(array_copy)

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Sorting Algorithm Visualizer")

    # Create a Canvas widget to embed the Pygame window
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack()

    # Create labels to display controls
    controls_label = tk.Label(root, text="Controls:")
    controls_label.pack()
    reset_label = tk.Label(root, text="- Press 'r' key: Reset Array")
    reset_label.pack()
    bubble_sort_label = tk.Label(
        root, text="- Press 'b' key: Run bubble sort algorithm")
    bubble_sort_label.pack()
    select_sort_label = tk.Label(
        root, text="- Press 's' key: Run selection sort algorithm")
    select_sort_label.pack()
    quit_label = tk.Label(root, text="- Press 'Esc' key: Quit the program")
    quit_label.pack()

    root.bind("<Key>", on_key)  # Bind key events

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the Canvas
        canvas.delete("all")

        # Sorting animation
        if sorting:
            try:
                array = next(sort_generator)
            except StopIteration:
                sorting = False

        # Draw the bars on the Canvas
        bar_width = WIDTH // len(array)
        for i, height in enumerate(array):
            canvas.create_rectangle(
                i * bar_width, HEIGHT - height, (i + 1) * bar_width, HEIGHT, fill="blue"
            )

        root.update_idletasks()
        root.update()
        clock.tick(120)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
