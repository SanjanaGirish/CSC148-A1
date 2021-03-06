"""CSC148 Assignment 1: Sample tests

=== CSC148 Winter 2022 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Assignment 0.

Warning: This is an extremely incomplete set of tests! Add your own tests
to be confident that your code is correct.

Note: this file is to only help you; you will not submit it when you hand in
the assignment.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) University of Toronto
"""
from datetime import date
from io import StringIO
from a1 import *

# A string representing a simple 4 by 4 game board.
# We use this in one of the tests below. You can use it in your own testing, but
# you do not have to.
SIMPLE_BOARD_STRING = 'P-B-\n-BRB\n--BB\n-C--'
WIDTH_MORE_THAN_HEIGHT_STRING = 'P-B-\n-BRB\n--BB'
HEIGHT_MORE_THAN_WIDTH_STRING = 'P@B\n-BB\nRBB\nBB-'


def width_more_than_height_setup() -> GameBoard:
    """Set up a game board with width greater than height"""
    b = GameBoard(4, 3)
    b.setup_from_grid(WIDTH_MORE_THAN_HEIGHT_STRING)
    return b


def height_more_than_width_setup() -> GameBoard:
    """Set up a game board with height greater than width"""
    b = GameBoard(3, 4)
    b.setup_from_grid(HEIGHT_MORE_THAN_WIDTH_STRING)
    return b


def simple_board_setup() -> GameBoard:
    """Set up a simple game board"""
    b = GameBoard(4, 4)
    b.setup_from_grid(SIMPLE_BOARD_STRING)
    return b


def test_simple_place_character() -> None:
    """Test GameBoard.place_character by placing a single Raccoon."""
    b = GameBoard(3, 2)
    r = Raccoon(b, 1, 1)
    assert b.at(1, 1)[0] == r  # requires GameBoard.at be implemented to work


def test_simple_at() -> None:
    """Test GameBoard.at on docstring example"""
    b = GameBoard(3, 2)
    r = Raccoon(b, 1, 1)
    assert b.at(1, 1)[0] == r
    p = Player(b, 0, 1)
    assert b.at(0, 1)[0] == p


def test_simple_str() -> None:
    """Test GameBoard.__str__ for the simple board in SIMPLE_BOARD_STRING."""
    b = simple_board_setup()
    assert str(b) == 'P-B-\n-BRB\n--BB\n-C--'


def test_width_greater_height_str() -> None:
    """Test GameBoard.__str__ for a board with width more than height"""
    b = width_more_than_height_setup()
    assert str(b) == WIDTH_MORE_THAN_HEIGHT_STRING


def test_height_greater_width_str() -> None:
    """Test GameBoard.__str__ for a board with height more than width"""
    b = height_more_than_width_setup()
    assert str(b) == HEIGHT_MORE_THAN_WIDTH_STRING


def test_simple_check_game_end() -> None:
    """Test GameBoard.check_game_end on the docstring example"""
    b = GameBoard(3, 2)
    Raccoon(b, 1, 0)
    Player(b, 0, 0)
    RecyclingBin(b, 1, 1)
    assert b.check_game_end() is None
    assert not b.ended
    RecyclingBin(b, 2, 0)
    score = b.check_game_end()
    assert b.ended
    assert score == 11  # will only pass this last one when done Task 5.


def test_simple_adjacent_bin_score() -> None:
    """Test GameBoard.adjacent_bin_score on the docstring example"""
    b = GameBoard(3, 3)
    RecyclingBin(b, 1, 1)
    RecyclingBin(b, 0, 0)
    RecyclingBin(b, 2, 2)
    assert b.adjacent_bin_score() == 1
    RecyclingBin(b, 2, 1)
    assert b.adjacent_bin_score() == 3
    RecyclingBin(b, 0, 1)
    assert b.adjacent_bin_score() == 5


def test_simple_player_move() -> None:
    """Test Player.move on docstring example."""
    b = GameBoard(4, 2)
    p = Player(b, 0, 0)
    assert not p.move(UP)
    assert p.move(DOWN)
    assert b.at(0, 1) == [p]
    RecyclingBin(b, 1, 1)
    assert p.move(RIGHT)
    assert b.at(1, 1) == [p]


