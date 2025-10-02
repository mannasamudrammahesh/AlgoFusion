from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
import json
import csv
import io
from .forms import ProblemForm, KnapsackForm
from .problems.knapsack import KnapsackProblem
from .problems.tsp import TSPProblem
from .problems.graph_matching import GraphMatchingProblem
from .solvers.greedy import GreedySolver
from .solvers.divide_conquer import DivideConquerSolver
from .solvers.dynamic_programming import DPSolver
from .solvers.backtracking import BacktrackingSolver
from .solvers.branch_bound import BranchBoundSolver
from .benchmark import benchmark_multiple, benchmark_single
from .models import OptimizationResult, BenchmarkSession

SOLVERS = {
    "Greedy": GreedySolver,
    "Divide&Conquer": DivideConquerSolver,
    "DynamicProgramming": DPSolver,
    "Backtracking": BacktrackingSolver,
    "Branch&Bound": BranchBoundSolver,
}

def index(request):
    if request.method == "POST":
        form = ProblemForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Parse problem data
                problem = parse_problem_data(form.cleaned_data)
                if not problem:
                    messages.error(request, "Failed to parse problem data")
                    return render(request, "index.html", {"form": form})
                
                # Get selected algorithms
                selected_algorithms = form.cleaned_data["algorithms"]
                solver_classes = [SOLVERS[alg] for alg in selected_algorithms]
                
                # Run benchmarks
                results, session_id = benchmark_multiple(
                    solver_classes, 
                    problem, 
                    form.cleaned_data["problem_type"]
                )
                
                if not results:
                    messages.error(request, "No algorithms completed successfully")
                    return render(request, "index.html", {"form": form})
                
                # Redirect to results page
                return redirect('results', session_id=session_id)
                
            except Exception as e:
                messages.error(request, f"Error processing request: {str(e)}")
                return render(request, "index.html", {"form": form})
    else:
        form = ProblemForm()

    return render(request, "index.html", {"form": form})

def results(request, session_id):
    try:
        session = BenchmarkSession.objects.get(session_id=session_id)
        results = OptimizationResult.objects.filter(
            problem_type=session.problem_type,
            created_at__gte=session.created_at
        ).order_by('created_at')
        
        # Prepare data for charts
        chart_data = prepare_chart_data(results)
        
        context = {
            'session': session,
            'results': results,
            'chart_data': json.dumps(chart_data),
            'problem_type': session.problem_type
        }
        return render(request, "results.html", context)
    except BenchmarkSession.DoesNotExist:
        messages.error(request, "Session not found")
        return redirect('index')

def parse_problem_data(data):
    """Parse problem data from form"""
    problem_type = data["problem_type"]
    input_method = data["input_method"]
    
    try:
        if input_method == "manual":
            return parse_manual_input(data, problem_type)
        elif input_method == "file":
            return parse_file_input(data, problem_type)
        elif input_method == "random":
            return generate_random_problem(data, problem_type)
    except Exception as e:
        print(f"Error parsing problem data: {e}")
        return None

def parse_manual_input(data, problem_type):
    """Parse manual input data"""
    if problem_type == "knapsack":
        weights = [int(x.strip()) for x in data["weights"].split(",") if x.strip()]
        values = [int(x.strip()) for x in data["values"].split(",") if x.strip()]
        capacity = data["capacity"]
        return KnapsackProblem(weights, values, capacity)
    
    elif problem_type == "tsp":
        cities_str = data["cities"]
        cities = []
        for city_str in cities_str.split(";"):
            if city_str.strip():
                x, y = map(float, city_str.strip().split(","))
                cities.append((x, y))
        return TSPProblem(cities)
    
    elif problem_type == "matching":
        edges_str = data["edges"]
        edges = []
        for edge_str in edges_str.split(";"):
            if edge_str.strip():
                u, v, w = edge_str.strip().split(",")
                edges.append((int(u), int(v), float(w)))
        return GraphMatchingProblem(edges)

