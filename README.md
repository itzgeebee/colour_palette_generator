# colour_palette_generator
## hosted on [heroku](https://radiant-sea-26869.herokuapp.com/)
I created this project as part of my #100 days of code journey.
This is a simple website that generates the 10 most common colours of any image you upload

## Starting the project
To build your own version of this project, [Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. 

## About the Stack
The Application is somewhat fullstack or a backend with a minimal frontend. I used:
- Flask for the backend
- HTML, CSS and Bootstrap for the frontend.

## Backend 
The [main.py](/main.py) contains a completed Flask Server.

### Setting up the backend

#### Install the dependencies
1. Python. I used version 3.9 for this project. Here's the instruction to install [python](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
2. I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
3. PIP Dependencies - Once your virtual environment is up and running, install the required dependencies by running:
` pip install -r requirements.txt`

#### Key Pip Dependencies
- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [Numpy](https://numpy.org/doc/) is the fundamental package for scientific computing in Python. It is a Python library that provides a multidimensional array object, various derived objects (such as masked arrays and matrices), and an assortment of routines for fast operations on arrays, including mathematical, logical, shape manipulation, sorting, selecting, I/O, discrete Fourier transforms, basic linear algebra, basic statistical operations, random simulation and much more. I used numpy to get the Hexcodes from the images
- [Pillow](https://pypi.org/project/Pillow/) The Python Imaging Library adds image processing capabilities to your Python interpreter. I used Pillow for the image processing

#### Run the Server
Ensure that you are working within your virtual environment before running the server.
To run the server, execute: 
` flask run `
 
 ### Deployment
 The application is deployed on heroku cloud platform with a [gunicorn](https://gunicorn.org/) server.
 
 
 
