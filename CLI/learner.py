import os
import sys

import torch
import pycuda.driver as cuda
import numpy as np
main_path = os.path.join(sys.path[0], '..')
sys.path.insert(0, os.path.abspath(main_path))

import argparse
from colorama import init
from CLI.cli_commands import *
import Learning.learning
import NNLoader
import sys


def check_args(args) -> bool:
    if args.e <= 0:
        error(f"Number of epochs should be positive, but {args.e} is given")
        return False
    if args.p <= 0:
        error(f"Number of players should be positive, but {args.p} is given")
        return False
    if args.default not in NNLoader.NN_FACADES.keys():
        error(f"Wrong default facade name: {args.default}. Possible names: {', '.join(NNLoader.NN_FACADES.keys())}")
        return False
    possible_warnings = {'none', 'warning', 'error'}
    if args.warning_level not in possible_warnings:
        error(f"Wrong warning level: {args.warning_level}. Possible levels: {', '.join(list(possible_warnings))}")
        return False

    return True


def print_by_warning_level(message, warning_level):
    if warning_level == 'warning':
        warning(message)
    elif warning_level == 'error':
        error(message)


def check_args_warning(args, names):
    MIN_PLAYERS_CNT = 2
    MIN_EPOCHS_CNT = 2

    if args.e < MIN_EPOCHS_CNT:
        print_by_warning_level(f"Epochs number should be at least {MIN_EPOCHS_CNT}", args.warning_level)
    if args.p < MIN_PLAYERS_CNT:
        print_by_warning_level(f"Players number should be at least {MIN_PLAYERS_CNT}", args.warning_level)

    if len(names) != args.p:
        print_by_warning_level(f"Players count does not match names count. Players count: {args.p}, "
                               f"Names count: {len(names)}", args.warning_level)


if __name__ == '__main__':
    init()
    cuda.init()
    torch.cuda.set_device(0)
    print("initialized")

    # t = torch.Tensor(np.ndarray(shape=(10000, 10000))).to(torch.device("cuda"))

    parser = argparse.ArgumentParser(description="Run learning process")
    parser.add_argument("-e", type=int, help="Number of epochs")
    parser.add_argument("-p", type=int, help="Number of players (NN's)")
    parser.add_argument("--default", required=False, default="simple_neuro", type=str, help="Name of default NN facade")
    parser.add_argument("--names", required=False, default="", type=str,
                        help="Names of NNs (comma separated without spaces)")
    parser.add_argument("--warning_level", required=False, type=str, default="warning",
                        help="Level of warning importance. none, warning or error. Default is warning")
    parser.add_argument("--show_statistics", required=False, action="store_true",
                        help="If set shows statistics after run")
    try:
        args = parser.parse_args()

        if check_args(args):
            default = NNLoader.NN_FACADES[args.default]

            dir_names = args.names.split(',')
            if args.names == "":
                dir_names = []

            check_args_warning(args, dir_names)

            try:
                learning = Learning.learning.Learning(model_class=default,
                                                      players=args.p,
                                                      epochs=args.e,
                                                      dir_names=dir_names)

                epoch_id = 0
                print_progress_bar(epoch_id, args.e, prefix="Learning...", suffix=" done", length=50)
                for stats in learning.learn():
                    epoch_id += 1
                    suffix = stats.to_string()
                    print_progress_bar(epoch_id, args.e, prefix="Learning...", suffix=(" done\n" + suffix), length=50)
                success("Done!")
            except Exception as e:
                error(e)
            except KeyboardInterrupt:
                warning("\nProcess interrupted by input")
                exit(0)
    except TypeError as e:
        error(e)


