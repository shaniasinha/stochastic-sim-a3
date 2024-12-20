<<<<<<< HEAD
# add your own functions here if necessary
=======
# add your own functions here if necessary
import numpy as np

def logarithmic_cooling(t_initial, beta, i):
    """
    Cooling in accordance with logarithmic schedule.
    
    Parameters:
        T_initial (float): The initial temperature.
        beta (float): Cooling rate constant.
        k (int): Current iteration number.
        
    Returns:
        float: Updated temperature.
    """
    if i == 0:
        return t_initial
    return t_initial / (1 + beta * np.log(1 + i))

def linear_cooling(t_initial, cooling_rate , i):
    """
    Cooling in accordance with linear schedule.
    
    Parameters:
        T_current (float): Current temperature.
        Cooling (float): Cooling rate given. 
        k (int): Current iteration number.
        
    Returns:
        float: Updated temperature.
    """
    return max(0.1, t_initial - cooling_rate * i)

>>>>>>> origin/karolina_updated
