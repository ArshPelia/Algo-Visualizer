import tkinter as tk
from tkinter import messagebox
import subprocess


def run_search_algorithm_visualization():
    # Execute the search algorithm visualization script
    subprocess.run(["python", "src\sort\main.py"])


def run_sort_algorithm_visualization():
    # Execute the sort algorithm visualization script
    subprocess.run(["python", "src\search\main.py"])


def show_info():
    info = """
    Welcome to the Algorithm Visualization Menu!

    Select an option to visualize different algorithms:
    - Search Algorithms: Visualize pathfinding algorithms.
    - Sort Algorithms: Visualize sorting algorithms.
    """
    messagebox.showinfo("Algorithm Visualization Menu", info)


# Create the main menu window
root = tk.Tk()
root.title("Algorithm Visualization Menu")

# Create a label with information
info_label = tk.Label(root, text="Select an option to visualize algorithms:")
info_label.pack(pady=20)

# Create buttons for search and sort algorithms
search_button = tk.Button(root, text="Search Algorithms",
                          command=run_search_algorithm_visualization)
search_button.pack()

sort_button = tk.Button(root, text="Sort Algorithms",
                        command=run_sort_algorithm_visualization)
sort_button.pack()

# Create an info button to display information about the menu
info_button = tk.Button(root, text="Info", command=show_info)
info_button.pack()

# Start the main loop
root.mainloop()
