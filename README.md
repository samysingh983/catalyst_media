Project Name

#CATALYST COUNT

Description

Web application using Django 3.x/4.x, Postgres and Bootstrap 4/5. The application will allow users to login and upload a large volume data csv (1GB) with a visual progress of the upload.
Once the file is uploaded, you must update the database with the contents of the file. Next, you must allow the user to filter the data using a form. Once the user submits the form, display the count of records based on the applied filters

#Requirements

Python (version 3 or later) - https://www.python.org/downloads/
Django (version 3.x/4.x or later) - https://docs.djangoproject.com/en/5.0/
Installation instructions for each library can be found on their respective documentation websites.
Installation

#Create a virtual environment:

It's highly recommended to create a virtual environment to isolate project dependencies and avoid conflicts with other Python projects on your system. Here's how to create one using venv (available in Python 3.3+):

#CMD

python -m venv venv

#Activate the virtual environment (commands differ slightly based on your operating system):

#Windows: venv\Scripts\activate.bat

#Install dependencies:

Navigate to your project directory and install the required packages from the requirements.txt file using pip:

#CMD

pip install -r requirements.txt

#Running the project

#Start the development server:

With the virtual environment activated, run the following command to start the Django development server:

#CMD

python manage.py runserver

This will typically start the server at http://127.0.0.1:8000/ by default. You can access your project in a web browser.

#Tests

The project includes a tests.py file containing unit tests for its functionalities. To run the tests:

#Execute the tests:

From your project directory, use the following command to execute the tests:

#CMD

python manage.py test

This will provide an overview of passed and failed tests, if any.

#Sample Image

#Login Page

![image](https://github.com/user-attachments/assets/f0a8fc79-8430-4530-91b0-d53188f907ba)

#USER Page

![image](https://github.com/user-attachments/assets/735b5146-1387-49b7-ab98-bb4adfeab3ca)

#Upload Data

![image](https://github.com/user-attachments/assets/6b2a889e-e477-4257-828b-7a63e428c50b)

#Query Builder

![image](https://github.com/user-attachments/assets/2cc7d272-d5a0-4b9f-a8d6-d9d0bfbbfae5)



