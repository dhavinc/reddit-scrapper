from os import environ
from flask import Flask
from flask import request

app = Flask(__name__)
@app.route('/')
def query_example():
    return 'Todo...'
if __name__ == "__main__":
    app.run(environ.get('PORT'))