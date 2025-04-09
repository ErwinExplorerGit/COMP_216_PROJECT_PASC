import tkinter as tk
import subscribers.one as subscriber_one_frame
import subscribers.two as subscriber_two_frame

from publishers.one import create_publisher_one
from publishers.two import create_publisher_two
from publishers.three import create_publisher_three

# Root window setup
root = tk.Tk()
root.title("COMP_216_PROJECT_PUBLISHER AND SUBSCRIBER COMMUNICATION")
root.resizable(False, False)

# Set window size and center on screen
window_width = 1000
window_height = 800
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int((screen_width - window_width) / 2)
center_y = int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

# Configure root grid
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Top: Subscribers
top_frame = tk.Frame(root)
top_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
top_frame.grid_columnconfigure(0, weight=1)
top_frame.grid_columnconfigure(1, weight=1)
top_frame.grid_rowconfigure(0, weight=1)

subscriber1 = subscriber_one_frame.create_subscriber_one(top_frame)
subscriber1.grid(row=0, column=0, sticky="nsew", padx=10)

subscriber2 = subscriber_two_frame.create_subscriber_two(top_frame)
subscriber2.grid(row=0, column=1, sticky="nsew", padx=10)

# Bottom: Publishers
bottom_frame = tk.Frame(root)
bottom_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
for col in range(3):
    bottom_frame.grid_columnconfigure(col, weight=1)
bottom_frame.grid_rowconfigure(0, weight=1)

publisher1 = create_publisher_one(bottom_frame)
publisher1.grid(row=0, column=0, sticky="nsew", padx=5)

publisher2 = create_publisher_two(bottom_frame)
publisher2.grid(row=0, column=1, sticky="nsew", padx=5)

publisher3 = create_publisher_three(bottom_frame)
publisher3.grid(row=0, column=2, sticky="nsew", padx=5)

# Run the application
root.mainloop()
