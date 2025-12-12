# pymermaid/class_diagram.py
from .core import BaseDiagram, DiagramType

class ClassDiagram(BaseDiagram):
    """
    Class for generating Mermaid Class diagrams.
    Example: ClassDiagram().class_("Animal").method("eat()").attribute("age: int")
    """
    def __init__(self):
        super().__init__(DiagramType.CLASS)
        self._current_class = None

    def class_(self, class_name: str, stereotype: str = None) -> 'ClassDiagram':
        """Defines a class."""
        self._current_class = class_name
        if stereotype:
            return self._add_element(f'class {class_name} <<{stereotype}>>')
        return self._add_element(f'class {class_name}')

    def attribute(self, attr_text: str) -> 'ClassDiagram':
        """Adds an attribute to the current class. E.g., '+field: type'."""
        if not self._current_class:
            raise ValueError("Must define a class using class_() first.")
        return self._add_element(f'{self._current_class} : {attr_text}')

    def method(self, method_text: str) -> 'ClassDiagram':
        """Adds a method to the current class. E.g., '+method(params): returnType'."""
        if not self._current_class:
            raise ValueError("Must define a class using class_() first.")
        return self._add_element(f'{self._current_class} : {method_text}')

    def relationship(self, source_class: str, connector: str, target_class: str, label: str = None) -> 'ClassDiagram':
        """Defines a relationship between classes. E.g., "Human --|> Mammal", "Car <|-- Engine"."""
        if label:
            element = f'{source_class} {connector} {target_class} : {label}'
        else:
            element = f'{source_class} {connector} {target_class}'
        return self._add_element(element)