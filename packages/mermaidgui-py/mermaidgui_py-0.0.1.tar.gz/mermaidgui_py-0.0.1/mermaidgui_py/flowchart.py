# pymermaid/flowchart.py
from .core import BaseDiagram, DiagramType

class Flowchart(BaseDiagram):
    """
    Class for generating Mermaid Flowchart diagrams.
    Example: Flowchart().node("A", "Start").link("A", "-->", "B").node("B", "Process")
    """
    def __init__(self, direction: str = 'TD'):
        if direction.upper() == 'LR':
            super().__init__(DiagramType.FLOWCHART_LR)
        else:
            super().__init__(DiagramType.FLOWCHART)

    def node(self, node_id: str, text: str = None, shape: str = 'default') -> 'Flowchart':
        """Adds a node. If text is not provided, node_id is used as text."""
        if text is None:
            text = node_id
        
        # Define specific shapes (e.g., rectangle, circle, rhombus)
        if shape == 'round': # Rounded rectangle
            element = f'{node_id}("{text}")'
        elif shape == 'stadium': # Stadium shape
            element = f'{node_id}[/{text}/]'
        elif shape == 'circle': # Circle
            element = f'{node_id}(({text}))'
        elif shape == 'rhombus': # Rhombus (decision)
            element = f'{node_id}{{"{text}"}}'
        elif shape == 'subroutine': # Subroutine
            element = f'{node_id}[[{text}]]'
        elif shape == 'asymmetric': # Asymmetric (database)
            element = f'{node_id}> {text}]'
        elif shape == 'hexagon': # Hexagon (Note: Mermaid doesn't have a direct hexagon syntax using '{{' and '}}' is often used as a template, not actual syntax)
            element = f'{node_id}{{"{text}"}}'
        elif shape == 'default': # Default rectangle
            element = f'{node_id}[{text}]'
        else: # Fallback for unknown shapes
            element = f'{node_id}[{text}]'
            print(f"Warning: Unknown shape '{shape}'. Using default rectangle for node '{node_id}'.")

        return self._add_element(element)

    def link(self, source_id: str, connector: str, target_id: str, text: str = None) -> 'Flowchart':
        """Adds a link (connector) between nodes."""
        if text:
            element = f'{source_id} {connector} |{text}| {target_id}'
        else:
            element = f'{source_id} {connector} {target_id}'
        return self._add_element(element)

    def subgraph(self, subgraph_id: str, title: str, nodes: list) -> 'Flowchart':
        """Adds a subgraph."""
        self._add_element(f'subgraph {title}')
        for node_id in nodes:
            self._add_element(f'  {node_id}')
        self._add_element('end')
        return self