# Django Backend

This is the backend for the Schedule Builder web application, built using **Django**.

---

## 🧩 Requirements

- **Python 3.13** or higher
- **Pipenv** for virtual environment and dependency management

---

## ⚙️ Setup Instructions

### 1. Clone the repository

git clone <your-repo-url>
cd <your-project-folder>

### 2. Install Pipenv (if not already installed)

pip install pipenv

### 3. Create and activate the virtual environment

pipenv shell

### 4. Install dependencies

pipenv install

### 5. Open the Project in VS Code

code .

### 6. Select the Correct Python Interpreter in VS Code

Open the Command Palette (Ctrl + Shift + P or Cmd + Shift + P on Mac).
Search for “Python: Select Interpreter”.
Choose the interpreter that points to your Pipenv virtual environment.
It should look something like:
.venv\Scripts\python.exe
or
...\.virtualenvs\<project-name>-<hash>\Scripts\python.exe
This ensures that VS Code runs your project with the correct environment.

### 7. Run the Development Server

python manage.py runserver

Your Django server will start at:
http://127.0.0.1:8000/


# To remove warnings about unapplied migrations, do the following:
CTRL + C // stop the server if it is running
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
