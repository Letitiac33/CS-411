import pytest
from unittest.mock import patch, MagicMock
from meal_max.models.battle_model import BattleModel
from meal_max.models.kitchen_model import Meal

RANDOM_NUMBER = 0.5  # Mocked random number for consistent test results

######################################################
#
#    Fixtures
#
######################################################

@pytest.fixture
def mock_combatant_1():
    return Meal(id=1, meal="Meal A", price=10.0, cuisine="Italian", difficulty="HIGH")

@pytest.fixture
def mock_combatant_2():
    return Meal(id=2, meal="Meal B", price=15.0, cuisine="Mexican", difficulty="LOW")

@pytest.fixture
def battle_model():
    return BattleModel()

######################################################
#
#    Tests for BattleModel
#
######################################################

@patch('meal_max.utils.random_utils.get_random', return_value=RANDOM_NUMBER)
@patch('meal_max.models.kitchen_model.update_meal_stats')
def test_battle(battle_model, mock_combatant_1, mock_combatant_2, mock_update_meal_stats, mock_get_random):
    """Test the battle function between two combatants."""
    # Prepare two combatants
    battle_model.prep_combatant(mock_combatant_1)
    battle_model.prep_combatant(mock_combatant_2)
    
    # Run the battle and check the winner
    winner = battle_model.battle()

    # Ensure one combatant is removed after the battle
    assert len(battle_model.combatants) == 1, "Only one combatant should remain after the battle."

    # Check that the winner is correctly chosen
    assert winner in [mock_combatant_1.meal, mock_combatant_2.meal], "The winner should be one of the two combatants."

    # Verify that update_meal_stats was called for both the winner and loser
    mock_update_meal_stats.assert_any_call(mock_combatant_1.id, 'win')
    mock_update_meal_stats.assert_any_call(mock_combatant_2.id, 'loss')

def test_prep_combatant(battle_model, mock_combatant_1, mock_combatant_2):
    """Test adding combatants to the battle model."""
    # Add the first combatant
    battle_model.prep_combatant(mock_combatant_1)
    assert len(battle_model.combatants) == 1, "One combatant should be added to the list."

    # Add the second combatant
    battle_model.prep_combatant(mock_combatant_2)
    assert len(battle_model.combatants) == 2, "Two combatants should be present in the list."

    # Attempt to add a third combatant and expect an error
    with pytest.raises(ValueError, match="Combatant list is full"):
        battle_model.prep_combatant(Meal(id=3, meal="Meal C", price=12.0, cuisine="Chinese", difficulty="MED"))

def test_clear_combatants(battle_model, mock_combatant_1, mock_combatant_2):
    """Test clearing all combatants."""
    # Add combatants
    battle_model.prep_combatant(mock_combatant_1)
    battle_model.prep_combatant(mock_combatant_2)
    
    # Clear the combatants and check that the list is empty
    battle_model.clear_combatants()
    assert len(battle_model.combatants) == 0, "Combatants list should be empty after clearing."

def test_get_battle_score(battle_model, mock_combatant_1, mock_combatant_2):
    """Test the calculation of battle scores for combatants."""
    score_1 = battle_model.get_battle_score(mock_combatant_1)
    score_2 = battle_model.get_battle_score(mock_combatant_2)

    # Calculate expected scores based on price, cuisine length, and difficulty modifier
    expected_score_1 = (mock_combatant_1.price * len(mock_combatant_1.cuisine)) - 1  # HIGH difficulty modifier is 1
    expected_score_2 = (mock_combatant_2.price * len(mock_combatant_2.cuisine)) - 3  # LOW difficulty modifier is 3

    assert score_1 == expected_score_1, f"Expected score {expected_score_1} for combatant 1, got {score_1}."
    assert score_2 == expected_score_2, f"Expected score {expected_score_2} for combatant 2, got {score_2}."

def test_battle_insufficient_combatants(battle_model, mock_combatant_1):
    """Test that a battle cannot start with fewer than two combatants."""
    # Add only one combatant
    battle_model.prep_combatant(mock_combatant_1)

    # Expect ValueError due to insufficient combatants
    with pytest.raises(ValueError, match="Two combatants must be prepped for a battle"):
        battle_model.battle()

def test_get_combatants(battle_model, mock_combatant_1, mock_combatant_2):
    """Test retrieving the current list of combatants."""
    # Add combatants
    battle_model.prep_combatant(mock_combatant_1)
    battle_model.prep_combatant(mock_combatant_2)

    # Retrieve and verify the combatants list
    combatants = battle_model.get_combatants()
    assert combatants == [mock_combatant_1, mock_combatant_2], "Combatants list does not match expected output."

