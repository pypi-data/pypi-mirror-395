import pytest
from epsonrc.commands import connect, send, command, go, move, go_here, move_here, begin

def test_connect():
    assert connect() == True

def test_send():
    assert send('Login') == True

def test_command():
    assert command("Speed 50") == True
    
def test_begin():
    assert begin() == True

def test_go():
    assert go(-325, 480, 650, 125, 0, 180) == True
    
def test_move():
    assert move(-225, 580, 650, 125, 0, 180) == True
    
def test_go_here():
    assert go_here(100, -100) == True
    
def test_move_here():
    assert move_here(-100, 100) == True
    
if __name__ == "__main__":
    pytest.main()