from django import forms

ALGO_CHOICES = [
    ('Greedy', 'Greedy'),
    ('Divide&Conquer', 'Divide & Conquer'),
    ('DynamicProgramming', 'Dynamic Programming'),
    ('Backtracking', 'Backtracking'),
    ('Branch&Bound', 'Branch & Bound'),
]

PROBLEM_CHOICES = [
    ('knapsack', 'Knapsack Problem'),
    ('tsp', 'Traveling Salesman Problem'),
    ('matching', 'Graph Matching Problem'),
]

INPUT_METHOD_CHOICES = [
    ('manual', 'Manual Input'),
    ('file', 'File Upload'),
    ('random', 'Random Generation'),
]

class ProblemForm(forms.Form):
    problem_type = forms.ChoiceField(
        label="Problem Type", 
        choices=PROBLEM_CHOICES
    )
    input_method = forms.ChoiceField(
        label="Input Method", 
        choices=INPUT_METHOD_CHOICES
    )
    algorithms = forms.MultipleChoiceField(
        label="Algorithms to Compare", 
        choices=ALGO_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        initial=['Greedy', 'DynamicProgramming']
    )
    
    # Knapsack fields
    weights = forms.CharField(
        label="Weights (comma separated)", 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g., 10,20,30'})
    )
    values = forms.CharField(
        label="Values (comma separated)", 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g., 60,100,120'})
    )
    capacity = forms.IntegerField(label="Capacity", required=False)
    
    # TSP fields
    cities = forms.CharField(
        label="Cities (x,y coordinates separated by semicolons)", 
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'e.g., 0,0;10,10;20,5', 'rows': 3})
    )
    
    # Graph Matching fields
    edges = forms.CharField(
        label="Edges (u,v,weight separated by semicolons)", 
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'e.g., 0,1,5;1,2,3;0,2,8', 'rows': 3})
    )
    
    # File upload
    data_file = forms.FileField(
        label="Data File", 
        required=False,
        help_text="Upload CSV, JSON, or TXT file with problem data"
    )
    
    # Random generation
    random_size = forms.IntegerField(
        label="Problem Size", 
        required=False, 
        initial=10,
        help_text="Number of items/cities/vertices to generate"
    )

class KnapsackForm(forms.Form):
    weights = forms.CharField(label="Weights (comma separated)", required=True)
    values = forms.CharField(label="Values (comma separated)", required=True)
    capacity = forms.IntegerField(label="Capacity", required=True)
    algorithm = forms.ChoiceField(label="Algorithm", choices=ALGO_CHOICES)
