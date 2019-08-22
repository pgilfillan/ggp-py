import util
import pytest
from src.core.propnet_arch.propnet import PropNet
from src.core.statemachines.propnet import PropNetStateMachine

simple_description = util.get_game_description("proptest_simple")
complex_grounded_description = util.get_game_description("proptest_complex_grounded")
variables_description = util.get_game_description("proptest_variables")

def test_simple_grounded_rules_propnet_creation():
    p = PropNet(simple_description)
    assert len(p.bases) == 1
    assert len(p.inputs) == 2
    assert len(p.roles) == 2
    assert len(p.legals["white"]) == 1
    assert len(p.legals["black"]) == 1
    assert p.terminal is not None
    assert len(p.rewards["white"]) == 2
    assert len(p.rewards["black"]) == 2

def test_simple_grounded_rules_game_play():
    util.run_random_game(PropNetStateMachine(simple_description), 5)

def test_complex_grounded_rules_propnet_creation():
    p = PropNet(complex_grounded_description)
    assert len(p.bases) == 2
    assert len(p.inputs) == 3
    assert len(p.roles) == 2
    assert len(p.legals["white"]) == 2
    assert len(p.legals["black"]) == 1
    assert p.terminal is not None
    assert len(p.rewards["white"]) == 2
    assert len(p.rewards["black"]) == 2