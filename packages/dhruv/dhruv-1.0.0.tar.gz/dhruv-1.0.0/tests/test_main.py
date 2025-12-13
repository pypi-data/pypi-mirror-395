# tests/test_main.py

from dhruv.main import hello

def test_hello():
    assert hello() == "Hello from Dhruv!"
