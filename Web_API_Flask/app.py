from flask import Flask

# this particular app takes its name from the name of the script
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
