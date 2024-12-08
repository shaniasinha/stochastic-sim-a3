from dataclasses import dataclass

@dataclass
class AnnealingParameters:
    """
    Data class to store the parameters.
    """
    problem_set: str = None
    save_data: bool = None                 # Saves data as csv file and saves the plots if True
    folder_name: str = None
    initial_temperature: float = None
    cooling_rate: float = None
    markov_chain_length: int = None
    num_markov_chains: int = None