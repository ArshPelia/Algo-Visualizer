import tkinter as tk
from tkinter import messagebox
import subprocess


def run_search_algorithm_visualization():
    # Execute the search algorithm visualization script
    subprocess.run(["python", "src\search\search.py"])


def run_sort_algorithm_visualization():
    # Execute the sort algorithm visualization script
    subprocess.run(["python", "src\sort\sort.py"])


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
# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window dimensions to fit the screen
window_width = screen_width // 2  # You can adjust this as needed
window_height = screen_height // 2  # You can adjust this as needed

# Set the window size
root.geometry(f"{window_width}x{window_height}")

root.title("Algorithm Visualization Menu")

# Create a label with information
info_label = tk.Label(root, text="Select an option to visualize algorithms:")
info_label.pack(pady=20)

# Create buttons for search and sort algorithms
search_button = tk.Button(root, text="Search Algorithms",
                          command=run_search_algorithm_visualization)
search_button.pack(pady=20)

sort_button = tk.Button(root, text="Sort Algorithms",
                        command=run_sort_algorithm_visualization)
sort_button.pack(pady=20)

# Create an info button to display information about the menu
info_button = tk.Button(root, text="Info", command=show_info)
info_button.pack(pady=20)

# Start the main loop
root.mainloop()
