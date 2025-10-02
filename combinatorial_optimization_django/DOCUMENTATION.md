# Project Documentation

## Overview

The Combinatorial Optimization Framework is a Django-based web application that allows users to solve and compare various combinatorial optimization problems using multiple algorithmic strategies.

## Architecture

### Project Structure

```
combinatorial_optimization_django/
├── combinatorial_optimization_django/  # Main Django project
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # Main URL configuration
│   └── wsgi.py                        # WSGI configuration
├── optimizer/                         # Main application
│   ├── problems/                      # Problem implementations
│   │   ├── knapsack.py               # Knapsack problem
│   │   ├── tsp.py                    # TSP problem
│   │   └── graph_matching.py         # Graph matching problem
│   ├── solvers/                       # Algorithm implementations
│   │   ├── greedy.py                 # Greedy algorithm
│   │   ├── dynamic_programming.py    # DP algorithm
│   │   ├── backtracking.py           # Backtracking algorithm
│   │   ├── branch_bound.py           # Branch & Bound algorithm
│   │   └── divide_conquer.py         # Divide & Conquer algorithm
│   ├── templates/                     # HTML templates
│   │   ├── base.html                 # Base template
│   │   ├── index.html                # Main interface
│   │   ├── results.html              # Results page
│   │   ├── legacy.html               # Legacy interface
│   │   └── result.html               # Single result page
│   ├── static/                        # Static files
│   │   └── style.css                 # Custom CSS
│   ├── models.py                      # Database models
│   ├── views.py                       # View functions
│   ├── forms.py                       # Form definitions
│   ├── benchmark.py                   # Benchmarking utilities
│   └── urls.py                        # App URL configuration
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
└── db.sqlite3                         # SQLite database
```

## Components

### 1. Problems

#### Knapsack Problem
- **File:** `optimizer/problems/knapsack.py`
- **Description:** Given items with weights and values, maximize value within capacity constraint
- **Input:** weights (list), values (list), capacity (int)
- **Output:** List of selected item indices

#### Traveling Salesman Problem (TSP)
- **File:** `optimizer/problems/tsp.py`
- **Description:** Find shortest tour visiting all cities exactly once
- **Input:** List of city coordinates (x, y)
- **Output:** Tour as list of city indices

#### Graph Matching Problem
- **File:** `optimizer/problems/graph_matching.py`
- **Description:** Find maximum weight matching in a graph
- **Input:** List of edges (u, v, weight)
- **Output:** List of selected edge indices

### 2. Solvers

#### Greedy Algorithm
- **Complexity:** O(n log n)
- **Optimality:** Not guaranteed
- **Best for:** Quick approximations, large instances
- **Strategy:** Makes locally optimal choices

#### Dynamic Programming
- **Complexity:** O(n * W) for knapsack, O(n² * 2ⁿ) for TSP
- **Optimality:** Guaranteed for knapsack
- **Best for:** Medium-sized instances with overlapping subproblems
- **Strategy:** Builds solution from smaller subproblems

#### Backtracking
- **Complexity:** O(2ⁿ) worst case
- **Optimality:** Guaranteed
- **Best for:** Small instances, exact solutions
- **Strategy:** Explores all possibilities with pruning

#### Branch & Bound
- **Complexity:** Varies, typically better than backtracking
- **Optimality:** Guaranteed
- **Best for:** Medium instances, exact solutions
- **Strategy:** Uses bounds to prune search space

#### Divide & Conquer
- **Complexity:** Varies by problem
- **Optimality:** Not guaranteed
- **Best for:** Problems with natural divide points
- **Strategy:** Splits problem into independent subproblems

### 3. Database Models

#### OptimizationResult
Stores individual algorithm results:
- `problem_type`: Type of problem (knapsack, tsp, matching)
- `algorithm`: Algorithm name
- `problem_data`: JSON field with problem instance
- `solution`: JSON field with solution
- `objective_value`: Solution quality metric
- `runtime_seconds`: Execution time
- `memory_mb`: Memory usage
- `created_at`: Timestamp

#### BenchmarkSession
Groups related optimization runs:
- `session_id`: Unique session identifier
- `problem_type`: Type of problem
- `problem_data`: JSON field with problem instance
- `created_at`: Timestamp

### 4. Views

#### index (Main Interface)
- **URL:** `/`
- **Method:** GET, POST
- **Purpose:** Main problem input and algorithm selection
- **Features:**
  - Problem type selection
  - Input method selection (manual, file, random)
  - Algorithm selection (multiple)
  - Dynamic form fields