def test_simple_recyclingbin_move() -> None:
    """Test RecyclingBin.move on docstring example."""
    b = GameBoard(4, 2)
    rb = RecyclingBin(b, 0, 0)
    assert not rb.move(UP)
    assert rb.move(DOWN)
    assert b.at(0, 1) == [rb]


def test_simple_raccoon_check_trapped() -> None:
    """Test Raccoon.check_trapped on docstring example."""
    b = GameBoard(3, 3)
    r = Raccoon(b, 2, 1)
    Raccoon(b, 2, 2)
    Player(b, 2, 0)
    assert not r.check_trapped()
    RecyclingBin(b, 1, 1)
    assert r.check_trapped()


def test_corner_raccoon_check_trapped() -> None:
    """Test Raccoon.check_trapped when raccoon is in top-left corner"""
    b = GameBoard(3, 3)
    r = Raccoon(b, 0, 0)
    Player(b, 1, 0)
    RecyclingBin(b, 0, 1)
    assert r.check_trapped()


def test_garbage_can_raccoon_check_trapped() -> None:
    """Test Raccoon.check_trapped when raccoon can move into an open garbage
    can. Also tests the case, when raccoon is not at an edge"""
    b = GameBoard(3, 3)
    r = Raccoon(b, 1, 1)
    _ = Player(b, 1, 0)
    _ = RecyclingBin(b, 0, 1)
    g = GarbageCan(b, 1, 2, False)
    _ = Raccoon(b, 2, 1)
    assert r.check_trapped() == False
    g.locked = True
    assert r.check_trapped() == True


def test_simple_raccoon_move() -> None:
    """Test Raccoon.move on docstring example."""
    b = GameBoard(4, 2)
    r = Raccoon(b, 0, 0)
    assert not r.move(UP)
    assert r.move(DOWN)
    assert b.at(0, 1) == [r]
    g = GarbageCan(b, 1, 1, True)
    assert r.move(RIGHT)
    assert (r.x, r.y) == (0, 1)  # Raccoon didn't change its position
    assert not g.locked  # Raccoon unlocked the garbage can!
    assert r.move(RIGHT)
    assert r.inside_can
    assert len(b.at(1, 1)) == 2  # Raccoon and GarbageCan are both at (1, 1)!


def test_simple_raccoon_take_turn() -> None:
    """Test Raccoon.take_turn on docstring example."""
    b = GameBoard(3, 4)
    r1 = Raccoon(b, 0, 0)
    r1.take_turn()
    assert (r1.x, r1.y) in [(0, 1), (1, 0)]
    r2 = Raccoon(b, 2, 1)
    RecyclingBin(b, 2, 0)
    RecyclingBin(b, 1, 1)
    RecyclingBin(b, 2, 2)
    r2.take_turn()  # Raccoon is trapped
    assert (r2.x, r2.y) == (2, 1)


def test_simple_smartraccoon_take_turn() -> None:
    """Test SmartRaccoon.take_turn on docstring example."""
    b = GameBoard(8, 2)
    s = SmartRaccoon(b, 4, 0)
    GarbageCan(b, 3, 1, False)
    GarbageCan(b, 0, 0, False)
    GarbageCan(b, 7, 0, False)
    s.take_turn()
    assert s.x == 5
    s.take_turn()
    assert s.x == 6


def test_simple_give_turns() -> None:
    """Test GameBoard.give_turns on docstring example."""
    b = GameBoard(4, 3)
    p = Player(b, 0, 0)
    r = Raccoon(b, 1, 1)
    for _ in range(RACCOON_TURN_FREQUENCY - 1):
        b.give_turns()
    assert b.turns == RACCOON_TURN_FREQUENCY - 1
    assert (r.x, r.y) == (1, 1)  # Raccoon hasn't had a turn yet
    assert (p.x, p.y) == (0, 0)  # Player hasn't had any inputs
    p.record_event(RIGHT)
    b.give_turns()
    assert (r.x, r.y) != (1, 1)  # Raccoon has had a turn!
    assert (p.x, p.y) == (1, 0)  # Player moved right!


