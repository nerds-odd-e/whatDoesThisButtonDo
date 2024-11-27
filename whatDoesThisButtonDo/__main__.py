import sys
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m whatDoesThisButtonDo <test_folder>")
        sys.exit(1)
    
    test_folder = Path(sys.argv[1])
    if not test_folder.is_dir():
        print(f"Error: {test_folder} is not a directory")
        sys.exit(1)
    
    print(f"Starting exploratory testing on {test_folder}")
    # TODO: Implement testing logic

if __name__ == "__main__":
    main() 