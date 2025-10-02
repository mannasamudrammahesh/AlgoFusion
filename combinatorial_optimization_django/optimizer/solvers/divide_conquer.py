from ..problems.knapsack import KnapsackProblem
from ..problems.tsp import TSPProblem
from ..problems.graph_matching import GraphMatchingProblem

class DivideConquerSolver:
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
        """Divide and conquer for knapsack (simplified approach)"""
        n = len(self.problem.values)
        if n == 0:
            return []
        if n == 1:
            return [0] if self.problem.weights[0] <= self.problem.capacity else []
        
        # Divide items into two halves
        mid = n // 2
        left_items = list(range(mid))
        right_items = list(range(mid, n))
        
        # Generate all possible combinations for each half
        left_combinations = self._generate_combinations(left_items)
        right_combinations = self._generate_combinations(right_items)
        
        # Find best combination
        best_value = 0
        best_solution = []
        
        for left_combo in left_combinations:
            left_weight = sum(self.problem.weights[i] for i in left_combo)
            left_value = sum(self.problem.values[i] for i in left_combo)
            remaining_capacity = self.problem.capacity - left_weight
            
            if remaining_capacity >= 0:
                # Find best right combination that fits
                best_right = []
                best_right_value = 0
                
                for right_combo in right_combinations:
                    right_weight = sum(self.problem.weights[i] for i in right_combo)
                    right_value = sum(self.problem.values[i] for i in right_combo)
                    
                    if right_weight <= remaining_capacity and right_value > best_right_value:
                        best_right = right_combo
                        best_right_value = right_value
                
                total_value = left_value + best_right_value
                if total_value > best_value:
                    best_value = total_value
                    best_solution = left_combo + best_right
        
        return best_solution
    
    def _generate_combinations(self, items):
        """Generate all possible combinations of items"""
        if not items:
            return [[]]
        
        combinations = []
        first = items[0]
        rest = items[1:]
        
        # Combinations without first item
        for combo in self._generate_combinations(rest):
            combinations.append(combo)
        
        # Combinations with first item
        for combo in self._generate_combinations(rest):
            combinations.append([first] + combo)
        
        return combinations
    
    def _solve_tsp(self):
        """Divide and conquer for TSP (simplified - uses nearest neighbor)"""
        # For TSP, divide and conquer is complex, so we use a heuristic approach
        if self.problem.n <= 1:
            return list(range(self.problem.n))
        
        # Divide cities into clusters and solve each cluster
        if self.problem.n <= 6:
            # Small instance - use brute force
            from .backtracking import BacktrackingSolver
            return BacktrackingSolver(self.problem).solve()
        else:
            # Large instance - use greedy
            from .greedy import GreedySolver
            return GreedySolver(self.problem).solve()
    
    def _solve_matching(self):
        """Divide and conquer for matching"""
        if len(self.problem.edges) <= 10:
            # Small instance - use exact algorithm
            from .backtracking import BacktrackingSolver
            return BacktrackingSolver(self.problem).solve()
        else:
            # Large instance - use greedy
            from .greedy import GreedySolver
            return GreedySolver(self.problem).solve()
