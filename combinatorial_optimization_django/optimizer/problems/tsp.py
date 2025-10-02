import math
import random
from typing import List, Tuple

class TSPProblem:
    """Traveling Salesman Problem implementation"""
    
    def __init__(self, cities: List[Tuple[float, float]]):
        self.cities = cities
        self.n = len(cities)
        self.distance_matrix = self._calculate_distance_matrix()
    
    def _calculate_distance_matrix(self):
        """Calculate distance matrix between all cities"""
        matrix = [[0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    x1, y1 = self.cities[i]
                    x2, y2 = self.cities[j]
                    matrix[i][j] = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        return matrix
    
    def calculate_tour_distance(self, tour: List[int]) -> float:
        """Calculate total distance of a tour"""
        if not tour or len(tour) < 2:
            return float('inf')
        
        total_distance = 0
        for i in range(len(tour)):
            current_city = tour[i]
            next_city = tour[(i + 1) % len(tour)]
            total_distance += self.distance_matrix[current_city][next_city]
        return total_distance
    
    def evaluate(self, solution: List[int]) -> float:
        """Evaluate solution quality (lower is better for TSP)"""
        return self.calculate_tour_distance(solution)
    
    @classmethod
    def generate_random_instance(cls, num_cities: int, max_coord: int = 100):
        """Generate random TSP instance"""
        cities = [(random.uniform(0, max_coord), random.uniform(0, max_coord)) 
                 for _ in range(num_cities)]
        return cls(cities)