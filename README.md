# Fatmug


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

python3.9 or latest

### Installing

A step-by-step series of examples that tell you how to get a development environment running.

1. Clone the repository:

    ```bash
    git clone https://github.com/shubh8383/fatmug.git
    cd fatmug
    ```

2. Create a virtual environment (recommended):
    - On Windows:
    ```bash
    python -m venv venv
    or 
    py -m venv venv
    ```
    - On Unix or MacOS:
    ```bash
    python3 -m venv venv
    ```
    

3. Activate the virtual environment:

    - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    - On Unix or MacOS:

        ```bash
        source venv/bin/activate
        ```

4. Install project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Apply migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Create a Superuser for Django admin:

    ```bash
    python manage.py createsuperuser
    ```
7. Run the development server:

    ```bash
    python manage.py runserver
    ```

The development server should now be running at [http://localhost:8000/](http://localhost:8000/).



