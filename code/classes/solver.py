from code.classes.board import Board
import time
import numpy as np
import csv
import os
from code.functions import *


class Solver:
    def __init__(self, params):
        """
        Initialize a Solver instance with the provided parameters.
        pre:
        - params must include attributes for the problem set, initial temperature, cooling rate, 
          markov chain length, number of markov chains, and save_data option.
        post:
        - A Solver instance is created with the given parameters and an initialized Board.
        """
        self.board = Board(params)
        self.p = params

        # Saved parameters for plotting
        self.all_tours = []
        self.all_lengths = []
        self.all_temperatures = []
        self.all_acceptance_probs = []

    def _give_answer(self):
        """
        Check if the current tour matches the optimal solution and print the result.
        pre:
        - self.board.tour_order must contain a valid tour of Node objects.
        - self.board.tour_solution must be the correct optimal solution.
        post:
        - Prints whether the tour is correct and displays the current tour and its length.
        """
        tour = [node.ID for node in self.board.tour_order]

        if tour != self.board.tour_solution:
            print("The tour is not correct.")
            print(f"Expected: {self.board.tour_solution}")
            print(f"Got: {tour}")
        else:
            print("The tour is correct.")
            print(f"Tour: {tour}")
            print(f"Tour length: {self.board.calculate_tour_distance()}")

    def simulated_annealing_exp_cooling(self):
        """
        Perform simulated annealing to solve the travelling salesman problem.
        pre:
        - self.p must include valid attributes for initial_temperature, cooling_rate, 
          markov_chain_length, num_markov_chains, and save_data options.
        - Board instance must be initialized with a valid tour and nodes.
        post:
        - Performs simulated annealing to find an optimized tour.
        - Saves intermediate states for visualization and optionally saves results to CSV files.
        """
        print('=========Simulated Annealing started==========')

        start_time = time.time() 

        current_distance = self.board.calculate_tour_distance()
        temperature = self.p.initial_temperature

        for i in range(self.p.num_markov_chains):
            temperature = temperature * self.p.cooling_rate

            for j in range(self.p.markov_chain_length):
                previous_tour = self.board.tour_order[:]

                index1, index2 = np.random.randint(0, len(self.board.tour_order), 2)
                while index1 == index2 or abs(index1 - index2) == 1 or abs(index1 - index2) == len(self.board.tour_order) - 1:
                    index1, index2 = np.random.randint(0, len(self.board.tour_order), 2)

                self.board.two_opt_swap(index1, index2)
                new_distance = self.board.calculate_tour_distance()
                delta = new_distance - current_distance
                acceptance_prob = np.exp(-delta / temperature) if delta > 0 else 1

                if delta < 0:
                    current_distance = new_distance
                else:
                    if np.random.rand() < acceptance_prob: 
                        current_distance = new_distance
                    else:
                        self.board.tour_order = previous_tour[:]

                # Save current state for visualization
                self.board.order_tour()
                self.all_tours.append(self.board.tour_order[:])
                self.all_lengths.append(current_distance)
                self.all_temperatures.append(temperature)
                self.all_acceptance_probs.append(acceptance_prob)

        self.board.order_tour()

        end_time = time.time() 
        elapsed_time = end_time - start_time
        print(f"Simulation took {elapsed_time:.2f} seconds.")


        print("=========Simulated Annealing finished=========")
        print(self.board)

        if self.p.save_data:
            self._save_data()

    def simulated_annealing_log_cool(self):
        """
        Perform simulated annealing to solve the travelling salesman problem using the 2-opt swap.
        pre:
        - self.p must include valid attributes for initial_temperature, cooling_rate, 
        markov_chain_length, num_markov_chains, and save_data options.
        - Board instance must be initialized with a valid tour and nodes.
        post:
        - Performs simulated annealing to find an optimized tour.
        - Saves intermediate states for visualization and optionally saves results to CSV files.
        """
        print('=========Simulated Annealing started==========')

        start_time = time.time()

        current_distance = self.board.calculate_tour_distance()

        initial_temperature = self.p.initial_temperature

        for i in range(self.p.num_markov_chains):
            temperature = logarithmic_cooling(initial_temperature, 11, i)

            for j in range(self.p.markov_chain_length):
                previous_tour = self.board.tour_order[:]

                # Select two non-adjacent cities (index1, index2) for the 2-opt swap
                index1, index2 = np.random.randint(0, len(self.board.tour_order), 2)
                while index1 == index2 or abs(index1 - index2) == 1 or abs(index1 - index2) == len(self.board.tour_order) - 1:
                    index1, index2 = np.random.randint(0, len(self.board.tour_order), 2)

                # Perform the 2-opt swap between the selected cities
                self.board.two_opt_swap(index1, index2)
                new_distance = self.board.calculate_tour_distance()
                delta = new_distance - current_distance
                acceptance_prob = np.exp(-delta / temperature) if delta > 0 else 1

                if delta < 0:
                    current_distance = new_distance
                else:
                    if np.random.rand() < acceptance_prob:
                        current_distance = new_distance
                    else:
                        self.board.tour_order = previous_tour[:]

                # Save current state for visualization
                self.board.order_tour()
                self.all_tours.append(self.board.tour_order[:])
                self.all_lengths.append(current_distance)
                self.all_temperatures.append(temperature)
                self.all_acceptance_probs.append(acceptance_prob)

        self.board.order_tour()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Simulation took {elapsed_time:.2f} seconds.")

        print("=========Simulated Annealing finished=========")
        print(self.board)

        if self.p.save_data:
            self._save_data()



    def _save_data(self):
        """
        Save all collected data to CSV files if save_data is True.
        pre:
        - self.p.save_data must be True to perform saving.
        - The specified output folder must be writable or creatable.
        post:
        - Saves the tour data, lengths, temperatures, and acceptance probabilities to CSV files.
        - Prints the directory where the data is saved.
        """
        if not self.p.save_data:
            return

        folder_path = os.path.abspath(os.path.join("output", self.p.folder_name))
        os.makedirs(folder_path, exist_ok=True)
        def write_csv(file_name, data, header=""):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([header])  
                writer.writerows(data) 

        params_header = (
            f"Problem Set: {self.p.problem_set}, "
            f"Initial Temperature: {self.p.initial_temperature}, "
            f"Cooling Rate: {self.p.cooling_rate}, "
            f"Markov Chain Length: {self.p.markov_chain_length}, "
            f"Number of Markov Chains: {self.p.num_markov_chains}"
        )

        write_csv("all_tours.csv", [[node.ID for node in tour] for tour in self.all_tours], params_header)
        write_csv("all_lengths.csv", [[length] for length in self.all_lengths], params_header)
        write_csv("all_temperatures.csv", [[temp] for temp in self.all_temperatures], params_header)
        write_csv("all_acceptance_probs.csv", [[prob] for prob in self.all_acceptance_probs], params_header)

        print(f"Data saved to folder: {folder_path}")
