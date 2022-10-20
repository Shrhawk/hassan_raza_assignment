# Product Stats Backend
The Goal of this project make a web application where user can input personal details, multiline text and upload a csv
file of sales data. After inputting, this data should be shown on the second tab with text, functional table and a
chart.
### Setup

The first thing to do is to clone the repository:
```shell
git clone "enter_here_link"
```
Create a virtual environment to install dependencies in and activate it:
run following command to install python-env

```shell
sudo apt-get install python3-venv  
mkdir djangoenv
```

create and activate virtual environment

```shell
python3 -m venv djangoenv 
source djangoenv/bin/activate 
```
Then install the dependencies:

```shell
pip install -r requirements.txt
```

After installing dependencies run following command to migrate changes in db:

```shell
python manage.py migrate
```

Note the (env) in front of the prompt. This indicates that this terminal session operates in a virtual environment:

After migrations run following command to create country and cities data in db:

```shell
python manage.py country_cities
```

Now run following command to runserver:
```shell
python manage.py runserver
```

## Execute Tests

All Api's endpoints are covered with test cases: 
After project setup run following command to execute tests.

```shell
pytest -vv -s
```

By executing this command you can run all test cases.

