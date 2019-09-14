### Run configurations

We can create a new run configuration of type: `Flask Server` 
in pycharm.

While creating we can point the Target to our `app.py` file and
set the `FLASK_DEBUG` environment variable to `True`.  This will 
enable automatic refresh whenever the code is modified

<img src="./img/diag1.png">

### Install a new package on the venv

To install a new package for the current venv:

1. Go to File -> Settings -> Project -> Project Interpreter
2. Here u can see all packages installed for 


### Flask CLI

In the `app.py` file `@app.cli.command('db_create')` defines 
the function below it as a CLI command `db_create`

Open terminal and type `flask db_create` to run the code 
for that command/function

1. Create the db: `flask db_create`
2. Seed the db: `flask db_seed`

Now we can view the db

<img src="./img/diag2.png">
