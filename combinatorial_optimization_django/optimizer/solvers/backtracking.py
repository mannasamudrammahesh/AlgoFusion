from ..problems.knapsack import KnapsackProblem
from ..problems.tsp import TSPProblem
from ..problems.graph_matching import GraphMatchingProblem

class BacktrackingSolver:
    def __init__(self, problem):
        self.problem = problem
        self.best_solution = []
        self.best_value = 0

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
        """Backtracking solution for knapsack"""
        self.best_solution = []
        self.best_value = 0
        self._backtrack_knapsack([], 0, 0)
        return self.best_solution

    def _backtrack_knapsack(self, solution, index, current_weight):
        if index >= len(self.problem.values):
            value = sum(self.problem.values[i] for i in solution)
            if value > self.best_value:
                self.best_value = value
                self.best_solution = solution[:]
            return
        # include
        if current_weight + self.problem.weights[index] <= self.problem.capacity:
            solution.append(index)
            self._backtrack_knapsack(solution, index+1, current_weight + self.problem.weights[index])
            solution.pop()
        # exclude
        self._backtrack_knapsack(solution, index+1, current_weight)
    
    def _solve_tsp(self):
        """Backtracking solution for TSP"""
        if self.problem.n > 10:  # Too expensive for large instances
            from .greedy import GreedySolver
            return GreedySolver(self.problem).solve()
        
        self.best_solution = []
        self.best_distance = float('inf')
        visited = [False] * self.problem.n
        visited[0] = True
        self._backtrack_tsp([0], visited, 0)
        return self.best_solution
    
    def _backtrack_tsp(self, path, visited, current_distance):
        if len(path) == self.problem.n:
            # Complete tour by returning to start
            total_distance = current_distance + self.problem.distance_matrix[path[-1]][path[0]]
            if total_distance < self.best_distance:
                self.best_distance = total_distance
                self.best_solution = path[:]
            return
        
        current_city = path[-1]
        for next_city in range(self.problem.n):
            if not visited[next_city]:
                new_distance = current_distance + self.problem.distance_matrix[current_city][next_city]
                # Pruning: if current distance already exceeds best, skip
                if new_distance < self.best_distance:
                    visited[next_city] = True
                    path.append(next_city)
                    self._backtrack_tsp(path, visited, new_distance)
                    path.pop()
                    visited[next_city] = False
    
    def _solve_matching(self):
        """Backtracking solution for matching"""
        if len(self.problem.edges) > 15:  # Too expensive for large instances
            from .greedy import GreedySolver
            return GreedySolver(self.problem).solve()
        
        self.best_solution = []
        self.best_weight = 0
        used_vertices = set()
        self._backtrack_matching([], used_vertices, 0, 0)
        return self.best_solution
    
    def _backtrack_matching(self, matching, used_vertices, edge_idx, current_weight):
        if edge_idx >= len(self.problem.edges):
            if current_weight > self.best_weight:
                self.best_weight = current_weight
                self.best_solution = matching[:]
            return
        
        # Try including current edge
        u, v, weight = self.problem.edges[edge_idx]
        if u not in used_vertices and v not in used_vertices:
            matching.append(edge_idx)
            used_vertices.add(u)
            used_vertices.add(v)
            self._backtrack_matching(matching, used_vertices, edge_idx + 1, current_weight + weight)
            matching.pop()
            used_vertices.remove(u)
            used_vertices.remove(v)
        
        # Try excluding current edge
        self._backtrack_matching(matching, used_vertices, edge_idx + 1, current_weight)
