import argparse
from .application import Application

class CommandLineApplication:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='WhatDoesThisButtonDo test generator'
        )
        self.parser.add_argument(
            'oracle_dir',
            help='Directory containing test oracle files'
        )

    def run(self):
        """Run the command line application"""
        try:
            args = self.parser.parse_args()
            app = Application()
            app.run(args.oracle_dir)
        except Exception:
            exit(1) 