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

@pytest.mark.parametrize("file, actions, verdict",[
    ('map_debug.txt', 'wdddd', 'NO CLEAR'),
    ('map_debug.txt', 'wddspddwss', 'CLEAR'),
])
def test_boulder_to_boulder(file, actions, verdict):
    session = Base_Game(file, actions, None)
    assert session.run_game() == verdict

@pytest.mark.parametrize("file, actions, verdict",[
    ('map_debug.txt', 'wwdddd', 'NO CLEAR'),
    ('map_debug.txt', 'wwddsdpdddwss', 'CLEAR'),
])
def test_boulder_to_boulder(file, actions, verdict):
    session = Base_Game(file, actions, None)
    assert session.run_game() == verdict

# test item usage
@pytest.mark.parametrize("file, actions, expected_holding, expected_item",[
    ('map_debug.txt', 'dpd', False, None),  # used axe
    ('map_debug.txt', 'spdddd', False, None),  # used flamethrower
])
def test_item_consumption(file, actions, expected_holding, expected_item):
    session = Base_Game(file, actions, None)
    assert session.game_state['holding'] == expected_holding
    assert session.player_held_item == expected_item

@pytest.mark.parametrize("file, actions",[
    ('map_debug.txt', 'ppppp'),  # multiple pickup attempts on empty tile
    ('map_debug.txt', 'dpasp'),  # multiple pickups after getting item
])
def test_multiple_pickup_attempts(file, actions):
    session = Base_Game(file, actions, None)
    # should not crash, holding state should be consistent
    assert isinstance(session.game_state['holding'], bool)