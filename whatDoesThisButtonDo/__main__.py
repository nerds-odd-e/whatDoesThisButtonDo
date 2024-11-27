from pathlib import Path
from .openai_test_generator import OpenAITestGenerator

def load_test_oracles(oracle_dir: str) -> list:
    """
    Load all test oracle markdown files from the specified directory
    """
    oracles = []
    oracle_path = Path(oracle_dir)
    
    for file in oracle_path.glob("*.md"):
        with open(file, 'r') as f:
            oracles.append({
                'name': file.name,
                'content': f.read()
            })
    
    return oracles

def main():
    # Load test oracles
    oracle_dir = "test_oracles"
    test_oracles = load_test_oracles(oracle_dir)
    
    try:
        # Initialize OpenAI client
        openai_client = OpenAITestGenerator()
        
        # Generate test cases directly using chat completion
        test_cases = openai_client.generate_test_cases(test_oracles)
        
        # Print generated test cases
        print("Generated Test Cases:")
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest Case {i}:")
            print(test_case)
            
    except ValueError as e:
        print(f"Error: {e}")
        print("Please ensure OPENAI_API_KEY environment variable is set")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main() 