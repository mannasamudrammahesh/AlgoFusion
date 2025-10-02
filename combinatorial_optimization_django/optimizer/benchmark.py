import time
import psutil
import uuid
from .problems.knapsack import KnapsackProblem
from .problems.tsp import TSPProblem
from .problems.graph_matching import GraphMatchingProblem
from .models import OptimizationResult, BenchmarkSession

def benchmark_single(SolverClass, problem):
    """Benchmark a single solver on a problem"""
    solver = SolverClass(problem)

    # Measure time and memory
    start_time = time.time()
    process = psutil.Process()
    mem_before = process.memory_info().rss / 1024 / 1024  # MB

    try:
        solution = solver.solve()
    except Exception as e:
        print(f"Solver {SolverClass.__name__} failed: {e}")
        return None

    mem_after = process.memory_info().rss / 1024 / 1024  # MB
    end_time = time.time()

    runtime_sec = end_time - start_time
    memory_mb = max(0, mem_after - mem_before)  # Ensure non-negative

    # Evaluate solution
    try:
        objective_value = problem.evaluate(solution)
    except:
        objective_value = 0

    return {
        "algorithm": SolverClass.__name__.replace('Solver', ''),
        "solution": solution,
        "objective_value": objective_value,
        "runtime_sec": runtime_sec,
        "memory_mb": memory_mb
    }

def benchmark_multiple(solver_classes, problem, problem_type):
    """Benchmark multiple solvers on the same problem"""
    results = []
    session_id = str(uuid.uuid4())
    
    # Create benchmark session
    problem_data = serialize_problem(problem, problem_type)
    session = BenchmarkSession.objects.create(
        session_id=session_id,
        problem_type=problem_type,
        problem_data=problem_data
    )
    
    for SolverClass in solver_classes:
        result = benchmark_single(SolverClass, problem)
        if result:
            results.append(result)
            
            # Save to database
            OptimizationResult.objects.create(
                problem_type=problem_type,
                algorithm=result["algorithm"],
                problem_data=problem_data,
                solution=result["solution"],
                objective_value=result["objective_value"],
                runtime_seconds=result["runtime_sec"],
                memory_mb=result["memory_mb"]
            )
    
    return results, session_id

def serialize_problem(problem, problem_type):
    """Serialize problem data for storage"""
    if problem_type == 'knapsack':
        return {
            'weights': problem.weights,
            'values': problem.values,
            'capacity': problem.capacity
        }
    elif problem_type == 'tsp':
        return {
            'cities': problem.cities,
            'n': problem.n
        }
    elif problem_type == 'matching':
        return {
            'edges': problem.edges,
            'vertices': list(problem.vertices)
        }
    return {}

def benchmark(SolverClass, weights, values, capacity):
    """Legacy function for backward compatibility"""
    problem = KnapsackProblem(weights, values, capacity)
    result = benchmark_single(SolverClass, problem)
    if result:
        return {
            "solution": result["solution"],
            "runtime_sec": result["runtime_sec"],
            "memory_mb": result["memory_mb"]
        }
    return {"solution": [], "runtime_sec": 0, "memory_mb": 0}
