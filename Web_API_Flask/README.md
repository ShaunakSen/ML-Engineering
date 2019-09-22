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


### Creating end points for db

We create a new route `/planets` to view all the planets in the 
db. However we run into an error 

```python
@app.route('/planets', methods=['GET'])
def planets():
    planets_list = Planet.query.all()
    return jsonify(data=planets_list)
```

This is because `planets_list` is a list of objects
and we cannot convert them using `jsonify`

The process of converting an obj into a textual repr of that obj
is called **serialization**, and reverse is called **deserialization**

We have to figure out how to serialize a collection of `SQLAlchemy Data Rows`

We use `flask-marshmallow` for this

The steps are"

1. Init marshmallow
```python
# init marshmallow
ma = Marshmallow(app)
```
2. Setup the classes for the fields

```python
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('planet_id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius', 'distance')
```

3. Instantiate the classes with single as well as multi obj deserialization
```python
user_schema = UserSchema()
users_schema = UserSchema(many=True)

planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)

```

4. Use in the route
```python
@app.route('/planets', methods=['GET'])
def planets():
    planets_list = Planet.query.all()
    # use marshmallow to deserialize the result set
    result = planets_schema.dump(planets_list)
    # result is fully serialized - we can now use jsonify
    return jsonify(result)
```

### API Security

We will be using JSON Web Tokens (JWT) for our API

Creating the `/register` route: This route will be able to
add new users to our db:

```python
@app.route('/register', methods=['POST'])
def register():
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
```

Creating the `/login` route:

We set the config for JWT:

```python
# add key for JWT
app.config['JWT_SECRET_KEY'] = 'super-secret'
```

Also we init JWTManager:

```python
# init JWT Manager
jwt = JWTManager(app)
```

We create the `/login` route:

```python
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
```

Sample response for successful login:

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZGVudGl0eSI6InBhZGR5QHBhZGh5LmNvbSIsImp0aSI6IjM3Y2NmYzMwLTk3YzAtNGNjOC1iOWY5LWRiYmRkMmIzMDk5NyIsImV4cCI6MTU2OTEwMjg5OCwiZnJlc2giOmZhbHNlLCJuYmYiOjE1NjkxMDE5OTgsImlhdCI6MTU2OTEwMTk5OCwidHlwZSI6ImFjY2VzcyJ9.kmmpTVHOaf2ArkSQd5nWGiq899qDknxWrpPgUvneNKs",
  "message": "Login succeeded!"
}
```

Sample response for unsuccessful login:

```json
{
  "message": "Invalid email or password"
}
```

### Forgot password functionality

We install `flask-mail`

For an email server we use [Mailtrap.io](https://mailtrap.io/)

After signing up, we will get the Credentials of our SMTP and
POP3 servers

We ue these to set the config params in our API

While setting username and password vars it is a good idea
not to write them in our code simply but to use enviroment vars

```python
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
```
At this point flask-mail is setup and ready to go

We need to create the endpoint now

```python
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
        return jsonify(message='Email: ' + email + ' does not exist')
```

Now we ust have to set the environment vars for this to work

In pycharm we go to `Edit Configurations` and add the environment
variables as shown below:

<img src="./img/diag3.png">

If we are not using pycharm we have to do this at the OS level

On testing, we should get the mail with the `msg` on our
MailTrap inbox

