import pytest

from robotpy_rev_digit.rev_digit_board import SimDigitBoard


def test_sim_digit_instance():
    """Test that a SimDigit object can be created"""
    digit = SimDigitBoard()
    assert digit.button_a is True
    assert digit.button_b is True
    assert digit.potentiometer == 0


def test_sim_digit_display():
    """Test that a SimDigit object display can be set and cleared"""
    digit = SimDigitBoard()
    digit.display_message("ABC")
    assert digit.get_display_message() == "ABC"
    digit.clear_display()
    assert digit.get_display_message() == ""


@pytest.mark.parametrize("a,b", [(False, True), (True, False), (False, False)])
def test_sim_digit_buttons(a, b):
    """Test that a SimDigit object buttons can be set"""
    digit = SimDigitBoard()
    digit.button_a = a
    digit.button_b = b
    assert digit.button_a == a
    assert digit.button_b == b


@pytest.mark.parametrize(
    "value,expected", [(0.01, 0.01), (4.99, 4.99), (5.01, 5.00), (-0.01, 0)]
)
def test_sim_digit_potentiometer(value, expected):
    """Test that a SimDigit object potentiometer can be set with limits"""
    digit = SimDigitBoard()
    digit.potentiometer = value
    assert digit.potentiometer == expected
