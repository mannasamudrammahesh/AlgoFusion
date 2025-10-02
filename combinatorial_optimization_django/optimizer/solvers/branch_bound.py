import heapq
from ..problems.knapsack import KnapsackProblem
from ..problems.tsp import TSPProblem
from ..problems.graph_matching import GraphMatchingProblem

class BranchBoundSolver:
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
        """Branch and bound solution for knapsack"""
        n = len(self.problem.values)
        queue = [([], 0, 0)]  # (solution, total_weight, total_value)
        best_solution = []
        best_value = 0

        while queue:
            solution, weight, value = queue.pop(0)
            if len(solution) == n:
                if value > best_value:
                    best_value = value
                    best_solution = solution
                continue
            index = len(solution)
            # include
            if weight + self.problem.weights[index] <= self.problem.capacity:
                queue.append((solution+[index], weight+self.problem.weights[index], value+self.problem.values[index]))
            # exclude
            queue.append((solution+[None], weight, value))

        # Remove Nones from solution
        return [i for i in best_solution if i is not None]
    
    def _solve_tsp(self):
        """Branch and bound solution for TSP"""
        if self.problem.n > 12:  # Too expensive for large instances
            from .greedy import GreedySolver
            return GreedySolver(self.problem).solve()
        
        # Use priority queue with lower bound estimation
        # State: (lower_bound, path, visited_set)
        queue = [(0, [0], {0})]
        best_distance = float('inf')
        best_tour = []
        
        while queue:
            bound, path, visited = heapq.heappop(queue)
            
            if bound >= best_distance:
                continue
                
            if len(path) == self.problem.n:
                # Complete tour
                total_distance = bound + self.problem.distance_matrix[path[-1]][path[0]]
                if total_distance < best_distance:
                    best_distance = total_distance
                    best_tour = path[:]
                continue
            
            current_city = path[-1]
            for next_city in range(self.problem.n):
                if next_city not in visited:
                    new_path = path + [next_city]
                    new_visited = visited | {next_city}
                    new_bound = bound + self.problem.distance_matrix[current_city][next_city]
                    
                    # Add lower bound estimation (minimum outgoing edges from unvisited cities)
                    if len(new_path) < self.problem.n:
                        remaining = set(range(self.problem.n)) - new_visited
                        for city in remaining:
                            min_edge = min(self.problem.distance_matrix[city][j] 
                                         for j in range(self.problem.n) if j != city)
                            new_bound += min_edge * 0.5  # Rough estimation
                    
                    if new_bound < best_distance:
                        heapq.heappush(queue, (new_bound, new_path, new_visited))
        
        return best_tour if best_tour else list(range(self.problem.n))
    
    def _solve_matching(self):
        """Branch and bound solution for matching"""
        if len(self.problem.edges) > 15:  # Too expensive for large instances
            from .greedy import GreedySolver
            return GreedySolver(self.problem).solve()
        
        # Use priority queue with upper bound (negative weight for max-heap simulation)
        # State: (-upper_bound, matching, used_vertices, edge_idx)
        queue = [(0, [], set(), 0)]
        best_weight = 0
        best_matching = []
        
        while queue:
            neg_bound, matching, used_vertices, edge_idx = heapq.heappop(queue)
            current_weight = -neg_bound
            
            if edge_idx >= len(self.problem.edges):
                if current_weight > best_weight:
                    best_weight = current_weight
                    best_matching = matching[:]
                continue
            
            # Try including current edge
            u, v, weight = self.problem.edges[edge_idx]
            if u not in used_vertices and v not in used_vertices:
                new_matching = matching + [edge_idx]
                new_used = used_vertices | {u, v}
                new_weight = current_weight + weight
                heapq.heappush(queue, (-new_weight, new_matching, new_used, edge_idx + 1))
            
            # Try excluding current edge
            heapq.heappush(queue, (neg_bound, matching, used_vertices, edge_idx + 1))
        
        return best_matching
