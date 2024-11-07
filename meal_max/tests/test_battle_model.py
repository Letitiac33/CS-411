import pytest
from pytest_mock import mocker

from meal_max.models.battle_model import BattleModel
from meal_max.models.kitchen_model import Meal


@pytest.fixture
def battle_model():
    """Fixture to provide a new instance of BattleModel for each test."""
    return BattleModel()

@pytest.fixture
def mock_update_meal_stats(mocker):
    """Mock the update_meal_stats function for testing purposes."""
    return mocker.patch("meal_max.models.battle_model.update_meal_stats")


##@pytest.fixture
##def mock_get_random(mocker):
##    return mocker.patch("meal_max.models.utils.random_utils.get_random")

"""Fixtures providing sample meals for the tests."""
@pytest.fixture
def mock_get_random():
    return 0.42

@pytest.fixture
def mock_combatant_1():
    return Meal(id=1, meal="Meal A", price=10.0, cuisine="Italian", difficulty="HIGH")

@pytest.fixture
def mock_combatant_2():
    return Meal(id=2, meal="Meal B", price=15.0, cuisine="Mexican", difficulty="LOW")

@pytest.fixture
def sample_battle(mock_combatant_1, mock_combatant_2):
    return [mock_combatant_1, mock_combatant_2]



######################################################
#
#    Battle Tests
#
######################################################

def test_battle(battle_model, mock_combatant_1, mock_combatant_2, mock_update_meal_stats, mock_get_random):
    """Test the battle function between two combatants."""
    battle_model.prep_combatant(mock_combatant_1)
    battle_model.prep_combatant(mock_combatant_2)
    
    mock_random = mocker.patch("meal_max.utils.random_util.get_random", return_value= 0.42)
 
    winner = battle_model.battle()
    
    # Ensure one combatant is removed after the battle
    assert len(battle_model.combatants) == 1, "Only one combatant should remain after the battle."

    #get scores
    score_1 = battle_model.get_battle_score(mock_combatant_1)
    score_2 = battle_model.get_battle_score(mock_combatant_2)
    delta = score_1 - score_2 #.33
    random_num = mock_get_random #.42 
    
    if (delta > random_num):
        assert winner == (1, "Meal A", 10.0, "Italian", "HIGH")

    else:
        assert winner == (2, "Meal B", 15.0, "Mexican", "LOW")

def test_clear_combatants(battle_model, mock_combatant_1, mock_combatant_2):
    """Test clearing all combatants."""
    battle_model.prep_combatant(mock_combatant_1)
    battle_model.prep_combatant(mock_combatant_2)
    battle_model.clear_combatants()

    # Verify the combatants list is empty
    assert len(battle_model.combatants) == 0, "Combatants list should be empty after clearing."

def test_get_battle_score(battle_model, mock_combatant_1, mock_combatant_2):
    """Test the calculation of battle scores for combatants."""
    score_1 = battle_model.get_battle_score(mock_combatant_1)
    score_2 = battle_model.get_battle_score(mock_combatant_2)

    expected_score_1 = (mock_combatant_1.price * len(mock_combatant_1.cuisine)) - 1  # Difficulty "HIGH" has modifier 1
    expected_score_2 = (mock_combatant_2.price * len(mock_combatant_2.cuisine)) - 3  # Difficulty "LOW" has modifier 3

    assert score_1 == expected_score_1, f"Expected score {expected_score_1} for combatant 1, got {score_1}."
    assert score_2 == expected_score_2, f"Expected score {expected_score_2} for combatant 2, got {score_2}."

def test_get_combatants(battle_model, mock_combatant_1, mock_combatant_2):
    """Test retrieving the current list of combatants."""
    battle_model.prep_combatant(mock_combatant_1)
    battle_model.prep_combatant(mock_combatant_2)

    combatants = battle_model.get_combatants()

    # Verify that the combatants list matches what was added
    assert combatants == [mock_combatant_1, mock_combatant_2], "Combatants list does not match expected output."

def test_prep_combatant(battle_model, mock_combatant_1, mock_combatant_2):
    """Test adding combatants to the battle model."""
    battle_model.prep_combatant(mock_combatant_1)
    assert len(battle_model.combatants) == 1, "One combatant should be added to the list."

    battle_model.prep_combatant(mock_combatant_2)
    assert len(battle_model.combatants) == 2, "Two combatants should be present in the list."

    # Attempt to add a third combatant and expect an error
    with pytest.raises(ValueError, match="Combatant list is full"):
        battle_model.prep_combatant(Meal(id=3, meal="Meal C", price=12.0, cuisine="Chinese", difficulty="MED"))

def test_prep_combatants_extra_combatant():
    return None

######################################################
#
#    Get Combatants
#
######################################################

