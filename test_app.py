import pytest
import app as board

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(board, "DB_PATH", str(tmp_path / "test.db"))
    return board.app.test_client()

def test_ping(client):
    assert client.get("/ping").data == b"pong"

def test_empty_board(client):
    assert b"No messages yet" in client.get("/").data

def test_post_and_show(client):
    client.post("/post", data={"name": "G", "body": "hello world"})
    assert b"hello world" in client.get("/").data

def test_rejects_empty(client):
    r = client.post("/post", data={"name": "", "body": "hi"})
    assert r.status_code == 400

def test_html_is_escaped(client):
    client.post("/post", data={"name": "x", "body": "<script>alert(1)</script>"})
    page = client.get("/").data
    assert b"<script>alert(1)" not in page