def test_battle_tie_scenario(battle_model, mock_combatant_1, mock_combatant_2):
    """Test a tie scenario where both combatants have the same battle score."""
    # Override scores to force a tie
    with patch.object(battle_model, 'get_battle_score', side_effect=[100, 100]):
        battle_model.prep_combatant(mock_combatant_1)
        battle_model.prep_combatant(mock_combatant_2)

        # Run the battle
        winner = battle_model.battle()
        
        # Ensure the tie-breaking mechanism selects a winner
        assert winner in [mock_combatant_1.meal, mock_combatant_2.meal], "The winner should be one of the two combatants."

def test_add_combatant(battle_model, sample_meal1):
    """Test adding a combatant to BattleModel."""
    battle_model.prep_combatant(sample_meal1)
    assert len(battle_model.combatants) == 1
    assert battle_model.combatants[0].meal == "Meal A"

def test_add_duplicate_combatant(battle_model, sample_meal1):
    """Test error when adding a duplicate combatant."""
    battle_model.prep_combatant(sample_meal1)
    with pytest.raises(ValueError, match="Combatant list is full"):
        battle_model.prep_combatant(sample_meal1)

def test_clear_combatants(battle_model, sample_meal1):
    """Test clearing the combatant list."""
    battle_model.prep_combatant(sample_meal1)
    battle_model.clear_combatants()
    assert len(battle_model.combatants) == 0, "Combatants list should be empty after clearing"

def test_clear_empty_combatants(battle_model):
    """Test clearing an empty combatant list."""
    battle_model.clear_combatants()
    assert len(battle_model.combatants) == 0, "Combatants list should remain empty"

##################################################
# Battle Execution Test Cases
##################################################

@patch('meal_max.utils.random_utils.get_random', return_value=0.5)
def test_battle_successful(battle_model, sample_meal1, sample_meal2, mock_update_meal_stats, mock_get_random):
    """Test successful battle between two combatants."""
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)

    winner = battle_model.battle()
    assert winner in [sample_meal1.meal, sample_meal2.meal], "Winner should be one of the two combatants"

def test_battle_insufficient_combatants(battle_model, sample_meal1):
    """Test error when starting a battle with less than two combatants."""
    battle_model.prep_combatant(sample_meal1)
    with pytest.raises(ValueError, match="Two combatants must be prepped for a battle"):
        battle_model.battle()

##################################################
# Combatant Order Management Test Cases
##################################################

def test_move_combatant_to_first_position(battle_model, sample_combatants):
    """Test moving a combatant to the first position."""
    battle_model.combatants.extend(sample_combatants)
    battle_model.move_combatant_to_position(2, 1)
    assert battle_model.combatants[0].id == 2

def test_swap_combatants(battle_model, sample_combatants):
    """Test swapping positions of two combatants."""
    battle_model.combatants.extend(sample_combatants)
    battle_model.swap_combatants(1, 2)
    assert battle_model.combatants[0].id == 2
    assert battle_model.combatants[1].id == 1

def test_move_combatant_to_end(battle_model, sample_combatants):
    """Test moving a combatant to the end of the list."""
    battle_model.combatants.extend(sample_combatants)
    battle_model.move_combatant_to_end(1)
    assert battle_model.combatants[1].id == 1

##################################################
# Combatant Retrieval Test Cases
##################################################

def test_get_combatant_by_id(battle_model, sample_meal1):
    """Test retrieving a combatant by ID."""
    battle_model.prep_combatant(sample_meal1)
    combatant = battle_model.get_combatant_by_id(1)
    assert combatant.id == 1
    assert combatant.meal == "Meal A"

def test_get_all_combatants(battle_model, sample_combatants):
    """Test retrieving all combatants."""
    battle_model.combatants.extend(sample_combatants)
    all_combatants = battle_model.get_all_combatants()
    assert len(all_combatants) == 2
    assert all_combatants[0].id == 1
    assert all_combatants[1].id == 2

def test_get_current_combatant(battle_model, sample_combatants):
    """Test retrieving the current combatant in battle."""
    battle_model.combatants.extend(sample_combatants)
    current_combatant = battle_model.get_current_combatant()
    assert current_combatant.id == 1
    assert current_combatant.meal == "Meal A"

def test_get_combatant_count(battle_model, sample_combatants):
    """Test getting the number of combatants."""
    battle_model.combatants.extend(sample_combatants)
    assert battle_model.get_combatant_count() == 2, "Expected combatant count to be 2"