def parse_file_input(data, problem_type):
    """Parse file input data"""
    file = data["data_file"]
    if not file:
        return None
    
    content = file.read().decode('utf-8')
    
    if file.name.endswith('.json'):
        json_data = json.loads(content)
        return parse_json_data(json_data, problem_type)
    elif file.name.endswith('.csv'):
        return parse_csv_data(content, problem_type)
    else:
        return parse_text_data(content, problem_type)

def parse_json_data(json_data, problem_type):
    """Parse JSON data"""
    if problem_type == "knapsack":
        return KnapsackProblem(
            json_data["weights"], 
            json_data["values"], 
            json_data["capacity"]
        )
    elif problem_type == "tsp":
        return TSPProblem(json_data["cities"])
    elif problem_type == "matching":
        return GraphMatchingProblem(json_data["edges"])

def parse_csv_data(content, problem_type):
    """Parse CSV data"""
    reader = csv.reader(io.StringIO(content))
    rows = list(reader)
    
    if problem_type == "knapsack":
        weights = [int(x) for x in rows[0]]
        values = [int(x) for x in rows[1]]
        capacity = int(rows[2][0])
        return KnapsackProblem(weights, values, capacity)
    elif problem_type == "tsp":
        cities = [(float(row[0]), float(row[1])) for row in rows]
        return TSPProblem(cities)
    elif problem_type == "matching":
        edges = [(int(row[0]), int(row[1]), float(row[2])) for row in rows]
        return GraphMatchingProblem(edges)

def parse_text_data(content, problem_type):
    """Parse plain text data"""
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    if problem_type == "knapsack":
        weights = [int(x) for x in lines[0].split()]
        values = [int(x) for x in lines[1].split()]
        capacity = int(lines[2])
        return KnapsackProblem(weights, values, capacity)
    elif problem_type == "tsp":
        cities = []
        for line in lines:
            x, y = map(float, line.split())
            cities.append((x, y))
        return TSPProblem(cities)
    elif problem_type == "matching":
        edges = []
        for line in lines:
            u, v, w = line.split()
            edges.append((int(u), int(v), float(w)))
        return GraphMatchingProblem(edges)

def generate_random_problem(data, problem_type):
    """Generate random problem instance"""
    size = data["random_size"]
    
    if problem_type == "knapsack":
        return KnapsackProblem.generate_random_instance(size)
    elif problem_type == "tsp":
        return TSPProblem.generate_random_instance(size)
    elif problem_type == "matching":
        return GraphMatchingProblem.generate_random_instance(size)

def prepare_chart_data(results):
    """Prepare data for visualization charts"""
    algorithms = []
    runtimes = []
    memories = []
    objectives = []
    
    for result in results:
        algorithms.append(result.algorithm)
        runtimes.append(result.runtime_seconds)
        memories.append(result.memory_mb)
        objectives.append(result.objective_value)
    
    return {
        'algorithms': algorithms,
        'runtimes': runtimes,
        'memories': memories,
        'objectives': objectives
    }

def legacy_index(request):
    """Legacy knapsack-only interface"""
    if request.method == "POST":
        form = KnapsackForm(request.POST)
        if form.is_valid():
            weights = list(map(int, form.cleaned_data["weights"].split(",")))
            values = list(map(int, form.cleaned_data["values"].split(",")))
            capacity = form.cleaned_data["capacity"]
            algorithm = form.cleaned_data["algorithm"]

            SolverClass = SOLVERS[algorithm]
            problem = KnapsackProblem(weights, values, capacity)
            result = benchmark_single(SolverClass, problem)
            
            if result:
                context = {
                    "form": form,
                    "algorithm": algorithm,
                    "items": result["solution"],
                    "value": result["objective_value"],
                    "runtime": result["runtime_sec"],
                    "memory": result["memory_mb"],
                }
                return render(request, "result.html", context)
    else:
        form = KnapsackForm()

    return render(request, "legacy.html", {"form": form})
