# pymermaid/core.py
import subprocess
import os
from enum import Enum

class DiagramType(Enum):
    """Enumeration for different Mermaid diagram types."""
    FLOWCHART = "graph TD" # Top-Down
    FLOWCHART_LR = "graph LR" # Left-Right
    SEQUENCE = "sequenceDiagram"
    CLASS = "classDiagram"

class BaseDiagram:
    """Base class for all Mermaid diagrams."""
    def __init__(self, diagram_type: DiagramType):
        self.diagram_type = diagram_type
        self._elements = [] # List to store diagram elements

    def _add_element(self, element: str):
        """Adds an element to the diagram. Returns self for method chaining."""
        self._elements.append(element)
        return self

    def generate(self) -> str:
        """Generates the Mermaid code for the current diagram."""
        diagram_code = [self.diagram_type.value]
        diagram_code.extend(self._elements)
        return "\n".join(diagram_code)

    def to_image(self, output_path: str, format: str = 'png', theme: str = 'default') -> bool:
        """
        Converts the generated Mermaid code into an image file.
        
        Note: This functionality requires Node.js and mermaid.cli to be installed on your system.
        You can install mermaid.cli using: `npm install -g @mermaid-js/mermaid-cli`
        """
        mermaid_code = self.generate()
        input_file = "temp_mermaid_input.mmd"
        
        try:
            # Save Mermaid code to a temporary file
            with open(input_file, "w", encoding="utf-8") as f:
                f.write(mermaid_code)

            # Use mermaid-cli to generate the image
            command = [
                "mmdc", # mermaid-cli executable command
                "-i", input_file,
                "-o", output_path,
                "-t", theme,
                "--backgroundColor", "transparent", # Make background transparent
            ]
            
            print(f"Executing command: {' '.join(command)}") # For debugging
            result = subprocess.run(command, capture_output=True, text=True, check=True, encoding="utf-8")
            
            if result.returncode == 0:
                print(f"Mermaid diagram saved to {output_path} successfully!")
                return True
            else:
                print(f"Error saving Mermaid diagram to image: {result.stderr}")
                return False
        except FileNotFoundError:
            print("Error: 'mmdc' command not found. Please install mermaid.cli:")
            print("  npm install -g @mermaid-js/mermaid-cli")
            print("  (Node.js and npm must be installed first.)")
            return False
        except subprocess.CalledProcessError as e:
            print(f"Error during image conversion: {e}")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
            return False
        finally:
            # Delete the temporary file
            if os.path.exists(input_file):
                os.remove(input_file)
