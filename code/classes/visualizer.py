from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from code.classes.board import Board
import numpy as np
import os
import csv
from matplotlib import rcParams

rcParams.update({
    'font.size': 15,
})

class Visualizer:
    def __init__(self, solver = None, params = None):
        """
        Initialize a Visualizer instance with the provided Solver instance or parameters.
        pre:
        - Either a Solver instance or parameters must be provided.
        post:
        - If a Solver instance is provided, the Visualizer is initialized with the Solver's data.
        - If parameters are provided, the Visualizer is initialized with the specified parameters.
        - If only params are given the visualizer loads data from the Solver's CSV files.
        """
        self.board = solver.board if solver != None else Board(params)
        self.p = solver.p if solver != None else params
        
        if solver != None:
            self.all_tours = solver.all_tours
            self.all_lengths = solver.all_lengths
            self.all_temperatures = solver.all_temperatures
            self.all_acceptance_probs = solver.all_acceptance_probs
        else:
            print("Loading data from CSV files...")
            self._load_data()

    def _load_data(self):
        """
        Load previously saved data from CSV files into the corresponding arrays.
        pre:
        - The specified folder and CSV files must exist.
        - The CSV files must be in the correct format.
        post:
        - Populates self.all_tours, self.all_lengths, self.all_temperatures, and self.all_acceptance_probs
        with the data read from the files.
        - Prints a success message when loading is complete.
        """
        folder_path = os.path.abspath(os.path.join("output", self.p.folder_name))
        
        def read_csv(file_name):
            file_path = os.path.join(folder_path, file_name)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File {file_path} does not exist.")
            with open(file_path, mode="r") as file:
                reader = csv.reader(file)
                next(reader)  
                return [row for row in reader]

        id_to_node = {node.ID: node for node in self.board.tour_order}

        self.all_tours = [
            [id_to_node[int(node_id)] for node_id in row]
            for row in read_csv("all_tours.csv")
        ]
        self.all_lengths = [
            float(row[0]) for row in read_csv("all_lengths.csv")
        ]
        self.all_temperatures = [
            float(row[0]) for row in read_csv("all_temperatures.csv")
        ]
        self.all_acceptance_probs = [
            float(row[0]) for row in read_csv("all_acceptance_probs.csv")
        ]

        print(f"Data loaded from folder: {folder_path}")


    def plot_final_solution(self):
        """
        Plot the final TSP solution, comparing it to the target solution.
        """
        x_final = [node.x for node in self.all_tours[-1]] + [self.all_tours[-1][0].x]
        y_final = [node.y for node in self.all_tours[-1]] + [self.all_tours[-1][0].y]

        x_solution = [node.x for node in self.board.tour_solution] + [self.board.tour_solution[0].x]
        y_solution = [node.y for node in self.board.tour_solution] + [self.board.tour_solution[0].y]

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.plot(x_solution, y_solution, 'o--', color='red', markersize=6, label="Target Solution Path")
        ax.plot(x_final, y_final, 'o-', color='blue', markersize=6, label="Final Tour Path", linewidth=2, alpha=0.5)
        

        # Optional: Adjust or remove node ID labels
        for node in self.all_tours[-1]:
            ax.text(
                node.x, node.y, "",  # Change "" to `str(node.ID)` to display smaller node IDs.
                color='white', fontsize=4, ha='center', va='center',  # Adjust font size here
                bbox=dict(boxstyle='circle', facecolor='black', pad=0.3)
            )

        ax.set_title("TSP Tour: Final vs Target Solution")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        plt.legend()

        if self.p.save_data:
            folder_path = os.path.abspath(os.path.join("output", self.p.folder_name))
            os.makedirs(folder_path, exist_ok=True)
            plt.savefig(f"output/{self.p.folder_name}/final.png")
            print(f"Final plot saved to/{folder_path} as final.png")

        plt.show()


    def plot_animation(self, target_frames=1000):
        """
        Animate the TSP solution evolution, downsampling frames to ensure a maximum of `target_frames`.
        :param target_frames: The target number of frames to display in the animation.
        """
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_title("TSP Solution Evolution")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        line, = ax.plot([], [], 'o-', color='blue', markersize=6, linewidth=2, alpha=0.7)
        length_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12, color='blue')

        total_frames = len(self.all_tours)
        if total_frames > target_frames:
            frame_indices = np.linspace(0, total_frames - 1, target_frames, dtype=int)
        else:
            frame_indices = np.arange(total_frames)

        def init():
            first_tour = self.all_tours[0]
            ax.set_xlim(
                min(node.x for node in first_tour) - 10, 
                max(node.x for node in first_tour) + 10
            )
            ax.set_ylim(
                min(node.y for node in first_tour) - 10, 
                max(node.y for node in first_tour) + 10
            )
            return line, length_text

        def update(frame):
            tour = self.all_tours[frame_indices[frame]]
            x = [node.x for node in tour] + [tour[0].x]
            y = [node.y for node in tour] + [tour[0].y]

            line.set_data(x, y)

            current_length = self.all_lengths[frame_indices[frame]]
            progress = (frame + 1) / len(frame_indices) * 100
            length_text.set_text(f"Length: {current_length:.2f} | Progress: {progress:.1f}%")

            if frame == len(frame_indices) - 1:
                length_text.set_text(f"Final Length: {current_length:.2f} | Animation Complete")

            return line, length_text

        anim = FuncAnimation(
            fig, update, frames=len(frame_indices), init_func=init, blit=True, interval=1, repeat=False
        )

        plt.show()

    def plot_summary(self):
        """
        Plots a 2x2 grid with:
        - Tour lengths over time
        - Temperatures over time
        - Acceptance probabilities over time
        - Final tour solution
        """
        fig, axs = plt.subplots(1, 2, figsize=(12, 10))
        fig.tight_layout(pad=5)
        
        axs[0].plot(self.all_lengths, color='blue', label="Tour Length")
        axs[0].set_title("Tour Lengths Over Time")
        axs[0].set_xlabel("Iteration")
        axs[0].set_ylabel("Tour Length")
        axs[0].legend()
        axs[0].grid(True)

        axs[1].plot(self.all_temperatures, color='red', label="Temperature")
        axs[1].set_title("Temperatures Over Time")
        axs[1].set_xlabel("Iteration")
        axs[1].set_ylabel("Temperature")
        axs[1].legend()
        axs[1].grid(True)
        
        if self.p.save_data:
            folder_path = os.path.abspath(os.path.join("output", self.p.folder_name))
            os.makedirs(folder_path, exist_ok=True)
            plt.savefig(f"output/{self.p.folder_name}/summary.png")
            print(f"Summary plot saved {folder_path} as summary.png")

        plt.show()

    def plot_tour_length(self):
        """
        Plot the tour lengths over time.
        """
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.plot(self.all_lengths, color='blue', label="Tour Length")
        ax.set_title("Tour Lengths Over Time")
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Tour Length")
        ax.legend()
        ax.grid(True)

        if self.p.save_data:
            folder_path = os.path.abspath(os.path.join("output", self.p.folder_name))
            os.makedirs(folder_path, exist_ok=True)
            plt.savefig(f"output/{self.p.folder_name}/summary.png")
            print(f"Summary plot saved {folder_path} as summary.png")

        plt.show()

