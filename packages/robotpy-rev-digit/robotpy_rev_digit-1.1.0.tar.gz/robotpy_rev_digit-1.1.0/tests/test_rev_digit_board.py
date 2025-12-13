import pytest
import wpilib
from wpilib.simulation import AnalogInputSim, DIOSim

from robotpy_rev_digit.rev_digit_board import RevDigitBoard, format_float, format_string


class I2CSim:
    def __init__(self, i2c_obj: wpilib.I2C):
        self._buffer: list[bytes] = []
        self._i2c_obj = i2c_obj

    def writeBulk(self, array: bytes):
        self._buffer.append(array)

    @property
    def buffer(self) -> list[bytes]:
        return self._buffer


def test_rev_digit_instance():
    """Test that a RevDigit object can be created"""
    digit = RevDigitBoard()
    assert isinstance(digit, RevDigitBoard)
    assert isinstance(digit._i2c, wpilib.I2C)
    assert isinstance(digit._button_a, wpilib.DigitalInput)
    assert isinstance(digit._button_b, wpilib.DigitalInput)
    assert isinstance(digit._potentiometer, wpilib.AnalogInput)


@pytest.mark.parametrize("state", [True, False])
def test_rev_digit_button_a(state):
    """Test reading the state of Button A"""
    digit = RevDigitBoard()
    button_a = DIOSim(input=digit._button_a)
    button_b = DIOSim(input=digit._button_b)
    button_a.setValue(state)
    button_b.setValue(not state)
    assert digit.button_a is state


@pytest.mark.parametrize("state", [True, False])
def test_rev_digit_button_b(state):
    """Test reading the state of Button B"""
    digit = RevDigitBoard()
    button_a = DIOSim(input=digit._button_a)
    button_b = DIOSim(input=digit._button_b)
    button_a.setValue(not state)
    button_b.setValue(state)
    assert digit.button_b is state


@pytest.mark.parametrize("voltage", [0.0, 1.0, 3.3, 5.0])
def test_rev_digit_potentiometer(voltage):
    """Test reading the state of the potentiometer sensor"""
    digit = RevDigitBoard()
    potentiometer = AnalogInputSim(analogInput=digit._potentiometer)
    potentiometer.setVoltage(voltage)
    assert digit.potentiometer == voltage


def test_rev_digit_clear_display():
    """Test that display can be cleared"""
    digit = RevDigitBoard()
    digit._i2c = I2CSim(i2c_obj=digit._i2c)  # Use a simulated I2C interface
    digit.clear_display()
    expected_packets = [b"\x0f\x0f\x00\x00\x00\x00\x00\x00\x00\x00"]
    for actual, expected in zip(digit._i2c.buffer, expected_packets):
        assert actual == expected


def test_rev_digit_display_init():
    """Test initializing the display"""
    digit = RevDigitBoard()
    digit._i2c = I2CSim(i2c_obj=digit._i2c)  # Use a simulated I2C interface
    digit._init_display()
    expected_packets = [
        b"\x21",
        b"\xef",
        b"\x81",
        b"\x0f\x0f\x00\x00\x00\x00\x00\x00\x00\x00",
    ]
    for actual, expected in zip(digit._i2c.buffer, expected_packets):
        assert actual == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("A", b"\x0f\x0f\xf7\x00\x00\x00\x00\x00\x00\x00"),
        (0, b"\x0f\x0f\x3f\x00\x00\x00\x00\x00\x00\x00"),
        (0.1, b"\x0f\x0f\x06\x00\x3f\x40\x00\x00\x00\x00"),
    ],
)
def test_rev_digit_write_message(test_input, expected):
    """Test that display can display message"""
    digit = RevDigitBoard()
    digit._i2c = I2CSim(i2c_obj=digit._i2c)  # Use a simulated I2C interface
    digit.display_message(test_input)
    actual = digit._i2c.buffer[0]  # look at the first item in the buffer
    assert actual == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (1.1, "  1.1"),
        (-1.1, " -1.1"),
        (15.0, " 15.0"),
        (-15.0, "-15.0"),
        (-15.04, "-15.0"),
        (-15.05, "-15.1"),
        (999.9, "999.9"),
        (-99.9, "-99.9"),
        (1000.0, "####"),
        (-100.0, "####"),
    ],
)
def test_rev_digit_format_float(test_input, expected):
    assert format_float(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("A", "   A"),
        ("AB", "  AB"),
        ("ABC", " ABC"),
        ("ABCD", "ABCD"),
        ("A.", "  A."),
        ("a", "   A"),
    ],
)
def test_rev_digit_format_string(test_input, expected):
    assert format_string(test_input) == expected
