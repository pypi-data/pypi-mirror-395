# mermaidgui_py

## English Version

**mermaidgui_py** is an intuitive Python library designed to simplify the creation and programmatic management of Mermaid diagrams, with a strong focus on **GUI integration**. It provides a clean, object-oriented API to define various diagram types such as flowcharts, sequence diagrams, and class diagrams directly from your Python code. Additionally, it offers utility to convert these generated Mermaid codes into image files (PNG, JPG, SVG) using `mermaid.cli`.

### Features
*   **Intuitive API**: Construct Mermaid diagrams using Python objects and method chaining, abstracting the complex Mermaid syntax.
*   **Multiple Diagram Types**: Supports major Mermaid diagram types including Flowcharts (both Top-Down and Left-Right), Sequence Diagrams, and Class Diagrams.
*   **Image Export**: Convert any generated Mermaid code into image formats (PNG, JPG, SVG) effortlessly. (Requires `mermaid.cli` to be installed externally).
*   **Strong GUI Integration Focus**: Designed to be easily integrated into graphical user interfaces (GUIs) built with frameworks like PySide6, enabling developers to create intuitive visual diagram editing and generation tools.

### Installation

1.  **Python Package**:
    Install `mermaidgui_py` and its GUI dependencies using pip:
    ```bash
    pip install mermaidgui_py
    ```

2.  **`mermaid.cli` (for image export)**:
    For `mermaidgui_py`'s image export functionality, you need `Node.js` and `mermaid.cli` installed globally on your system.
    ```bash
    # First, ensure Node.js is installed (download from nodejs.org)
    npm install -g @mermaid-js/mermaid-cli
    ```
    Verify installation by running `mmdc -v` in your terminal.

### Quick Usage

```python
# Note: The internal package name remains 'pymermaid' for import statements
from pymermaid import Flowchart, SequenceDiagram, ClassDiagram

# Example 1: Create a simple Flowchart
flow = Flowchart(direction='LR') \
    .node("A", "Start Process", shape='round') \
    .link("A", "-->", "B", "Input Data") \
    .node("B", "Process Data") \
    .link("B", "--->", "C", "Data Processed") \
    .node("C", "End")

print("--- Flowchart Code ---")
print(flow.generate())
# Save as image (requires mermaid.cli)
flow.to_image("flowchart_example.png")


# Example 2: Create a simple Sequence Diagram
seq = SequenceDiagram() \
    .actor("User") \
    .participant("System") \
    .message("User", "->>", "System", "Request data") \
    .activate("System") \
    .message("System", "-->>", "User", "Data response") \
    .deactivate("System")

print("\n--- Sequence Diagram Code ---")
print(seq.generate())
seq.to_image("sequence_example.png")


# Example 3: Create a simple Class Diagram
cls = ClassDiagram() \
    .class_("Animal") \
    .attribute("-age: int") \
    .method("+eat()") \
    .class_("Dog", stereotype="<<abstract>>") \
    .attribute("+breed: string") \
    .method("+bark()") \
    .relationship("Dog", "--|>", "Animal")

print("\n--- Class Diagram Code ---")
print(cls.generate())
cls.to_image("class_example.png")