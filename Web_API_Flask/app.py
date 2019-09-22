from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message

# this particular app takes its name from the name of the script
app = Flask(__name__)
# base dir: get path for the application
basedir = os.path.abspath(os.path.dirname(__file__))

# app.config is a dict which holds all the configuration values.
# But this is also where you can have your own configuration.
# This is where we set the config for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
# add key for JWT
app.config['JWT_SECRET_KEY'] = 'super-secret'

# Mail Server config properties - from mailtrap credentials

app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']


# now that config has been done, we can init our database
db = SQLAlchemy(app)

# init marshmallow
ma = Marshmallow(app)

# init JWT Manager
jwt = JWTManager(app)

# init mail
mail = Mail(app)


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


# ----------------------------------------------------------------------
# API endpoints to interact with the db

# this route should ONLY respond to GET requests
@app.route('/planets', methods=['GET'])
def planets():
    planets_list = Planet.query.all()
    # use marshmallow to deserialize the result set
    result = planets_schema.dump(planets_list)
    # result is fully serialized - we can now use jsonify
    return jsonify(result)

# ----------------------------------------------------------------------
# Auth endpoints to interact with the db

# REGISTER
@app.route('/register', methods=['POST'])
def register():
    # here we are expecting the request to have come from HTML form fields
    email = request.form['email']
    # check if email exists in our db
    test = User.query.filter_by(email=email).first()
    if test:
        # email already exists
        return jsonify(message='The email: '+email+' already exists'), 409
    else:
        # new user
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        # create the User obj
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        # add the user
        db.session.add(user)
        # commit
        db.session.commit()
        return jsonify(message='User with email: '+email+' added successfully to db'), 201

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    # here we are expecting the request to have come as JSON request
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        # if req came from HTML form fields
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        # user found: send them the JWT token using identity as user email
        access_token = create_access_token(identity=email)
        return jsonify(message='Login succeeded!', access_token=access_token)
    else:
        # no match
        return jsonify(message='Invalid email or password'), 401  # permission denied


# Retrieve password route: accept email as param
@app.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email: str):
    # query the user with the email
    user = User.query.filter_by(email=email).first()
    if user:
        # user exists
        msg = Message('Your Planetary API password is: ' + user.password, sender='admin@planetary-api.com',
                      recipients=['shaunak1105@gmail.com'])
        mail.send(msg)
        # email sent - send response
        return jsonify(message='Password sent to ' + email)
    else:
        return jsonify(message='Email: ' + email + ' does not exist'), 401

# get planet details by ID route
@app.route('/planet_details/<int:planet_id>', methods=['GET'])
def planet_details(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()

    if planet:
        # serialize the result
        result = planet_schema.dump(planet)
        return jsonify(result)

    else:
        return jsonify(message='planet with id:' + str(planet_id) + ' not found'), 404

# route to add a new planet
@app.route('/add_planet', methods=['POST'])
@jwt_required
def add_planet():
    planet_name = request.form['planet_name']
    # check if this planet is already in db
    test = Planet.query.filter_by(planet_name=planet_name).first()

    if test:
        # planet exists already
        return jsonify(message='There is already a planet by that name'), 409  # conflict
    else:
        # get planet details from the form
        planet_type = request.form['planet_type']
        home_star = request.form['home_star']
        mass = float(request.form['mass'])
        radius = float(request.form['radius'])
        distance = float(request.form['distance'])

        # create a new record

        new_planet = Planet(planet_name=planet_name, planet_type=planet_type,
                            home_star=home_star, mass=mass, radius=radius,
                            distance=distance)
        # add the obj to the db
        db.session.add(new_planet)
        db.session.commit()

        return jsonify(message='Added the planet: ' + planet_name), 201

# route for updating a planet
@app.route('/update_planet', methods=['PUT'])
@jwt_required
def update_planet():
    # accept planet_id as a form field
    planet_id = int(request.form['planet_id'])
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        # planet exists
        # get rest of properties and update planet
        planet.planet_name = request.form['planet_name']
        planet.planet_type = request.form['planet_type']
        planet.home_star = request.form['home_star']
        planet.mass = float(request.form['mass'])
        planet.distance = float(request.form['distance'])
        planet.radius = float(request.form['radius'])
        # commit the changes
        db.session.commit()

        return jsonify(message='Updated planet with id: ' + str(planet_id)), 202
    else:
        # no planet
        return jsonify(message='Planet with id: ' + str(planet_id) + ' does not exists'), 404


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


# ----------------------------------------------------
# Classes for Marshmallow
# these are the indicators that tell Marshmallow what fields we are looking for
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('planet_id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius', 'distance')


# instantiate the schema classes - we are defining the ability to deserialize a single obj as well as multiple objects
user_schema = UserSchema()
users_schema = UserSchema(many=True)

planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)

if __name__ == '__main__':
    app.run()
