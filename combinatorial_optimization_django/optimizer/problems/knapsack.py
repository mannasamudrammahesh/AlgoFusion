import random

class KnapsackProblem:
    def __init__(self, weights, values, capacity):
        self.weights = weights
        self.values = values
        self.capacity = capacity

    def evaluate(self, solution):
        return sum(self.values[i] for i in solution)
    
    def is_valid_solution(self, solution):
        """Check if solution is valid (doesn't exceed capacity)"""
        total_weight = sum(self.weights[i] for i in solution)
        return total_weight <= self.capacity
    
    @classmethod
    def generate_random_instance(cls, num_items, max_weight=50, max_value=100):
        """Generate random knapsack instance"""
        weights = [random.randint(1, max_weight) for _ in range(num_items)]
        values = [random.randint(1, max_value) for _ in range(num_items)]
        capacity = sum(weights) // 2  # Set capacity to roughly half of total weight
        return cls(weights, values, capacity)
