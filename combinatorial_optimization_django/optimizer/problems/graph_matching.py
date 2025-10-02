import random
from typing import List, Tuple, Set

class GraphMatchingProblem:
    """Maximum Weight Matching Problem implementation"""
    
    def __init__(self, edges: List[Tuple[int, int, float]]):
        """
        Initialize with list of edges (u, v, weight)
        """
        self.edges = edges
        self.vertices = set()
        for u, v, _ in edges:
            self.vertices.add(u)
            self.vertices.add(v)
        self.n_vertices = len(self.vertices)
    
    def is_valid_matching(self, matching: List[int]) -> bool:
        """Check if the matching is valid (no vertex appears twice)"""
        used_vertices = set()
        for edge_idx in matching:
            if edge_idx >= len(self.edges):
                return False
            u, v, _ = self.edges[edge_idx]
            if u in used_vertices or v in used_vertices:
                return False
            used_vertices.add(u)
            used_vertices.add(v)
        return True
    
    def calculate_matching_weight(self, matching: List[int]) -> float:
        """Calculate total weight of matching"""
        if not self.is_valid_matching(matching):
            return 0
        
        total_weight = 0
        for edge_idx in matching:
            _, _, weight = self.edges[edge_idx]
            total_weight += weight
        return total_weight
    
    def evaluate(self, solution: List[int]) -> float:
        """Evaluate solution quality (higher is better for matching)"""
        return self.calculate_matching_weight(solution)
    
    @classmethod
    def generate_random_instance(cls, num_vertices: int, edge_probability: float = 0.3):
        """Generate random graph matching instance"""
        edges = []
        edge_id = 0
        for u in range(num_vertices):
            for v in range(u + 1, num_vertices):
                if random.random() < edge_probability:
                    weight = random.uniform(1, 100)
                    edges.append((u, v, weight))
        return cls(edges)