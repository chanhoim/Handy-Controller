from itertools import groupby
import platform
from pynput import keyboard

COMBINATION = {keyboard.Key.cmd, keyboard.Key.ctrl}
current = set()


def on_press(key):
    if key in COMBINATION:
        current.add(key)
        if all(k in current for k in COMBINATION):
            print('All modifiers active!')
    if key == keyboard.Key.esc:
        listener.stop()


def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


def main():

    """
    Check OS
    """
    os = platform.system()  # Windows / Darwin(Mac)
    print(os)

    if os == "Windows":
        print("You are working on Windows")
    elif os == "Darwin":
        print("You are working on MacOSX")
    else:
        print("What?")
    on_press(keyboard.Key.f11)
    on_release(keyboard.Key.f11)
    """
    Check list
    """
    myList = [1, 1, 0, 0, 0]
    print(myList[2:5])
    print(all_equal(myList))


if __name__ == "__main__":
    main()
