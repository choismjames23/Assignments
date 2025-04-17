from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, This is Main Page!"

@app.route('/about')
def about():
    return "Hello, This is About Page!"

@app.route('/user/<username>')
def user_profile(username):
    return f'UserName : {username}'

@app.route('/test')
def test():
    url = 'http://127.0.0.1:5000'
    data = 'test-data'
    response = requests.post(url=url, data=data)
    return response

@app.route('/submin', methods=['GET', 'POST', 'PUT', 'DELETE'])
def submit():
    print(request.method)

    if request.method == 'GET':
        print("GET method")
    elif request.method == 'POST':
        print("***POST method***", request.data)

    return Response('success!', status=200)

if __name__ == "__main__":
    app.run()