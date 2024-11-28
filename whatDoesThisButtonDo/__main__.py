from .cli import CommandLineApplication

def main():
    """Entry point for the application"""
    cli = CommandLineApplication()
    cli.run()

if __name__ == "__main__":
    main() 