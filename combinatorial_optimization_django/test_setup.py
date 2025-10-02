#!/usr/bin/env python
"""
Quick test script to verify the setup is working correctly
"""

import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        import django
        print(f"✓ Django {django.get_version()} imported successfully")
        
        # Set up Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'combinatorial_optimization_django.settings')
        django.setup()
        
        from optimizer.problems.knapsack import KnapsackProblem
        print("✓ KnapsackProblem imported successfully")
        
        from optimizer.problems.tsp import TSPProblem
        print("✓ TSPProblem imported successfully")
        
        from optimizer.problems.graph_matching import GraphMatchingProblem
        print("✓ GraphMatchingProblem imported successfully")
        
        from optimizer.solvers.greedy import GreedySolver
        print("✓ GreedySolver imported successfully")
        
        from optimizer.solvers.dynamic_programming import DPSolver
        print("✓ DPSolver imported successfully")
        
        from optimizer.solvers.backtracking import BacktrackingSolver
        print("✓ BacktrackingSolver imported successfully")
        
        from optimizer.solvers.branch_bound import BranchBoundSolver
        print("✓ BranchBoundSolver imported successfully")
        
        from optimizer.solvers.divide_conquer import DivideConquerSolver
        print("✓ DivideConquerSolver imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_knapsack_solver():
    """Test a simple knapsack problem"""
    print("\nTesting Knapsack Solver...")
    try:
        from optimizer.problems.knapsack import KnapsackProblem
        from optimizer.solvers.greedy import GreedySolver
        
        # Create a simple problem
        problem = KnapsackProblem([10, 20, 30], [60, 100, 120], 50)
        solver = GreedySolver(problem)
        solution = solver.solve()
        
        print(f"✓ Knapsack problem solved: {solution}")
        print(f"  Total value: {problem.evaluate(solution)}")
        return True
    except Exception as e:
        print(f"✗ Knapsack solver error: {e}")
        return False

def test_tsp_solver():
    """Test a simple TSP problem"""
    print("\nTesting TSP Solver...")
    try:
        from optimizer.problems.tsp import TSPProblem
        from optimizer.solvers.greedy import GreedySolver
        
        # Create a simple problem
        cities = [(0, 0), (10, 10), (20, 5), (15, 20)]
        problem = TSPProblem(cities)
        solver = GreedySolver(problem)
        solution = solver.solve()
        
        print(f"✓ TSP problem solved: {solution}")
        print(f"  Tour distance: {problem.evaluate(solution):.2f}")
        return True
    except Exception as e:
        print(f"✗ TSP solver error: {e}")
        return False

def test_matching_solver():
    """Test a simple matching problem"""
    print("\nTesting Graph Matching Solver...")
    try:
        from optimizer.problems.graph_matching import GraphMatchingProblem
        from optimizer.solvers.greedy import GreedySolver
        
        # Create a simple problem
        edges = [(0, 1, 5), (1, 2, 3), (0, 2, 8), (2, 3, 4)]
        problem = GraphMatchingProblem(edges)
        solver = GreedySolver(problem)
        solution = solver.solve()
        
        print(f"✓ Matching problem solved: {solution}")
        print(f"  Total weight: {problem.evaluate(solution):.2f}")
        return True
    except Exception as e:
        print(f"✗ Matching solver error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Combinatorial Optimization Framework - Setup Test")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Knapsack Solver", test_knapsack_solver()))
    results.append(("TSP Solver", test_tsp_solver()))
    results.append(("Matching Solver", test_matching_solver()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("=" * 60)
    if all_passed:
        print("✓ All tests passed! Setup is working correctly.")
        print("\nYou can now run: python manage.py runserver")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        print("\nMake sure you have:")
        print("1. Activated the virtual environment")
        print("2. Installed all dependencies: pip install -r requirements.txt")
        print("3. Run migrations: python manage.py migrate")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
