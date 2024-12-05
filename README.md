<h1>Project Overview</h1>
Welcome to the NeatNest backend repository! This project is built using the <strong>Django</strong> framework. Django follows the Model-View-Template (MVT) architectural pattern, enabling developers to efficiently manage data, business logic, and user interfaces. For our database, we are using <strong>PostgreSQL</strong>. Deployment has been done via <strong>www.render.com</strong>


<h5>How Django Works</h5>
Django's MVT architecture can be broken down into three key components:

- Models: Define the data structure. Models are Python classes that map to database tables.
- Views: Handle the application logic and interact with the model to fetch, update, or display data.
- Templates: Define the presentation layer using HTML and Django Template Language (DTL) to dynamically generate web pages.
___

<h3>Useful Commands</h3>


Here are the essential commands you’ll use while developing with Django:

<h5>Create a new Django project</h5>

- ```django-admin startproject project_name```
    - Initializes the project with the default directory structure.


<h5>Create a new app</h5>

- ```python manage.py startapp app_name```
    - Creates a modular component to encapsulate functionality.
___

<h5>Database Setup</h5>

- ```python manage.py makemigrations```
    - makemigrations: Prepares changes to your models as migration files.
- ```python manage.py migrate```
    - migrate: Applies migrations to your database.
___

<h5>Development Server</h5>
Run the development server:

```python manage.py runserver```
Launches the development server at http://127.0.0.1:8000/ by default.
___

<h5>User Management</h5>


```python manage.py createsuperuser```
Generates an admin account to access the Django Admin interface.
___

<h5>Shell and Debugging</h5>
Open the Django shell:

```python manage.py shell```
Launches an interactive Python shell with Django context preloaded.
___

<h5>Development Workflow</h5>
<strong>Setup Environment:</strong>

- Create a virtual environment and activate it:

    - ```python -m venv venv```
    - Mac: ```source venv/bin/activate```
    - Windows: ```venv\Scripts\activate```

- Install dependencies from requirements.txt:

    - ```pip install -r requirements.txt```

- Create models in models.py and apply migrations.

- Link your app’s URLs in urls.py files.

- Write views in views.py to handle application logic.

- Design templates in templates folder for rendering dynamic web pages.

- Run tests to validate functionality.
___

<h5>Deploy</h5>

Use WSGI/ASGI servers like Gunicorn or Daphne for deployment.
Integrate with a production database and configure static/media file handling.
___
<h5>Best Practices</h5>

- Avoid redundancy in your code by reusing components.
- Environment Variables: Store sensitive data like API keys and secrets in environment variables.
- Use Git: Track your project history using version control.
- Documentation: Keep your code well-documented for maintainability.
- Testing: Write unit tests for critical features to ensure reliability.
  
___

