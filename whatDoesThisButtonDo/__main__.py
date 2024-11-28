import argparse
from .application import Application

def main():
    """Entry point for the application"""
    parser = argparse.ArgumentParser(description='WhatDoesThisButtonDo test generator')
    parser.add_argument('oracle_dir', help='Directory containing test oracle files')
    
    try:
        args = parser.parse_args()
        app = Application()
        app.run(args.oracle_dir)
    except Exception:
        exit(1)

if __name__ == "__main__":
    main() 