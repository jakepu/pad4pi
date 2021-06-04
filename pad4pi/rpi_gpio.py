import RPi.GPIO as GPIO
import time

DEFAULT_KEY_DELAY = 300

"""
CAUTIONS
1. if the button is released before it polls the column number,
    this library will return the leftmost value in that row
2. PUT A RESISTOR WITH VALUE > 200 OHM BETWEEN THE COLUMN PADS AND OUTPUT PINS 
    TO AVOID SHORTING (https://github.com/brettmclean/pad4pi/pull/17/commits/254ac67c8ce71f1d788a02f2954fcb30a7b72f91)
"""

class KeypadFactory():

    def create_keypad(self, keypad=None, row_pins=None, col_pins=None, key_delay=DEFAULT_KEY_DELAY, gpio_mode=GPIO.BCM):

        if keypad is None:
            keypad = [
                [1,2,3],
                [4,5,6],
                [7,8,9],
                ["*",0,"#"]
            ]

        if row_pins is None:
            row_pins = [4,14,15,17]

        if col_pins is None:
            col_pins = [18,27,22]

        return Keypad(keypad, row_pins, col_pins, key_delay, gpio_mode)

    def create_4_by_3_keypad(self):

        KEYPAD = [
            [1,2,3],
            [4,5,6],
            [7,8,9],
            ["*",0,"#"]
        ]

        ROW_PINS = [4,14,15,17]
        COL_PINS = [18,27,22]

        return self.create_keypad(KEYPAD, ROW_PINS, COL_PINS)

    def create_4_by_4_keypad(self):

        KEYPAD = [
            [1,2,3,"A"],
            [4,5,6,"B"],
            [7,8,9,"C"],
            ["*",0,"#","D"]
        ]

        ROW_PINS = [4,14,15,17]
        COL_PINS = [18,27,22,23]

        return self.create_keypad(KEYPAD, ROW_PINS, COL_PINS)

class Keypad():
    def __init__(self, keypad, row_pins, col_pins, key_delay=DEFAULT_KEY_DELAY, gpio_mode=GPIO.BCM):
        self._handlers = []

        self._keypad = keypad
        self._row_pins = row_pins
        self._col_pins = col_pins
        self._key_delay = key_delay
        GPIO.setmode(gpio_mode)
        self._set_rows_as_input()
        self._set_columns_as_output()

    def registerKeyPressHandler(self, handler):
        self._handlers.append(handler)

    def unregisterKeyPressHandler(self, handler):
        self._handlers.remove(handler)

    def clearKeyPressHandlers(self):
        self._handlers = []

    def _repeatTimer(self):
        self._repeat_timer = None
        self._onKeyPress(None)

    def _on_key_press_row_0(self, channel):
        key_pressed = self._get_key(0)
        if key_pressed is not None:
            for handler in self._handlers:
                handler(key_pressed)
    def _on_key_press_row_1(self, channel):
        key_pressed = self._get_key(1)
        if key_pressed is not None:
            for handler in self._handlers:
                handler(key_pressed)
    def _on_key_press_row_2(self, channel):
        key_pressed = self._get_key(2)
        if key_pressed is not None:
            for handler in self._handlers:
                handler(key_pressed)
    def _on_key_press_row_3(self, channel):
        key_pressed = self._get_key(3)
        if key_pressed is not None:
            for handler in self._handlers:
                handler(key_pressed)
    def _on_key_press_row_4(self, channel):
        key_pressed = self._get_key(4)
        if key_pressed is not None:
            for handler in self._handlers:
                handler(key_pressed)

    self.call_back_list = [_on_key_press_row_0, _on_key_press_row_1, _on_key_press_row_2,
                           _on_key_press_row_3, _on_key_press_row_4]

    def _set_rows_as_input(self):
        # Set all rows as input
        for i in range(len(self._row_pins)):
            GPIO.setup(self._row_pins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(self._row_pins[i], GPIO.FALLING, callback=self.call_back_list[i], bouncetime=self._key_delay)

    def _set_columns_as_output(self):
        # Set all columns as output low
        for j in range(len(self._col_pins)):
            GPIO.setup(self._col_pins[j], GPIO.OUT)
            GPIO.output(self._col_pins[j], GPIO.LOW)

    """
    if the button is released before it polls the column number,
    it will return the leftmost value in that row
    """
    def _get_key(self, row_val):

        key_val = None

        # Scan columns for pressed key
        col_val = None
        for i in range(len(self._col_pins)):
            GPIO.output(self._col_pins[i], GPIO.HIGH)
            if GPIO.input(self._row_pins[row_val]) == GPIO.HIGH:
                GPIO.output(self._col_pins[i], GPIO.LOW)
                col_val = i
                break
            GPIO.output(self._col_pins[i], GPIO.LOW)
        # if the button is released before I poll the column number,
        # it will return the leftmost value in that row
        key_val = self._keypad[row_val][col_val]

        return key_val



if __name__ == "__main__":
    from pad4pi import rpi_gpio

    KEYPAD = [
        ["F1", "F2", "#", "*"],
        [1, 2, 3, "Up"],
        [4, 5, 6, "Down"],
        [7, 8, 9, "Esc"],
        ["Left", 0, "Right", "Ent"]
        ]
    ROW_PINS = [4, 17, 18, 27, 22]
    COL_PINS = [9, 10, 24, 23]
    kp = rpi_gpio.KeypadFactory().create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS, key_delay=100)
    def printkey(key):
        print(key)
    kp.registerKeyPressHandler(printkey)
    i = raw_input('')
