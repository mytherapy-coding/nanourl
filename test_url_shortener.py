import pytest
from url_shortener import app, url_mapping


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get("/")
    assert b"Shorten a URL" in response.data


def test_shorten_valid_url(client):
    response = client.post("/shorten", data={"long_url": "http://example.com"})
    assert b"Shortened URL" in response.data


def test_shorten_invalid_url(client):
    response = client.post("/shorten", data={"long_url": ""})
    assert b"Please provide a URL" in response.data


def test_redirect_to_original(client):
    short_url = "abc123"
    url_mapping[short_url] = "http://example.com"
    response = client.get(f"/{short_url}")
    assert response.status_code == 302
    assert response.headers["Location"] == "http://example.com"


def test_redirect_to_original_invalid_short_url(client):
    response = client.get("/invalid_short_url")
    assert b"Short URL not found" in response.data
