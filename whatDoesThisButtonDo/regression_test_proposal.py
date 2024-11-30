from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path
import textwrap

@dataclass
class TestStep:
    tool_call: str
    action: str
    parameters: Optional[Dict[str, Any]] = None

@dataclass
class RegressionTestProposal:
    """Represents a proposal for a regression test based on an exploratory test run"""
    sandbox_name: str
    test_title: str
    test_description: str
    steps: List[TestStep] = field(default_factory=list)
    test_result: str = ""
    test_conclusion: str = ""
    
    def add_step(
        self, 
        tool_call: str, 
        action: str, 
        parameters: Optional[Dict[str, Any]] = None
    ):
        """Add a test step to the proposal"""
        self.steps.append(TestStep(tool_call, action, parameters))
    
    def write_to_file(self, output_path: Path) -> None:
        """Write or append this test to a pytest file"""
        # Prepare the test function name
        test_name = f"test_{self.test_title.lower().replace(' ', '_')}"
        
        # Generate the test code
        test_code = self._generate_test_code(test_name)
        
        # Create or append to the file
        mode = 'a' if output_path.exists() else 'w'
        with open(output_path, mode) as f:
            if mode == 'w':
                # Write imports if creating new file
                f.write("import pytest\n")
                f.write(
                    "from whatDoesThisButtonDo.testable_sandbox "
                    "import TestableSandbox\n"
                )
                f.write("from pathlib import Path\n\n\n")
            
            f.write(test_code)
            f.write("\n\n")
    
    def _generate_test_code(self, test_name: str) -> str:
        """Generate the pytest code for this test"""
        code = [
            f"def {test_name}():",
            '    """',
            f"    {self.test_description}",
            '    """',
            "    # Initialize sandbox",
            f"    sandbox = TestableSandbox(Path('test_oracles/{self.sandbox_name}'))",
            "    try:",
            "        possible_actions = sandbox.start()"
        ]
        
        # Add each test step
        for step in self.steps:
            if step.tool_call == "assertion_for_regression":
                params_str = ", ".join(
                    f"{k}={repr(v)}" 
                    for k, v in step.parameters.items()
                )
                code.append("        sandbox.execute_assertion(")
                code.append(f"            '{step.action}',")
                code.append(f"            {{{params_str}}},")
                code.append("            sandbox.read_state()")
                code.append("        )")
            else:
                if step.parameters:
                    params_str = ", ".join(
                        f"{k}={repr(v)}" 
                        for k, v in step.parameters.items()
                    )
                    code.append(
                        f"        possible_actions = "
                        f"sandbox.execute_action('{step.action}', {{{params_str}}})"
                    )
                else:
                    code.append(
                        f"        possible_actions = "
                        f"sandbox.execute_action('{step.action}')"
                    )
        
        # Add teardown in finally block
        code.extend([
            "    finally:",
            "        sandbox.teardown()"
        ])
        
        return "\n".join(textwrap.indent(line, ' ' * 4) for line in code) 