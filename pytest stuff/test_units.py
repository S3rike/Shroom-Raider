import pytest
from shroom_raider import Base_Game

@pytest.mark.parametrize("file, actions, verdict",[
    ('map3.txt', 's', 'NO CLEAR'),
    ('map3.txt', 'w', 'NO CLEAR'),
    ('map3.txt', 'aa', 'NO CLEAR'),
    ('map3.txt', 's', 'NO CLEAR'),
    ('map3.txt', 'dddssddddsdw', 'NO CLEAR'),
    ('map3.txt', 'ddddsssss', 'NO CLEAR'),
    ('map3.txt', 'ddddssdddssddddd', 'NO CLEAR'),
])
def test_wall(file, actions, verdict):
    session = Base_Game(file, actions, None)
    assert session.run_game() == verdict
    
@pytest.mark.parametrize("file, actions, verdict",[
    ('map3.txt', 'ddddssdddwsaawddsssddwwwwdpasssaawaasaaaasapdwwaa', 'CLEAR'),
    ('map.txt', 'dddddddd', 'CLEAR'),
    ('map2.txt', 'aawwadssdddwddaawwdd', 'CLEAR'),
])
def test_boulder(file, actions, verdict):
    session = Base_Game(file, actions, None)
    assert session.run_game() == verdict

@pytest.mark.parametrize("file, actions, verdict",[
    ('map3.txt', 'ddddssa', 'NO CLEAR'),
    ('map3.txt', 'ddddssdddwd', 'NO CLEAR'),
    ('map3.txt', 'ddddssdddsddww', 'NO CLEAR'),
])
def test_drown(file, actions, verdict):
    session = Base_Game(file, actions, None)
    assert session.run_game() == verdict

@pytest.mark.parametrize("file, actions, verdict",[
    ('map3.txt', 'ddddssdddwsaawddsssddwwwwdppppppasssaawaasaaaasapdwwaa', 'CLEAR'),
    ('map3.txt', 'ddddssdddwsaawddsssddwwwwdpasssaawaasaaaasappppppdwwaa', 'CLEAR'),
])
def test_axe(file, actions, verdict):
    session = Base_Game(file, actions, None)
    assert session.run_game() == verdict

@pytest.mark.parametrize("file, actions, verdict",[
    ('map_debug.txt', 'spaa', 'NO CLEAR'),
    ('map_debug.txt', 'spddddww', 'CLEAR'),
    ('map_debug.txt', 'spdwpppppssdddwwww', 'CLEAR'),
])
def test_flamethrower(file, actions, verdict):
    session = Base_Game(file, actions, None)
    assert session.run_game() == verdict