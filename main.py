"""
MAIN
"""
from code.classes.parser import AnnealingParameters
from code.classes.solver import Solver
from code.classes.visualizer import Visualizer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

np.random.seed(50)

if __name__ == '__main__':

    """
    Parameters for the best found solution of a280 and pcb442
    """

    # parameters for the best found solution of a280
    params_best1 = AnnealingParameters(
        problem_set='a280',
        save_data=True,
        folder_name= "a280_best",
        initial_temperature=150,
        cooling_rate=0.5,
        markov_chain_length=500,
        num_markov_chains=1500,
    )

    solver_best1 = Solver(params_best1)
    solver_best1.simulated_annealing_log_cool()


    # parameters for the best found solution of a280
    params_best2 = AnnealingParameters(
        problem_set='pcb442',
        save_data=True,
        folder_name= "pcb442_best",
        initial_temperature=60,
        cooling_rate=0.99,
        markov_chain_length=5000,
        num_markov_chains=500,
    )

    solver_best2 = Solver(params_best2)
    solver_best2.simulated_annealing_log_cool()

    """
    Showing temperature change of different couling schedules
    """

    initial_temp = 150
    rate = 0.99 
    Markov_length = 150
    Markov_Num = 1000
    beta = 11

    rcParams.update({
    'font.size': 15,
    })
    iteration = np.linspace(1,1000,1000)
    temp_exp = []
    temperature = initial_temp
    for i in range(1000): 
        temperature = temperature * rate
        temp_exp.append(temperature)
    temp_log = []
    initial_temp = 150
    for i in range(1000): 
        temperature = initial_temp / (1 + beta * np.log(1 + i))
        temp_log.append(temperature)
    temp_lin = []
    initial_temp = 150
    for i in range(1000): 
        temperature = max(0.1, initial_temp - rate * i)
        temp_lin.append(temperature)    

    plt.figure(figsize=(12, 10))
    plt.grid()
    plt.plot(iteration, temp_exp, label = "Exponencial cooling", color = "red")
    plt.plot(iteration, temp_lin, label = "Linear cooling", color = "blue")
    plt.plot(iteration, temp_log, label = "Logarithmic cooling", color = "green")
    plt.legend()
    plt.xlabel("Temperature adjustment points(Number of Markov chains)")
    plt.ylabel("Temperature value")

    """
    Different cooling schedules
    """

    # exponential cooling
    for i in range(10):    
        params_exp = AnnealingParameters(
            problem_set='a280',
            save_data=True,
            folder_name= f'Exp_{i}',
            initial_temperature=150,
            cooling_rate=0.5,
            markov_chain_length=500,
            num_markov_chains=1500,
        )

        # create board and solve the problem
        solver_exp = Solver(params_exp)
        solver_exp.simulated_annealing_exp_cooling()

        visualizer_exp = Visualizer(solver=solver_exp)
        visualizer_exp.plot_final_solution()
        visualizer_exp.plot_tour_length()
        
        # Optional functions
        # visualizer.plot_animation()
        # visualizer.plot_summary()


    # linear cooling
    for i in range(10):
        params_lin = AnnealingParameters(
            problem_set='a280',
            save_data=True,
            folder_name= f'Lin_{i}',
            initial_temperature=150,
            cooling_rate=0.5,
            markov_chain_length=150,
            num_markov_chains=1000,
        )
        solver_lin = Solver(params_lin)
        solver_lin.simulated_annealing_lin_cool()

        visualizer_lin = Visualizer(solver=solver_lin)
        visualizer_lin.plot_final_solution()
        visualizer_lin.plot_tour_length() 


    # log cooling
    iteration = np.linspace(10,150,15, dtype=int)
    for i in iteration:
        params_log = AnnealingParameters(
            problem_set='a280',
            save_data=True,
            folder_name= f'Length_{i}',
            initial_temperature=150,
            cooling_rate=0.5,
            markov_chain_length=i,
            num_markov_chains=1000,
        )

        solver_log = Solver(params_log)
        solver_log.simulated_annealing_log_cool()

        visualizer_log = Visualizer(solver=solver_log)
        visualizer_log.plot_final_solution()
        visualizer_log.plot_tour_length() 