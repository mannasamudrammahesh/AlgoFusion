# Setup Guide

## Quick Start

Follow these steps to get the Combinatorial Optimization Framework up and running:

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning)

### 2. Installation Steps

#### Step 1: Navigate to Project Directory
```bash
cd combinatorial_optimization_django
```

#### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

#### Step 3: Activate Virtual Environment

**Windows (CMD):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

#### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 5: Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Step 6: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

#### Step 7: Start Development Server
```bash
python manage.py runserver
```

#### Step 8: Access the Application
Open your web browser and navigate to:
```
http://127.0.0.1:8000/
```

## Troubleshooting

### Issue: "No module named 'django'"
**Solution:** Make sure you've activated the virtual environment and installed dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Table doesn't exist" errors
**Solution:** Run migrations:
```bash
python manage.py migrate
```

### Issue: Static files not loading
**Solution:** Collect static files:
```bash
python manage.py collectstatic
```

### Issue: Port 8000 already in use
**Solution:** Use a different port:
```bash
python manage.py runserver 8080
```

## Testing the Application

### Test with Sample Data

1. **Knapsack Problem:**
   - Weights: `10,20,30`
   - Values: `60,100,120`
   - Capacity: `50`

2. **TSP Problem:**
   - Cities: `0,0;10,10;20,5;15,20`

3. **Graph Matching:**
   - Edges: `0,1,5;1,2,3;0,2,8;2,3,4`

## Development

### Running Tests
```bash
python manage.py test optimizer
```

### Creating Migrations
```bash
python manage.py makemigrations optimizer
```

### Accessing Admin Panel
1. Create a superuser (if not already done)
2. Navigate to: `http://127.0.0.1:8000/admin/`
3. Login with superuser credentials

## Production Deployment

For production deployment, please:
1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Use a production-grade database (PostgreSQL recommended)
4. Set up proper static file serving
5. Use a WSGI server like Gunicorn
6. Configure HTTPS

## Additional Resources

- Django Documentation: https://docs.djangoproject.com/
- Bootstrap Documentation: https://getbootstrap.com/docs/
- Chart.js Documentation: https://www.chartjs.org/docs/

## Support

If you encounter any issues, please check:
1. Python version compatibility
2. Virtual environment activation
3. All dependencies installed
4. Database migrations completed
