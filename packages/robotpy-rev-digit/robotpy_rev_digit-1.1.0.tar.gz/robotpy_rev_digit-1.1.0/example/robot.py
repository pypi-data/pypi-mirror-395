import inspect

import wpilib
import wpilib.simulation

import robotpy_rev_digit

I2C_DEV_ADDR = 0x70
TEST_PATTERN = "   ABCDEFGHIJKLMNOPQRSTUVWXYZ*?@#   "


class MyRobot(wpilib.TimedRobot):
    """
    ##########################################################################
    RevDigitBoard Example Program
    This program is an example of how to use the RevDigitBoard class.
    """

    def robotInit(self):
        """
        This function is called upon program startup and should be used for any
        initialization code.
        """
        # Display information about this robot program on the driver station console
        print(inspect.getdoc(self))
        print(f"robotpy_rev_digit version: {robotpy_rev_digit.__version__}")

        # initialize the robot
        self.rev_digit = robotpy_rev_digit.RevDigitBoard()
        self.timer = wpilib.Timer()
        self.robot = wpilib.RobotController

    def robotPeriodic(self):
        """This function is called periodically regardless of the robot's state"""
        pass

    def teleopInit(self):
        """This function is run once each time the robot enters teleop mode."""
        self.timer.start()

    def teleopPeriodic(self):
        """This function is called periodically during teleop mode."""
        time = self.timer.get()
        idx = int(time // 1) % len(TEST_PATTERN)
        text = TEST_PATTERN[idx:]
        voltage = self.rev_digit.potentiometer

        # If neither button is pressed, show the timer
        if self.rev_digit.button_a and self.rev_digit.button_b:
            self.rev_digit.display_message(time)

        # If Button A is pressed, display the battery voltage
        elif not self.rev_digit.button_a:
            self.rev_digit.display_message(voltage)

        # If Button B is pressed, display the test pattern
        elif not self.rev_digit.button_b:
            self.rev_digit.display_message(text)

    def teleopExit(self):
        """This function is called when teleop mode ends."""
        self.timer.stop()

    def disabledPeriodic(self):
        """This function is called periodically when the robot is disabled"""
        voltage = self.robot.getBatteryVoltage()
        self.rev_digit.display_message(voltage)

    def _simulationInit(self):
        """This function is run once each time the robot enters simulation mode."""
        self.rev_digit = robotpy_rev_digit.SimDigitBoard()

    def _simulationPeriodic(self):
        """This function is called periodically during simulation mode."""
        self.rev_digit.update_simulation()


if __name__ == "__main__":
    wpilib.run(MyRobot)
