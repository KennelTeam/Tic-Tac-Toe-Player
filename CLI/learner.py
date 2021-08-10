import argparse
from colorama import init
from cli_commands import print_progress_bar, print_colored
import sys


if __name__ == '__main__':
    init()
    parser = argparse.ArgumentParser()
    parser.add_argument("-t")
    parser.add_argument("-q")
    args = parser.parse_args()

    print_colored(args.q, "red", "on_green")
    print_colored(args.t)


    import time

    # A List of Items
    items = list(range(0, 57))
    l = len(items)

    # Initial call to print 0% progress
    print_progress_bar(0, l, prefix='Progress:', suffix='complete', length=50)
    for i, item in enumerate(items):
        # Do stuff...
        time.sleep(0.1)
        # Update Progress Bar
        print_progress_bar(i + 1, l, prefix='Progress:', suffix='complete', length=50)
