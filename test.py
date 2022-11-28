from itertools import groupby


def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


def main():
    myList = [30, 30, 30]

    print(all_equal(myList))

    if __name__ == "__main__":
        main()
