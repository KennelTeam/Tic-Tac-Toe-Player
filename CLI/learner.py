import argparse
from colorama import init
from cli_commands import *
import sys


if __name__ == '__main__':
    init()
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", type=int)
    parser.add_argument("-p", type=int)
    parser.add_argument("--default", required=False, default="simple_neuro", type=str)
    parser.add_argument("--names", required=False, default="[]", type=str)
    parser.add_argument("--warning_level", required=False, type=str, default="warning")
    parser.add_argument("--show_statistics", required=False, action="store_true")
    try:
        args = parser.parse_args()
        print(args)
    except TypeError as e:
        error(e)


