photos = {}


def set_photos():
    names = ["bomb.png", "flag.png", "repeat.png", "timer.png", "X.png", "x_test.png", "play.png"]
    for name in names:
        photos[name[:-4]] = f"photos/{name}"


def find_longest(array):
    longest = array[0]
    for el in array:
        if len(el) > len(longest):
            longest = el

    return longest


set_photos()
