<h1>Project Overview</h1>
Welcome to the NeatNest backend repository! This project is built using the <strong>Django</strong> framework. Django follows the Model-View-Template (MVT) architectural pattern, enabling developers to efficiently manage data, business logic, and user interfaces. For our database, we are using <strong>PostgreSQL</strong>. Deployment has been done via <a href ="www.render.com">www.render.com</a>


<h5>How Django Works</h5>
Django's MVT architecture can be broken down into three key components:

- [Models](#models): Define the data structure. Models are Python classes that map to database tables.
- [Views](#views): Handle the application logic and interact with the model to fetch, update, or display data.
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

- Create [Models](#models) in models.py and apply migrations.

- Link your app’s [URLs](#URLs) in urls.py files.

- Create [Serializers](#serializers) for your models. 

- Write [Views](#views) in views.py to handle application logic.

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
___
<h2 id = "models">Models</h2>


<h4>User</h4>

Creating a User object is the first step in creating an account. Fields in this model will be things that are universal across both Customer objects, or accounts, and Service_Provider objects or accounts. Our User model inherits AbstractUser, which automatically populates fields such as first name, last name, username, password. These fields will not be shown in the model. 

At the top of our User model, we have a line of code:

```User = get_user_model```

This code retrieves the custom User model we have built. This is necessary because in settings.py we have another line of code:

```AUTH_USER_MODEL = 'main.User'```

This is assigning the Auth User Model to our custom User model. 
___

<h4>Customer</h4>

Our Customer model is linked to our User Model, or data table, via a one-to-one foreign key. This is the same for our Service_Provider model as well. The foreign key relationship automatically sets the primary key of User to the foreign key of Customer. The User, and Customer models do not store location or address information. Rather, the Home objects linked to the Customer store the address information for each Home object respectively. 
___

<h4>Service_Provider</h4>

Service_Provider has a very similar setup to Customer. One of the main differences of this model as opposed to the Customer model, is the Service Provider model stores address information, as well as longitude and latitude coordinates. 

___

<h4>Home</h4>

The Home model has a Customer foreign key, associating each Home object with a Customer object. Like the Service_Provider model, Home stores address information, as well as longitude and latitude coordinates. This model stores also stores information that helps guide a Service_Provider to understanding the size of the home, and resultingly the amount of work likely to be necessary for a Job. 
___

<h4>Job</h4>

The Job model has 3 main relationships - Customer, Service_Provider, and Home. Because of this, any Job will be associated with the necessary information - who is providing the service, who is requesting and paying for the service, and where the service is taking place. Jobs also store information from other models - task and rooms. Each Job, will have Rooms in which services will be required, and one-or-many tasks for each room. A list of status choices for each Job appears at the top of the model. These are important, as they track the status of Jobs, and allow us to maintain an accurate, up-to-date database. 
___

<h4>Room</h4>

The Room model is associated with a Home. A Room object holds information like the type of room, it's name, and any information relevant to the room or how to clean it. 

___

<h4>Task</h4>

The Task model is associated with a Job object, and a Room object. This allows for detailed information, where each task is assigned to a Room, and the task in that Room is assigned to a Job. Tasks contain descriptions about the nature of the Task, an optional duration field, an optional price if the Service_Provider charges for each task as opposed to a flat rate. Additionally, there are fields provided for Service_Provider notes and Customer notes, allowing further detail to be given pertaining to the Task. 
___
___

<h2 id = "urls">URLs</h2>

Most of our URLs are created by the use a router, which inherits a class based viewset from Views. The viewset handles all HTTP request methods. A few custom paths have also been made. These paths reference specific Views that house custom logic for specific querying needs

___
___

<h2 id = "views">Views</h2>

Most of our class based Views inherit viewsets. This allows for a streamlined approach for all basic CRUD operations or HTTP methods. Our Customer and Service_Provider views contain specific logic for post requests, which require a User id to be provided in order to link the new object with a User id. JobHistoryList and HomeHistoryList contain specific logic for get requests, which when queried, provide a job history in descending order - where the most recent jobs appear at the top of the list. NearbyProvidersView uses some functionality housed in utils.py - which allows for the use of a distance matrix API on locationiq. This allows us to return an ordered list of Service Providers based on proximity to the house being cleaned via a get request. 

___
___

<h2 id = "serializers">Serializers</h2>

Our Serizalizers are pretty straightforward. The purpose of a serializer is to jsonify data going to and coming from a database. A lot of our Serializers simply call all of the fields from a Model - ```fields = '__all__'```. Most of the Serializers that contain custom logic have foreign key relationships in their respective models. 
___

<h2>Deployment</h2>

We chose to deploy our application via <a href ="www.render.com">www.render.com</a>. Render automatically pulls from the accepted Repository in Github and automatically updates as long as the repository is up to date on all of our pushes. In order to connect render with Django a couple dependencies needed to be installed which are: gunicorn and dj_database_url. Gunicorn is a Python WSGI used to deploy web applications and dj_database_url is used for database configuration. We also needed to connect our PostgreSQL database with Render to deploy the application. In order to connect PostgreSQL dependency psycopg2-binary needs to be installed as well. To connect the PostgreSQL the internal URL was added in settings.py. Our .env file which is included in the .gitignore contains our LOCATIONIQ_API_KEY and SECRET_KEY. 
___


# Image Upload and Management

This document explains how the image upload functionality works in the app and how it integrates with AWS S3 using a Lambda function. It covers the setup, models, views, and API usage.

---

## **Features**
- Upload images to the app.
- Store uploaded images in an AWS S3 bucket (`neatnest`).
- Handle image files using a Django model.
- Use AWS Lambda for S3 upload.
- Serve image URLs back to the client.

---

## **Setup**

### **1. AWS Configuration**

1. **S3 Bucket:**
   - Create an S3 bucket named `neatnest` in your AWS account.
   - Configure the bucket permissions to allow public read access for uploaded objects.

2. **IAM Role for Lambda:**
   - Create an IAM role with the following permissions:
     - `s3:PutObject`
     - `s3:GetObject`
   - Attach this role to your AWS Lambda function.

3. **AWS Lambda Function:**
   - Create an AWS Lambda function for uploading images to S3.
   - Use the provided Python code in `lambda_function.py` (see below) to handle image uploads.
   - Configure environment variables for `BUCKET_NAME` and any other required settings.

### **2. Django Configuration**

1. Install the required libraries:
   ```bash
   pip install boto3
   ```

2. Add the following settings to `settings.py`:
   ```python
   AWS_ACCESS_KEY_ID = "<your-access-key-id>"
   AWS_SECRET_ACCESS_KEY = "<your-secret-access-key>"
   AWS_REGION = "<your-region>"
   AWS_S3_BUCKET = "bucket_name"
   AWS_S3_URL = f"https://{AWS_S3_BUCKET}.s3.amazonaws.com/"
   ```

---

## **Models**

The `Image` model is used to store metadata about uploaded images, including the S3 URL.

```python
from django.db import models

class Image(models.Model):
    title = models.CharField(max_length=255)
    s3_url = models.URLField()  # Stores the S3 URL of the image
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

---

## **Views**

The image upload API endpoint allows users to upload images and saves the S3 URL in the database.

---

## **AWS Lambda Function**

The Lambda function receives the image file and uploads it to S3.

---

## **Testing the API**

### **1. Using Postman**

1. Set the URL to `http://127.0.0.1:8000/upload/`.
2. Use the POST method.
3. Add the following form-data:
   - `title`: (string) Title of the image.
   - `file`: (file) Select an image file to upload.

4. Send the request.

#### Example Response:
```json
{
    "message": "Image uploaded successfully",
    "image": {
        "id": 1,
        "s3_url": "https://neatnest.s3.amazonaws.com/unique-image-id.jpg"
    }
}
```

---

## **Troubleshooting**

- **"No image file provided":** Ensure you are sending the file in the `file` field of the POST request.
- **"Failed to upload image to S3":** Verify your AWS Lambda function URL and permissions.
- **"Token authentication failed":** Ensure you are passing a valid Firebase ID token if required.

For further assistance, contact the development team.

