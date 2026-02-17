import tkinter as tk
from tkinter import simpledialog, messagebox
from grid import Grid
from constants import *
import algorithms


# ---------------------- MAIN MENU ----------------------

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Pathfinder")
        self.root.geometry("500x500")
        self.root.configure(bg="#1e1e2f")

        self.algorithms = {
            1: ("Breadth-First Search", algorithms.bfs),
            2: ("Depth-First Search", algorithms.dfs),
            3: ("Uniform-Cost Search", algorithms.ucs),
            4: ("Depth-Limited Search", algorithms.dls),
            5: ("Iterative Deepening DFS", algorithms.iddfs),
            6: ("Bidirectional Search", algorithms.bidirectional)
        }

        self.create_layout()

    def create_layout(self):

        # Title
        title = tk.Label(self.root,
                         text="AI GRID PATHFINDER",
                         font=("Helvetica", 22, "bold"),
                         fg="white",
                         bg="#1e1e2f")
        title.pack(pady=40)

        subtitle = tk.Label(self.root,
                            text="Select an Uninformed Search Algorithm",
                            font=("Helvetica", 12),
                            fg="#bbbbbb",
                            bg="#1e1e2f")
        subtitle.pack(pady=10)

        # Button Frame
        btn_frame = tk.Frame(self.root, bg="#1e1e2f")
        btn_frame.pack(pady=20)

        for num, (name, _) in self.algorithms.items():
            btn = tk.Button(
                btn_frame,
                text=f"{num}. {name}",
                width=30,
                height=2,
                font=("Helvetica", 11),
                bg="#3a3a5c",
                fg="white",
                activebackground="#5757a8",
                activeforeground="white",
                bd=0,
                cursor="hand2",
                command=lambda n=num: self.start_algorithm(n)
            )

            btn.pack(pady=8)

            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#5757a8"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#3a3a5c"))

    def start_algorithm(self, choice):
        name, algo = self.algorithms[choice]

        depth_limit = None
        if choice == 4:
            depth_limit = simpledialog.askinteger(
                "Depth Limit",
                "Enter Depth Limit:",
                minvalue=1,
                maxvalue=100
            )
            if depth_limit is None:
                return

        self.root.destroy()

        root = tk.Tk()
        app = App(root, algo, depth_limit)
        root.mainloop()


# ---------------------- SEARCH WINDOW ----------------------

class App:
    def __init__(self, root, algorithm, depth_limit=None):
        self.root = root
        self.root.title("AI Grid Pathfinder")

        self.grid_obj = Grid()
        self.algorithm_func = algorithm
        self.depth_limit = depth_limit

        # Frame layout
        self.main_frame = tk.Frame(root)
        self.main_frame.pack()

        self.canvas = tk.Canvas(self.main_frame,
                                width=COLS * CELL_SIZE,
                                height=ROWS * CELL_SIZE)
        self.canvas.grid(row=0, column=0)

        # Legend on the right
        self.legend_frame = tk.Frame(self.main_frame)
        self.legend_frame.grid(row=0, column=1, padx=20)

        self.create_legend()

        self.search_gen = None
        self.final_path = None

        self.draw_grid()
        self.start_search()

    # ---------------------- LEGEND ----------------------

    def create_legend(self):
        tk.Label(self.legend_frame,
                 text="Color Key",
                 font=("Arial", 14)).pack(pady=10)

        self.add_legend_item("Start", START_COLOR)
        self.add_legend_item("Target", TARGET_COLOR)
        self.add_legend_item("Static Wall", WALL_COLOR)
        self.add_legend_item("Dynamic Wall", DYNAMIC_COLOR)
        self.add_legend_item("Frontier", FRONTIER_COLOR)
        self.add_legend_item("Explored", EXPLORED_COLOR)
        self.add_legend_item("Current Node", "blue")
        self.add_legend_item("Final Path", PATH_COLOR)

    def add_legend_item(self, text, color):
        frame = tk.Frame(self.legend_frame)
        frame.pack(anchor="w", pady=3)

        box = tk.Canvas(frame, width=20, height=20)
        box.create_rectangle(0, 0, 20, 20, fill=color)
        box.pack(side="left")

        tk.Label(frame, text="  " + text).pack(side="left")

    # ---------------------- DRAW GRID ----------------------

    def draw_grid(self):
        self.canvas.delete("all")

        for r in range(ROWS):
            for c in range(COLS):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                color = EMPTY_COLOR
                cell = self.grid_obj.grid[r][c]

                if cell == 1:
                    color = WALL_COLOR
                elif cell == 2:
                    color = DYNAMIC_COLOR
                elif (r, c) == self.grid_obj.start:
                    color = START_COLOR
                elif (r, c) == self.grid_obj.target:
                    color = TARGET_COLOR

                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=color, outline="gray")

    # ---------------------- SEARCH ----------------------

    def start_search(self):
        if self.depth_limit:
            self.search_gen = self.algorithm_func(self.grid_obj,
                                                  self.depth_limit)
        else:
            self.search_gen = self.algorithm_func(self.grid_obj)

        self.step()

    def step(self):
        try:
            current, frontier, explored = next(self.search_gen)

            self.grid_obj.spawn_dynamic_obstacle()

            self.draw_grid()

            for node in frontier:
                self.color_cell(node, FRONTIER_COLOR)

            for node in explored:
                self.color_cell(node, EXPLORED_COLOR)

            self.color_cell(current, "blue")

            self.root.after(DELAY, self.step)

        except StopIteration as e:
            self.final_path = e.value

            if self.final_path:
                for node in self.final_path:
                    self.color_cell(node, PATH_COLOR)

            self.ask_return_menu()

    # ---------------------- RETURN MENU ----------------------

    def ask_return_menu(self):
        result = messagebox.askyesno(
            "Algorithm Finished",
            "Search completed.\n\nReturn to algorithm selection menu?"
        )

        self.root.destroy()

        if result:
            root = tk.Tk()
            menu = MainMenu(root)
            root.mainloop()

    # ---------------------- COLOR CELL ----------------------

    def color_cell(self, pos, color):
        r, c = pos
        x1 = c * CELL_SIZE
        y1 = r * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2,
                                     fill=color, outline="gray")


# ---------------------- START PROGRAM ----------------------

root = tk.Tk()
menu = MainMenu(root)
root.mainloop()
