import os
import pathlib
import argparse


class ReadableDir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not os.path.isdir(values):
            raise argparse.ArgumentTypeError(f"ReadableDir: {values} is not a valid path")
        if os.access(values, os.R_OK):
            setattr(namespace, self.dest, values)
        else:
            raise argparse.ArgumentTypeError(f"ReadableDir: {values} is not a readable directory")


class WriteableDir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not os.path.isdir(values):
            raise argparse.ArgumentTypeError(f"WriteableDir: {values} is not a valid path")
        if os.access(values, os.W_OK):
            setattr(namespace, self.dest, values)
        else:
            raise argparse.ArgumentTypeError(f"WriteableDir: {values} is not a writeable directory")


def ReadableDirType(path: str) -> pathlib.Path:
    try:
        try_path = pathlib.Path(path)
        if not try_path.is_dir():
            raise argparse.ArgumentTypeError(f"ReadableDirType: {try_path} is not a valid path")
        if not os.access(try_path, os.R_OK):
            raise argparse.ArgumentTypeError(f"ReadableDirType: {try_path} is not a readable directory")
        return try_path
    except TypeError as e:
        raise argparse.ArgumentTypeError(f"ReadableDirType: {path} is not a string") from e



def WriteableDirType(path: str) -> pathlib.Path:
    try:
        try_path = pathlib.Path(path)
        if not try_path.is_dir():
            raise argparse.ArgumentTypeError(f"WriteableDirType: {try_path} is not a valid path")
        if not os.access(try_path, os.W_OK):
            raise argparse.ArgumentTypeError(f"WriteableDirType: {try_path} is not a writeable directory")
        return try_path
    except TypeError as e:
        raise argparse.ArgumentTypeError(f"WriteableDirType: {path} is not a string") from e

