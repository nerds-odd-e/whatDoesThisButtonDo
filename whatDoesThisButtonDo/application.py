from . import AIExploratoryTestAssistant
from .explorer import Explorer
from .test_scope import TestScope
from pathlib import Path
from typing import List
from .regression_test_proposal import RegressionTestProposal
import os


class Application:
    """
    Main application class for WhatDoesThisButtonDo.
    Handles initialization, test oracle loading, and test execution.
    """
    
    def __init__(self):
        pass
        
    def run(self, oracle_dir: str) -> None:
        """
        Main execution method that runs the test oracles
        
        Args:
            oracle_dir: Directory containing test oracle files
        """
        test_scope = TestScope()
        test_scope.load_test_oracles(oracle_dir)
        
        # Initialize OpenAI client with test oracles
        openai_client = AIExploratoryTestAssistant(
            test_oracles=test_scope.get_test_oracles(),
            api_key=os.getenv('OPENAI_API_KEY'),
            model="gpt-4o-mini"
        )
        
        # Collect all proposals
        all_proposals: List[RegressionTestProposal] = []
        
        # Create and run executors for each sandbox
        for sandbox in test_scope.get_testable_sandboxes():
            executor = (Explorer.create()
                    .with_sandbox(sandbox, {
                        "environment": "test",
                        "cleanup_enabled": True
                    })
                    .with_ai_assistant(openai_client)
                    .build())
            proposals = executor.explore()
            all_proposals.extend(proposals)
        
        # Ask user to confirm each proposal
        for proposal in all_proposals:
            print("\nTest Proposal:")
            print(f"Title: {proposal.test_title}")
            print(f"Description: {proposal.test_description}")
            print(f"Result: {proposal.test_result}")
            print(f"Conclusion: {proposal.test_conclusion}")
            
            while True:
                response = input("\nWould you like to keep this test? (y/n): ").lower()
                if response in ['y', 'n']:
                    break
                print("Please answer 'y' or 'n'")
            
            if response == 'y':
                # Create the regression tests directory if it doesn't exist
                regression_dir = Path(oracle_dir) / "regression_tests"
                regression_dir.mkdir(exist_ok=True)
                
                # Write the test to the appropriate file
                test_file = regression_dir / f"test_{proposal.sandbox_name}.py"
                proposal.write_to_file(test_file)
                print(f"Test written to {test_file}")