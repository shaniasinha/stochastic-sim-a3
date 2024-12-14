# add your own functions here if necessary
import numpy as np

def logarithmic_cooling(t_initial, beta, i):
    """
    Cooling in accordance with logarithmic schedule.
    
    Parameters:
        T_initial (float): The initial temperature.
        beta (float): Cooling rate constant (small positive value, e.g., 0.01).
        k (int): Current iteration or step count.
        
    Returns:
        float: Updated temperature.
    """
    if i == 0:
        return t_initial
    return t_initial / (1 + beta * np.log(1 + i))

