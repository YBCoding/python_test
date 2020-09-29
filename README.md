# PYTHON_TEST
This project is a Test project. It is an API which allows to get back a list of rides and compute the cost of the ride.
In order to achieve that, It exposes two endpoint :


- GET /rides/ 

- GET /rides/{ride_id}/cost
 

## Installation
Requires
- python 3.7+
- pip3.7+

### Virtual env creation
You have to first create a virtual environment to run this project, for this execute the following command
<br />``python3 -m venv /path/to/new/virtual/environment``<br />
<br />
Then you can activate it with following command <br />
``source env/bin/activate``<br />
<br />
For more information see : https://docs.python.org/fr/3/library/venv.html
<br />

### Dependencies
Now that the virtual env is created, you can install the dependencies of the project with following command <br />
``pip install -f requirements.txt``

### Run the Flask server
``python -m flask run``

### Run tests
``python -m pytest``

