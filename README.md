# Combinatorial Optimization Framework

A comprehensive Django-based web application for solving and comparing various combinatorial optimization problems using multiple algorithmic strategies.

## 🚀 Features

- **Multiple Problem Types**
  - Knapsack Problem
  - Traveling Salesman Problem (TSP)
  - Graph Matching Problem

- **Multiple Solving Algorithms**
  - Greedy Algorithm
  - Divide & Conquer
  - Dynamic Programming
  - Backtracking
  - Branch & Bound

- **Flexible Input Methods**
  - Manual input via web forms
  - File upload (CSV, JSON, TXT)
  - Random problem generation

- **Performance Benchmarking**
  - Compare multiple algorithms simultaneously
  - Visualize runtime, memory usage, and solution quality
  - Interactive charts using Chart.js

- **Legacy Mode**
  - Backward-compatible single-algorithm solver
  - Focused on Knapsack problem

## 📋 Requirements

- Python 3.8+
- Django 4.0+
- Modern web browser with JavaScript enabled

## 🛠️ Installation

### Quick Setup

1. **Navigate to the project directory**
   ```bash
   cd combinatorial_optimization_django
   ```

2. **Create and activate virtual environment**
   
   Windows (CMD):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   Windows (PowerShell):
   ```bash
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```
   
   Linux/Mac:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Test the setup (optional)**
   ```bash
   python test_setup.py
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   Open your browser and navigate to: `http://127.0.0.1:8000/`

For detailed setup instructions, see [SETUP.md](combinatorial_optimization_django/SETUP.md)

## 📖 Usage

### Main Interface

1. **Select Problem Type**: Choose from Knapsack, TSP, or Graph Matching
2. **Choose Input Method**: Manual, File Upload, or Random Generation
3. **Select Algorithms**: Pick one or more algorithms to compare
4. **Enter Problem Data**: Provide the problem instance data
5. **Run Optimization**: Click the button to execute and compare algorithms

### Input Formats

#### Knapsack Problem
- **Weights**: Comma-separated integers (e.g., `10,20,30`)
- **Values**: Comma-separated integers (e.g., `60,100,120`)
- **Capacity**: Single integer (e.g., `50`)

#### Traveling Salesman Problem
- **Cities**: Semicolon-separated x,y coordinates (e.g., `0,0;10,10;20,5;15,20`)

#### Graph Matching Problem
- **Edges**: Semicolon-separated u,v,weight tuples (e.g., `0,1,5;1,2,3;0,2,8;2,3,4`)

### File Upload Formats

#### JSON Format
```json
{
  "weights": [10, 20, 30],
  "values": [60, 100, 120],
  "capacity": 50
}
```

#### CSV Format
```csv
10,20,30
60,100,120
50
```

#### Text Format
```
10 20 30
60 100 120
50
```

## 🏗️ Project Structure

```
combinatorial_optimization_django/
├── combinatorial_optimization_django/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── optimizer/
│   ├── problems/
│   │   ├── knapsack.py
│   │   ├── tsp.py
│   │   └── graph_matching.py
│   ├── solvers/
│   │   ├── greedy.py
│   │   ├── divide_conquer.py
│   │   ├── dynamic_programming.py
│   │   ├── backtracking.py
│   │   └── branch_bound.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── results.html
│   │   ├── legacy.html
│   │   └── result.html
│   ├── static/
│   │   └── style.css
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── benchmark.py
│   └── urls.py
├── manage.py
└── db.sqlite3
```

## 🔧 Algorithm Details

### Greedy Algorithm
- Fast execution time
- May not always find optimal solution
- Good for quick approximations

### Divide & Conquer
- Breaks problem into smaller subproblems
- Efficient for certain problem structures
- Moderate complexity

### Dynamic Programming
- Guarantees optimal solution
- Higher memory usage
- Excellent for overlapping subproblems

### Backtracking
- Explores all possible solutions
- Can be slow for large problems
- Guarantees finding optimal solution

### Branch & Bound
- Prunes search space intelligently
- Balances speed and optimality
- Good for medium-sized problems

## 📊 Performance Metrics

The application tracks and displays:
- **Runtime**: Execution time in seconds
- **Memory Usage**: Peak memory consumption in MB
- **Solution Quality**: Objective value (maximization/minimization)
- **Solution Details**: Actual solution representation

## 🎨 User Interface

The application features a clean, professional design with:
- Responsive Bootstrap 5 layout
- Interactive forms with dynamic field visibility
- Real-time chart visualizations
- Mobile-friendly interface
- Intuitive navigation

## 🧪 Testing

To run tests:
```bash
python manage.py test optimizer
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is open-source and available under the MIT License.

## 👥 Authors

- Combinatorial Optimization Framework Team

## 🐛 Known Issues

- Large problem instances (>1000 items) may cause performance degradation
- Some algorithms may timeout on very complex problems

## 🔮 Future Enhancements

- [ ] Add more optimization problems (Set Cover, Bin Packing, etc.)
- [ ] Implement parallel algorithm execution
- [ ] Add solution visualization (graphs, charts)
- [ ] Export results to PDF
- [ ] User authentication and saved sessions
- [ ] API endpoints for programmatic access

## 📞 Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

## 🙏 Acknowledgments

- Django Framework
- Bootstrap 5
- Chart.js
- Python Community
