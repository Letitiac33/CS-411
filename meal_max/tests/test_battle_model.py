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

def test_battle(battle_model, mock_combatant_1, mock_combatant_2, mock_update_meal_stats, mocker):
    """Test the battle function between two combatants."""
    battle_model.prep_combatant(mock_combatant_1)
    battle_model.prep_combatant(mock_combatant_2)

    
    mock_random = mocker.patch("meal_max.models.battle_model.get_random", return_value= 0.42)
 
    result = battle_model.battle()

    winner = mock_combatant_2
    expected_result = winner.meal

    assert result == expected_result, f"Expected {expected_result}, got {result}"
    mock_random.assert_called_once_with()
    
    # Ensure one combatant is removed after the battle
    assert len(battle_model.combatants) == 1, f"Only one combatant should remain after the battle."

    #test that loser left
    assert mock_combatant_1 not in battle_model.combatants, f"Loser should not remain in battle."

    # Test that the winner remains
    assert mock_combatant_2 in battle_model.combatants, f"Winner should remain after the battle."

    #test that stats are updated
    mock_update_meal_stats.assert_any_call(mock_combatant_1.id, 'loss')
    mock_update_meal_stats.assert_any_call(mock_combatant_2.id, "win")

def test_battle_one_combatant(battle_model, mock_combatant_1):
    """Test that a battle cannot start with fewer than two combatants."""
    # Add only one combatant
    battle_model.prep_combatant(mock_combatant_1)
    # Expect ValueError due to insufficient combatants
    with pytest.raises(ValueError, match="Two combatants must be prepped for a battle"):
        battle_model.battle()

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

def test_prep_combatants_extra_combatant(battle_model, mock_combatant_1, mock_combatant_2):
    """Test adding a 3rd combatant to battle mode."""""
    battle_model.prep_combatant(mock_combatant_1)
    assert len(battle_model.combatants) == 1, "One combatant should be added to the list."

    battle_model.prep_combatant(mock_combatant_2)
    assert len(battle_model.combatants) == 2, "Two combatants should be present in the list."

    # Attempt to add a third combatant and expect an error
    with pytest.raises(ValueError, match="Combatant list is full"):
        battle_model.prep_combatant(Meal(id=3, meal="Meal C", price=12.0, cuisine="Chinese", difficulty="MED"))
    
