from ..problems.knapsack import KnapsackProblem
from ..problems.tsp import TSPProblem
from ..problems.graph_matching import GraphMatchingProblem

class GreedySolver:
    def __init__(self, problem):
        self.problem = problem

    def solve(self):
        if isinstance(self.problem, KnapsackProblem):
            return self._solve_knapsack()
        elif isinstance(self.problem, TSPProblem):
            return self._solve_tsp()
        elif isinstance(self.problem, GraphMatchingProblem):
            return self._solve_matching()
        else:
            raise ValueError(f"Unsupported problem type: {type(self.problem)}")
    
    def _solve_knapsack(self):
        """Greedy solution for knapsack: sort by value/weight ratio"""
        items = list(range(len(self.problem.values)))
        items.sort(key=lambda i: self.problem.values[i]/self.problem.weights[i], reverse=True)
        solution = []
        total_weight = 0
        for i in items:
            if total_weight + self.problem.weights[i] <= self.problem.capacity:
                solution.append(i)
                total_weight += self.problem.weights[i]
        return solution
    
    def _solve_tsp(self):
        """Greedy solution for TSP: nearest neighbor heuristic"""
        if self.problem.n <= 1:
            return list(range(self.problem.n))
        
        unvisited = set(range(1, self.problem.n))
        tour = [0]  # Start from city 0
        current = 0
        
        while unvisited:
            nearest = min(unvisited, key=lambda city: self.problem.distance_matrix[current][city])
            tour.append(nearest)
            unvisited.remove(nearest)
            current = nearest
        
        return tour
    
    def _solve_matching(self):
        """Greedy solution for matching: sort edges by weight, add if valid"""
        # Sort edges by weight (descending)
        edge_indices = list(range(len(self.problem.edges)))
        edge_indices.sort(key=lambda i: self.problem.edges[i][2], reverse=True)
        
        matching = []
        used_vertices = set()
        
        for edge_idx in edge_indices:
            u, v, _ = self.problem.edges[edge_idx]
            if u not in used_vertices and v not in used_vertices:
                matching.append(edge_idx)
                used_vertices.add(u)
                used_vertices.add(v)
        
        return matching
