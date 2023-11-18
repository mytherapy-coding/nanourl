"""
URL Shortener

This module defines a simple Flask application for URL shortening.
"""
import string
import random
import json
import os
import flask

FORM = """
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
"""


app = flask.Flask(__name__)


def load_mappings():
    """
    Load URL mappings from the 'data.json' file.

    Returns:
        dict: A dictionary containing the loaded URL mappings.
    """
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


url_mapping = load_mappings()


def generate_short_url():
    """
    Generate a random short URL.

    This function generates a random short URL by combining ASCII letters
    (both lowercase and uppercase) and digits. The length of the short URL
    is set to 6 characters by default, but you can adjust the length as needed.

    Returns:
        str: A randomly generated short URL.

    Example:
        >>> generate_short_url()
        'AbC12f'
    """
    characters = string.ascii_letters + string.digits
    short_url = "".join(random.choice(characters) for i in range(6))
    # You can adjust the length of the short URL
    return short_url


@app.route("/")
def index():
    """
    Render the HTML form for URL shortening.

    This function is the entry point for accessing the URL shortener application.
    It renders an HTML form that allows users to submit a long URL for shortening.

    Returns:
        str: The HTML content of the form.

    Example:
        >>> index()
        '<!DOCTYPE html>...</html>'
    """
    return FORM


def save_mappings():
    """
    Save URL mappings to the 'data.json' file.

    This function writes the current URL mappings to the 'data.json' file.
    If the file does not exist, it will be created.

    Note:
        This function overwrites the existing 'data.json' file.

    Raises:
        IOError: If there is an issue writing to the file.
    """
    with open("data1.json", "w", encoding="utf-8") as file:
        json.dump(url_mapping, file, indent=4)
    os.replace("data1.json", "data.json")


@app.route("/shorten", methods=["POST"])
def shorten():
    """
    Shorten a long URL.

    This function is called when a user submits a long URL via a form.
    It generates a short URL, maps it to the provided long URL, and saves
    the mapping to the 'data.json' file.

    Returns:
        str: A message indicating the shortened URL.

    Raises:
        ValueError: If the submitted form data is invalid.
    """
    long_url = flask.request.form.get("long_url")
    if long_url:
        short_url = generate_short_url()
        url_mapping[short_url] = long_url
        save_mappings()
        print(url_mapping)
        return f"Shortened URL: {flask.request.host_url}{short_url}"
    return "Please provide a URL to shorten."


@app.route("/<short_url>")
def redirect_to_original(short_url):
    """
    Redirect to the original long URL.

    This function is called when a user accesses a short URL.
    It looks up the short URL in the URL mappings, and if found,
    it redirects the user to the original long URL.

    Args:
        short_url (str): The short URL to look up.

    Returns:
        Union[str, werkzeug.wrappers.response.Response]:
            If the short URL is found, a redirection response.
            If the short URL is not found, a message indicating that
            the short URL is not found.
    """
    long_url = url_mapping.get(short_url)
    if long_url:
        return flask.redirect(long_url)
    return "Short URL not found."