#### results (Results Page)
- **URL:** `/results/<session_id>/`
- **Method:** GET
- **Purpose:** Display comparison results
- **Features:**
  - Performance charts (runtime, memory, quality)
  - Detailed results table
  - Problem data display
  - Export functionality

#### legacy_index (Legacy Interface)
- **URL:** `/legacy/`
- **Method:** GET, POST
- **Purpose:** Backward-compatible single-algorithm interface
- **Features:**
  - Knapsack-only
  - Single algorithm selection
  - Simple result display

### 5. Forms

#### ProblemForm
Main form for problem input:
- `problem_type`: Choice field (knapsack, tsp, matching)
- `input_method`: Choice field (manual, file, random)
- `algorithms`: Multiple choice field
- Problem-specific fields (weights, values, cities, edges, etc.)
- `data_file`: File upload field
- `random_size`: Integer field for random generation

#### KnapsackForm
Legacy form for knapsack:
- `weights`: Comma-separated string
- `values`: Comma-separated string
- `capacity`: Integer
- `algorithm`: Choice field

## API Reference

### Benchmark Functions

#### `benchmark_single(SolverClass, problem)`
Benchmarks a single solver on a problem.

**Parameters:**
- `SolverClass`: Solver class to use
- `problem`: Problem instance

**Returns:**
- Dictionary with solution, objective_value, runtime_sec, memory_mb

#### `benchmark_multiple(solver_classes, problem, problem_type)`
Benchmarks multiple solvers on the same problem.

**Parameters:**
- `solver_classes`: List of solver classes
- `problem`: Problem instance
- `problem_type`: String ('knapsack', 'tsp', 'matching')

**Returns:**
- Tuple of (results list, session_id)

### Problem Methods

All problem classes implement:
- `evaluate(solution)`: Calculate solution quality
- `generate_random_instance(size)`: Create random problem instance

### Solver Methods

All solver classes implement:
- `__init__(problem)`: Initialize with problem instance
- `solve()`: Solve the problem and return solution

## Frontend

### Technologies
- **Bootstrap 5:** Responsive UI framework
- **Chart.js:** Data visualization
- **Vanilla JavaScript:** Form interactions

### Key Features
- Responsive design (mobile-friendly)
- Dynamic form fields based on selections
- Real-time chart rendering
- Clean, professional styling (no glassmorphism)

### CSS Classes
- `.navbar`: Fixed top navigation
- `.card`: Content containers
- `.feature-card`: Problem type cards
- `.form-control`: Form inputs
- `.btn-primary`: Primary action buttons

## Performance Considerations

### Algorithm Selection Guidelines

| Problem Size | Recommended Algorithms |
|--------------|------------------------|
| Small (< 10) | All algorithms |
| Medium (10-20) | Greedy, DP, Branch & Bound |
| Large (> 20) | Greedy, Divide & Conquer |

### Optimization Tips
1. Use greedy for quick approximations
2. Use DP for guaranteed optimal solutions (medium size)
3. Limit backtracking to small instances
4. Consider problem structure when choosing algorithm

## Testing

### Manual Testing
1. Test each problem type with sample data
2. Verify all algorithms complete successfully
3. Check chart rendering
4. Test file upload functionality
5. Verify random generation

### Automated Testing
Run the test setup script:
```bash
python test_setup.py
```

## Deployment

### Development
```bash
python manage.py runserver
```

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use production database (PostgreSQL)
- [ ] Set up static file serving
- [ ] Configure HTTPS
- [ ] Use WSGI server (Gunicorn)
- [ ] Set up logging
- [ ] Configure environment variables

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure virtual environment is activated
   - Install all dependencies: `pip install -r requirements.txt`

2. **Database Errors**
   - Run migrations: `python manage.py migrate`
   - Delete db.sqlite3 and re-run migrations if needed

3. **Static Files Not Loading**
   - Check STATIC_URL in settings.py
   - Run `python manage.py collectstatic` for production

4. **Algorithm Timeout**
   - Reduce problem size
   - Use faster algorithms (Greedy)
   - Check algorithm complexity limits

## Future Enhancements

- [ ] Add more optimization problems
- [ ] Implement parallel algorithm execution
- [ ] Add solution visualization
- [ ] Export results to PDF
- [ ] User authentication
- [ ] API endpoints
- [ ] Real-time progress tracking
- [ ] Algorithm parameter tuning
- [ ] Batch processing
- [ ] Cloud deployment support

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
- Check documentation
- Review troubleshooting section
- Open an issue on GitHub
- Contact development team
