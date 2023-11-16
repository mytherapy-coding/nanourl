from flask import Flask, request, redirect
import string
import random
import json

form = \
'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Shortener</title>
</head>
<body>
    <h2>Shorten a URL</h2>
    <form method="post" action="/shorten">
        <label for="long_url">Enter URL:</label>
        <input type="text" id="long_url" name="long_url" required>
        <button type="submit">Shorten</button>
    </form>
</body>
</html>
'''




app = Flask(__name__)

def load_mappings():
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

url_mapping = load_mappings()

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for i in range(6))  # You can adjust the length of the short URL
    return short_url


@app.route('/')
def index():
    return form


def save_mappings():
    with open('data.json', 'w') as file:
        json.dump(url_mapping, file, indent=4)

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form.get('long_url')
    if long_url:
        short_url = generate_short_url()
        url_mapping[short_url] = long_url
        save_mappings()
        print(url_mapping)
        return f'Shortened URL: {request.host_url}{short_url}'
    else:
        return 'Please provide a URL to shorten.'
    

@app.route('/<short_url>')
def redirect_to_original(short_url):
    long_url = url_mapping.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return 'Short URL not found.'


