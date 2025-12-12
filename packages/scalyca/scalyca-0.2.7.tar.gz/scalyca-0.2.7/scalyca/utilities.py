import argparse
from pathlib import Path


class ReadableDir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        path = Path(values)
        if not path.is_dir():
            raise argparse.ArgumentTypeError(f"ReadableDir: {path} is not a valid path")
        try:
            setattr(namespace, self.dest, path)
        except IOError:
            raise argparse.ArgumentTypeError(f"ReadableDir: {path} is not a readable directory")


class WriteableDir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        path = Path(values)
        path.mkdir(parents=True, exist_ok=True)

        if not path.is_dir():
            raise argparse.ArgumentTypeError(f"WriteableDir: {path} is not a valid path")
        try:
            setattr(namespace, self.dest, path)
        except IOError:
            raise argparse.ArgumentTypeError(f"WriteableDir: {path} is not a writeable directory")
