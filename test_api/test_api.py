import requests
import pytest
import sqlite3
def test_get_post():
    responce = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    data = responce.json()
    assert responce.status_code == 200
    assert "title" in data
    assert "body" in data
    assert data["id"] == 1
    assert "userId" in data
def test_save_post_to_db():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY,
        title TEXT)""")
    conn.commit()
    get_post = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    data = get_post.json()
    title = data["title"]
    cursor.execute("INSERT INTO posts (title) VALUES (?)", (title,))
    conn.commit()
    cursor.execute("SELECT title FROM posts WHERE title = (?)", (title,))
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == title