# MyPipe
## What is it
MyPipe is an online video web hosting, wher the videos can be taken from the YouTube or via direct upload

This project served as a **MySQL** connection and **Django** framework testing

## Requirements

Requirements are listed in the requirements.txt file
In order to run them call:

```shell
pip install -r requirements.txt
```

## Configure
To Configure the project:

1. Run the 'mysqldump.sql' file
2. In MyPipe/models.py edit the login and password from the database
   in variable conn
```python
try:
    conn = sql.connect(host='localhost', user="root", password="Qwerty",
                       database='mypipe', charset="utf8mb4", cursorclass=sql.cursors.DictCursor)

```
This will connect to the database with user `root` and password `Qwerty`

3. After the database is configured and python or virtual enviroment is set up run:

python manage.py runserver

You will get something like that:
```python
Django version 3.1.7, using settings 'myPipeProject.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Go by the `http` presented and you will see the website

If you see `Error 404`, check that Django is version 3.1.7, this is a key requirement for the page to work



## Project Overview

1. All the connections of for the database are be made in MyPipe/models.py. 
2. Views, the rendering of pages, should is done in myPipe/views.py
3. Urls are in myPipeProject.urls.py
4. HTML templates should be are in templates folder
5. Static files(CSS, JavaScript) is in static folder
   Also photos of accounts, channels are also in the static folder
6. HTML and CSS is based on Materialise stylesheet + js
7. On video upload, there is an option to upload directly from computer
it is working however takes some time to read the file, so is not 
   preferable
   
