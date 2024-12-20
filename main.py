"""
MAIN
"""
from code.classes.parser import AnnealingParameters
from code.classes.solver import Solver
from code.classes.visualizer import Visualizer
from code.functions import * # Feel free to add functions within this file 

np.random.seed(50)

# for i in range(10):
#     if __name__ == '__main__':

#         ################################################
#         # Example of how to run the solver and visualizer
#         ################################################

#         #parameters
#         params1 = AnnealingParameters(
#             problem_set='a280',
#             save_data=True,
#             folder_name= f'Lin_{i}',
#             initial_temperature=150,
#             cooling_rate=0.5,
#             markov_chain_length=150,
#             num_markov_chains=1000,
#         )

#         # create board and solve the problem
#         solver1 = Solver(params1)
#         solver1.simulated_annealing_lin_cool()

#         # functions you can use after the solver is finished
#         visualizer = Visualizer(solver=solver1)
#         visualizer.plot_final_solution()
#         visualizer.plot_summary() 
#         #visualizer.plot_animation() this gives an annimation 

# iteration = np.linspace(10,150,15, dtype=int)
# for i in iteration:
#     if __name__ == '__main__':

#         ################################################
#         # Example of how to run the solver and visualizer
#         ################################################

#         #parameters
#         params1 = AnnealingParameters(
#             problem_set='a280',
#             save_data=True,
#             folder_name= f'Length_{i}',
#             initial_temperature=150,
#             cooling_rate=0.5,
#             markov_chain_length=i,
#             num_markov_chains=1000,
#         )

#         # create board and solve the problem
#         solver1 = Solver(params1)
#         solver1.simulated_annealing_log_cool()

#         # functions you can use after the solver is finished
#         visualizer = Visualizer(solver=solver1)
#         visualizer.plot_final_solution()
#         visualizer.plot_summary() 
#         #visualizer.plot_animation() this gives an annimation 


if __name__ == '__main__':

        ################################################
        # Example of how to run the solver and visualizer
        ################################################

    #parameters
    params1 = AnnealingParameters(
        problem_set='a280',
        save_data=True,
        folder_name= "Aim_for_the_best",
        initial_temperature=150,
        cooling_rate=0.5,
        markov_chain_length=500,
        num_markov_chains=1500,
    )

    # create board and solve the problem
    solver1 = Solver(params1)
    solver1.simulated_annealing_log_cool()

        # functions you can use after the solver is finished
    visualizer = Visualizer(solver=solver1)
    visualizer.plot_final_solution()
    visualizer.tour_length() 
        #visualizer.plot_animation() this gives an annimation 