def test_simple_pc1() -> None:
    """ Test place player character when gameboard empty"""
    g = GameBoard(4, 3)
    _ = Player(g, 0, 0)
    g.place_character(_)
    assert g.at(0, 0)[0] == _


def test_simple_pc2() -> None:
    """ Test place recyling bin character on occupied position"""
    g = GameBoard(4, 3)
    _ = Player(g, 0, 0)
    rb = RecyclingBin(g, 0, 0)
    g.place_character(_)
    g.place_character(rb)
    assert len(g.at(0, 0)) == 1


def test_simple_pc3() -> None:
    """ Test place racoon character on garbagecan - open and closed"""
    g = GameBoard(4, 3)
    g1 = GarbageCan(g, 0, 0, True)
    _ = Raccoon(g, 0, 0)
    assert len(g.at(0, 0)) == 1
    g1.locked = False
    _ = Raccoon(g, 0, 0)
    assert len(g.at(0, 0)) == 2


def test_simple_ge1() -> None:
    """ Test game ended with empty neighboring tile"""
    g = GameBoard(3, 3)
    r = Raccoon(g, 1, 1)
    RecyclingBin(g, 1, 0)
    RecyclingBin(g, 0, 1)
    RecyclingBin(g, 1, 2)
    assert g.check_game_end() == None
    assert g.ended == False


def test_simple_ge2() -> None:
    """ Test game ended with racoon in board corner"""
    g = GameBoard(3, 3)
    r = Raccoon(g, 0, 0)
    RecyclingBin(g, 1, 0)
    RecyclingBin(g, 0, 1)
    assert g.check_game_end() != None
    assert g.ended == True
    assert g.check_game_end() == 11


def test_simple_ge3() -> None:
    """ Test game ended with racoon in garbagecan"""
    g = GameBoard(3, 3)
    GarbageCan(g, 0, 0, False)
    Raccoon(g, 0, 0)
    assert len(g.at(0, 0)) == 2
    assert g.check_game_end() != None
    assert g.ended == True


def test_simple_ge4() -> None:
    """ Test game ended with racoon in garbagecan"""


def test_smart_raccoon_turn_taker_closed() -> None:
    """ Testing SmartRaccoon.turn_taker, when the closest GarbageCan
    is closed also tests whether the smart raccoon opens the garbage can if
    locked."""
    g = GameBoard(5,5)
    r = SmartRaccoon(g, 2, 2)
    _ = GarbageCan(g, 1, 2, True)
    t = _
    _ = GarbageCan(g, 2, 1, False)
    r.take_turn()
    assert r.x == 2 and r.y == 2
    assert not t.locked


def test_smart_raccoon_turn_taker_closed2() -> None:
    """ Testing SmartRaccoon.turn_taker, when the closest GarbageCan
    is closed"""
    g = GameBoard(5, 5)
    r = SmartRaccoon(g, 2, 2)
    _ = GarbageCan(g, 0, 2, True)
    _ = GarbageCan(g, 2, 0, False)
    r.take_turn()
    assert r.x == 1 and r.y == 2


def test_smart_raccoon_turn_taker_closed3() -> None:
    """ Testing SmartRaccoon.turn_taker, when the closest GarbageCan
    is closed"""
    g = GameBoard(5, 5)
    r = SmartRaccoon(g, 2, 2)
    _ = GarbageCan(g, 0, 2, True)
    _ = GarbageCan(g, 2, 1, False)
    r.take_turn()
    assert r.x == 2 and r.y == 1
    
    
def test_adjacent_bins_score_no_bins() -> None:
    """Test adjacent bins score with no recycling bins"""
    g = GameBoard(3, 3)
    assert g.adjacent_bin_score() == 0


def test_adjacent_bins_score_all() -> None:
    """Test adjacent bins score with all squares recycling bins"""
    g = GameBoard(3, 3)
    for i in range(g.width):
        for j in range(g.height):
            _ = RecyclingBin(g, i, j)
    assert g.adjacent_bin_score() == 9

    
if __name__ == '__main__':
    import pytest

    pytest.main(['a1_sample_test.py'])
