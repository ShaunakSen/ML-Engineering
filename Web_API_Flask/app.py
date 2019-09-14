from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os

# this particular app takes its name from the name of the script
app = Flask(__name__)
# base dir: get path for the application
basedir = os.path.abspath(os.path.dirname(__file__))

# app.config is a dict which holds all the configuration values.
# But this is also where you can have your own configuration.
# This is where we set the config for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')

# now that config has been done, we can init our database
db = SQLAlchemy(app)


# 3 scripts: create db, seed db and delete db
# --------------------------------
# 1: DB CREATE: the decorator turns the function into a CLI command, with the command: 'db_create'
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created')

# 2: DB DROP: the decorator turns the function into a CLI command, with the command: 'db_drop'
@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped')

# 3: DB SEED: the decorator turns the function into a CLI command, with the command: 'db_seed'
@app.cli.command('db_seed')
def db_seed():
    # seed db with 3 planets and 1 user
    mercury = Planet(planet_name='Mercury',
                     planet_type='Class D',
                     home_star='Sol',
                     mass=3.258e23,
                     radius=1516,
                     distance=35.98e6)
    venus = Planet(planet_name='Venus',
                     planet_type='Class K',
                     home_star='Sol',
                     mass=4.867e24,
                     radius=3760,
                     distance=67.24e6)
    earth = Planet(planet_name='Earth',
                     planet_type='Class M',
                     home_star='Sol',
                     mass=5.972e24,
                     radius=3959,
                     distance=92.96e6)
    # add these planets to the db as records
    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    # create a new user
    test_user = User(first_name='Mini', last_name='Sen', email='mini@mini.com', password='blaah')

    # add the user to the db
    db.session.add(test_user)

    # save the changes
    db.session.commit()

    print('Database seeded')


# DECORATOR: special capabilities to our functions
@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/super_simple')
def super_simple():
    return jsonify(message="Hey there from the API!")


# test endpoint that generates an error

@app.route('/not_found')
def not_found():
    return jsonify(message="NOT FOUND"), 404

# URL parameters
@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))

    if age < 18:
        return jsonify(message="Sorry " + name + ", you are not old enough"), 401
    else:
        return jsonify(message="Welcome! " + name)


# cleaner way to get URL parameters
@app.route("/url_variables/<string:name>/<int:age>")
def url_variables(name: str, age: int):
    if age < 18:
        return jsonify(message="Sorry " + name + ", you are not old enough"), 401
    else:
        return jsonify(message="Welcome! " + name)


# add classes for the db models
class User(db.Model):
    # set table name when table is created by SQLAlchemy
    __tablename__ = 'users'
    # set columns
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Planet(db.Model):
    # set table name when table is created by SQLAlchemy
    __tablename__ = 'planets'

    # set columns
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)


if __name__ == '__main__':
    app.run()
