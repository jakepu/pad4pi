# pad4pi

This repo is branched from [brettmclean/pad4pi](https://github.com/brettmclean/pad4pi). I encountered serveral problems using that library in my senior project and I am trying to address them in this repo.

## Problems Addressed

1. The original library has bad performance when there are multiple key presses within a short period of time. The problem comes from the `getKey()` from [his code](https://github.com/brettmclean/pad4pi/blob/develop/pad4pi/rpi_gpio.py). It takes a bit extra time to poll `rowVal` and spend some time dealing with repeat related code. If the button is released before we poll the `colVal` or even `rowVal`, it will return a wrong key value. I modified the logic so that this problem is alleviated.
2. I do not know what the **repeat** feature is for in the original branch and it was not used in the examples so I deleted the related codes.
3. I changed some function names and variable names to fulfill [PEP 8](https://www.python.org/dev/peps/pep-0008) but I left the commom API untouched such as class name and method names `registerKeyPressHandler()`. If you follow the example in his library to write your code, this library should also work. However, `getKey()` is changed to `_get_key()` and shall not be used externally.

## Cautions

1. Although the performance is better than the original one, you should always keep in mind that there is still a chance this library will give a wrong key value. The wrong key value will be the leftmost key of the row of the key you press. I welcome any productive patch to this library to fix this. To avoid this problem easily, simply hold the button a bit longer when you press it.

## Usage

You will have to download the library from this GitHub repo because I have not uploaded it to a source where you can use pip to install.

I am pasting the example from [original library](https://github.com/brettmclean/pad4pi/blob/develop/pad4pi/rpi_gpio.py) because the exposed API is the same.

    from pad4pi import rpi_gpio

    KEYPAD = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        ["*", 0, "#"]
    ]

    ROW_PINS = [4, 14, 15, 17] # BCM numbering
    COL_PINS = [18, 27, 22] # BCM numbering

    factory = rpi_gpio.KeypadFactory()

    # Try factory.create_4_by_3_keypad
    # and factory.create_4_by_4_keypad for reasonable defaults
    keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

    def printKey(key):
        print(key)

    # printKey will be called each time a keypad button is pressed
    keypad.registerKeyPressHandler(printKey)

## License

This repo has to use GNU Lesser General Public License since the original library uses it.