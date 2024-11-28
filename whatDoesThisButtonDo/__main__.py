from pathlib import Path
from . import OpenAITestGenerator, GenerateTestPlanCommand
from .executor import Executor
from .test_sandbox import TestSandbox
from .test_scope import TestScope

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
    # Create an executor using the factory
    executor = (Executor.create()
                .with_sandbox(TestSandbox, {
                    "environment": "test",
                    "cleanup_enabled": True
                })
                .with_scope(TestScope())
                .build())
    
    # Use the executor
    executor.reset_environment()
    
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
        
        # Generate and print test plan for the first test case
        if test_cases:
            print("\nGenerating Test Plan for First Test Case...")
            test_plan_command = GenerateTestPlanCommand(
                openai_client.openai_client,
                test_cases[0],
                test_oracles
            )
            test_plan = test_plan_command.execute()
            print("\nTest Plan:")
            print(test_plan)
            
    except ValueError as e:
        print(f"Error: {e}")
        print("Please ensure OPENAI_API_KEY environment variable is set")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main() 