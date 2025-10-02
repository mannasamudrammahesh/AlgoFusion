from django.db import models
import json

class OptimizationResult(models.Model):
    PROBLEM_TYPES = [
        ('knapsack', 'Knapsack Problem'),
        ('tsp', 'Traveling Salesman Problem'),
        ('matching', 'Graph Matching Problem'),
    ]
    
    problem_type = models.CharField(max_length=20, choices=PROBLEM_TYPES)
    algorithm = models.CharField(max_length=50)
    problem_data = models.JSONField()  # Store problem instance data
    solution = models.JSONField()  # Store solution
    objective_value = models.FloatField()  # Solution quality
    runtime_seconds = models.FloatField()
    memory_mb = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.problem_type} - {self.algorithm} - {self.created_at}"

class BenchmarkSession(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    problem_type = models.CharField(max_length=20)
    problem_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Session {self.session_id} - {self.problem_type}"
