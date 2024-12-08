"""
MAIN
"""
from code.classes.parser import AnnealingParameters
from code.classes.solver import Solver
from code.classes.visualizer import Visualizer
from code.functions import * # Feel free to add functions within this file 


if __name__ == '__main__':

    ################################################
    # Example of how to run the solver and visualizer
    ################################################

    # parameters
    params = AnnealingParameters(
        problem_set = 'eil51',
        save_data = True,
        folder_name = 'eil51_test1',
        initial_temperature=30,
        cooling_rate=0.99,
        markov_chain_length=500,
        num_markov_chains=1000
    )

    # create board and solve the problem
    solver = Solver(params)
    solver.simulated_annealing()

    # functions you can use after the solver is finished
    visualizer = Visualizer(solver)
    visualizer.plot_final_solution()
    visualizer.plot_summary()   
    visualizer.plot_animation()
    
    ################################################
    # Example of how to load the data from the csv files
    ################################################

    # Choose the folder name to read the data from
    # Do not add additional parameters except problem_set and folder_name
    params2 = AnnealingParameters(    
        problem_set = 'eil51',
        folder_name = 'eil51_test2',
    )

    visualizer2 = Visualizer(params=params2)
    visualizer2.plot_final_solution()
    visualizer2.plot_summary()
    visualizer2.plot_animation()


    # You can also create 2 instances of the solver and compare the results, as the results are saved in each solver object
    # Or create seperate functions to compare the stored csv data, in the file functions.py
