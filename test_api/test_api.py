import pytest
import requests
import sqlite3
def test_save_post_to_db():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS saved_posts (
        id INTEGER PRIMARY KEY,
        title TEXT
    )""")
    conn.commit()
    responce = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    assert responce.status_code == 200
    data = responce.json()
    assert "title" in data
    title = data["title"]
    cursor.execute("INSERT INTO saved_posts (title) VALUES (?)", (title,))
    conn.commit()
    cursor.execute("SELECT title FROM saved_posts WHERE title = ?", (title,))
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == title
    conn.close()
def test_create_post():
    conn = sqlite3.connect("post.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY,
        title TEXT
    )""")
    
    new_post = {
            "title": "Мой тестовый пост",
            "body": "скибиди боб",
            "userId": 1
        }
    responce = requests.post("https://jsonplaceholder.typicode.com/posts", json=new_post)
    assert responce.status_code == 201
    data = responce.json()
    post_id = data["id"]
    title = data["title"]
    cursor.execute("INSERT OR IGNORE INTO posts (id, title) VALUES (?,?)", (post_id, title))
    conn.commit()
    cursor.execute("SELECT title FROM posts WHERE id = ?", (post_id,))
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == title
    conn.close()
    
