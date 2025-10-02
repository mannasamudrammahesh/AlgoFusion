from ..problems.knapsack import KnapsackProblem
from ..problems.tsp import TSPProblem
from ..problems.graph_matching import GraphMatchingProblem

class DPSolver:
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
        """Dynamic programming solution for knapsack"""
        n = len(self.problem.values)
        W = self.problem.capacity
        dp = [[0]*(W+1) for _ in range(n+1)]

        for i in range(1, n+1):
            for w in range(W+1):
                if self.problem.weights[i-1] <= w:
                    dp[i][w] = max(dp[i-1][w],
                                   dp[i-1][w-self.problem.weights[i-1]] + self.problem.values[i-1])
                else:
                    dp[i][w] = dp[i-1][w]

        # reconstruct solution
        solution = []
        w = W
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                solution.append(i-1)
                w -= self.problem.weights[i-1]
        return solution
    
    def _solve_tsp(self):
        """Dynamic programming solution for TSP (Held-Karp algorithm)"""
        n = self.problem.n
        if n <= 1:
            return list(range(n))
        if n > 15:  # Too expensive for large instances
            from .greedy import GreedySolver
            return GreedySolver(self.problem).solve()
        
        # dp[mask][i] = minimum cost to visit all cities in mask ending at city i
        dp = {}
        parent = {}
        
        # Initialize: start from city 0
        for i in range(1, n):
            dp[(1 << i) | 1, i] = self.problem.distance_matrix[0][i]
            parent[(1 << i) | 1, i] = 0
        
        # Fill DP table
        for mask in range(1, 1 << n):
            if not (mask & 1):  # Must include city 0
                continue
            for u in range(n):
                if not (mask & (1 << u)):
                    continue
                for v in range(n):
                    if u == v or not (mask & (1 << v)):
                        continue
                    prev_mask = mask ^ (1 << u)
                    if (prev_mask, v) in dp:
                        cost = dp[prev_mask, v] + self.problem.distance_matrix[v][u]
                        if (mask, u) not in dp or cost < dp[mask, u]:
                            dp[mask, u] = cost
                            parent[mask, u] = v
        
        # Find minimum cost tour
        final_mask = (1 << n) - 1
        min_cost = float('inf')
        last_city = -1
        
        for i in range(1, n):
            if (final_mask, i) in dp:
                cost = dp[final_mask, i] + self.problem.distance_matrix[i][0]
                if cost < min_cost:
                    min_cost = cost
                    last_city = i
        
        # Reconstruct path
        if last_city == -1:
            return list(range(n))
        
        path = []
        mask = final_mask
        curr = last_city
        
        while curr != -1:
            path.append(curr)
            if (mask, curr) not in parent:
                break
            next_curr = parent[mask, curr]
            mask ^= (1 << curr)
            curr = next_curr
        
        path.reverse()
        return path
    
    def _solve_matching(self):
        """DP solution for matching (simplified - uses greedy for complex cases)"""
        # For small instances, we can use bitmask DP
        if len(self.problem.edges) > 20:
            from .greedy import GreedySolver
            return GreedySolver(self.problem).solve()
        
        # Use greedy approach for matching as DP is complex for general matching
        from .greedy import GreedySolver
        return GreedySolver(self.problem).solve()
