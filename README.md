# Assignment
# Django Project Setup Guide

## Prerequisites
- Python 3.x installed
- Virtual environment package (e.g., `venv`, `virtualenv`) installed
- Git installed

## Steps to Set Up and Run the Project

1. Clone the Repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>

2. Create and Activate the Virtual Environment:

    On Windows:
        python -m venv venv
        venv\Scripts\activate

    On macOS/Linux:
        python3 -m venv venv
        source venv/bin/activate

3. Install Required Dependencies:
    pip install -r requirements.txt


4. Apply Migrations:
    python manage.py makemigrations
    python manage.py migrate


5. Run the Development Server:
    python manage.py runserver

6. Access the Application: Open your browser and navigate to http://127.0.0.1:8000/.
7. Postman collection






