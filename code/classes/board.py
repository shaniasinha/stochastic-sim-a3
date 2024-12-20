import os
import math as m
import numpy as np
from typing import List


class Node:
    def __init__(self, ID: int, x: float, y: float):
        """
        Initialize a Node instance.
        pre:
        - ID must be a positive integer.
        - x and y must be valid float coordinates.
        post:
        - A Node instance is created with specified ID and coordinates.
        """
        self.ID = ID
        self.x = x
        self.y = y


class Board:
    def __init__(self, params):
        """
        Initialize a Board instance for a given TSP problem set.
        The tour_order list is initialized with the nodes in the order they are read from the file.
        """
        self.problem_set = params.problem_set
        if self.problem_set not in {'eil51', 'a280', 'pcb442'}:
            raise ValueError('Invalid problem set: choose eil51, a280 or pcb442')
        
        self.tour_solution: List[int] = self.read_solution()
        self.tour_order: List[Node] = self.read_nodes()
        self.tour_distance = self.calculate_tour_distance()

    def read_nodes(self) -> List[Node]:
        """
        Read nodes from the TSP configuration file.
        pre:
        - The file path corresponding to the problem_set must exist and contain valid node data.
        post:
        - Returns a list of Node objects matching the specified dimension in the file.
        - Raises ValueError if the number of nodes does not match the dimension.
        """
        path = os.path.join(os.path.dirname(__file__), '../..', 'TSP-Configurations', f'{self.problem_set}.tsp.txt')
        dimension = 0
        nodes = []
        start_processing = False
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('DIMENSION'):
                    line = line.strip()
                    dimension = int(line.split()[-1])
                    continue
                if line.startswith('NODE_COORD_SECTION'):
                    start_processing = True
                    continue
                if start_processing:
                    if line.startswith('EOF'):
                        continue
                    node = line.strip().split()
                    nodes.append(Node(int(node[0]), float(node[1]), float(node[2])))

        if len(nodes) != dimension:
            raise ValueError('Number of nodes does not match dimension')
        
        return nodes

    def read_solution(self) -> List[int]:
        """
        Read the optimal tour solution from the TSP configuration file.
        pre:
        - The file path corresponding to the problem_set must exist and contain valid solution data.
        post:
        - Returns a list of node IDs representing the optimal tour solution.
        - Raises ValueError if the number of nodes does not match the dimension.
        """
        path = os.path.join(os.path.dirname(__file__), '../..', 'TSP-Configurations', f'{self.problem_set}.opt.tour.txt')
        dimension = 0
        correct_order = []
        start_processing = False
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('DIMENSION'):
                    line = line.strip()
                    dimension = int(line.split()[-1])
                    continue
                if line.startswith('TOUR_SECTION'):
                    start_processing = True
                    continue
                if start_processing:
                    if line.startswith('-1'):
                        break
                    node = line.strip().split()
                    correct_order.append(int(node[0]))

        if len(correct_order) != dimension:
            raise ValueError('Number of nodes does not match dimension')
        
        return correct_order
    
    def two_opt_swap(self, index1: int, index2: int):
        """
        Performs a 2-opt swap between two non-adjacent nodes in the tour by reversing the order of the nodes
        between index1 and index2. This eliminates edge crossings and potentially reduces the total distance.
        
        pre:
        - index1 and index2 must be valid indices in the tour_order list.
        - Nodes at index1 and index2 must not be adjacent or form a direct loop edge.
        post:
        - The sub-tour between index1 and index2 is reversed (2-opt).
        - Raises ValueError if nodes are adjacent or form a direct loop edge.
        """
        if abs(index1 - index2) == 1 or abs(index1 - index2) == len(self.tour_order) - 1:
            raise ValueError('Nodes are adjacent or form a direct loop edge')
        
        # Ensure index1 is smaller than index2 for consistency in slicing
        if index1 > index2:
            index1, index2 = index2, index1
        
        # Reverse the segment between index1 and index2 (2-opt swap)
        self.tour_order[index1:index2 + 1] = reversed(self.tour_order[index1:index2 + 1])


    def order_tour(self):
        """
        Reorders the tour so that it starts with the node having ID 1.
        pre:
        - Node with ID 1 must exist in the tour_order list.
        post:
        - The tour_order list is rearranged to start with the node having ID 1.
        """
        start_index = next(i for i, node in enumerate(self.tour_order) if node.ID == 1)
        self.tour_order = self.tour_order[start_index:] + self.tour_order[:start_index]

    def _distance(self, Node1: Node, Node2: Node) -> float:
        """
        Calculate the Euclidean distance between two nodes.
        pre:
        - Node1 and Node2 must be valid Node instances.
        post:
        - Returns the Euclidean distance between Node1 and Node2.
        """
        x1, y1 = Node1.x, Node1.y
        x2, y2 = Node2.x, Node2.y
        distance = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        distance_rounded = np.round(distance)
        return distance

    def calculate_tour_distance(self) -> float:
        """
        Calculate the total distance of the tour, forming a closed loop.
        pre:
        - tour_order must contain a valid sequence of Node instances.
        post:
        - Returns the total distance of the tour as a float.
        """
        return sum(
            self._distance(self.tour_order[i], self.tour_order[(i + 1) % len(self.tour_order)])
            for i in range(len(self.tour_order))
        )

    def __str__(self) -> str:
        """
        Represent the tour as a string.
        pre:
        - tour_order must be a valid list of Node instances.
        post:
        - Returns a string representation of the tour order and total distance.
        """
        tour_order = ', '.join(str(node.ID) for node in self.tour_order)
        tour_distance = self.calculate_tour_distance()
        return f'Tour order: {tour_order}\nTotal distance: {tour_distance}'
