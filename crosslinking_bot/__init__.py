import argparse

from .version import __version__

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', '-v', action='version',
                        version='%(prog)s {}'.format(__version__))

    return parser.parse_args()
