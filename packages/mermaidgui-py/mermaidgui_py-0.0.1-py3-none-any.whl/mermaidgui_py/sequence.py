# pymermaid/sequence.py
from .core import BaseDiagram, DiagramType

class SequenceDiagram(BaseDiagram):
    """
    Class for generating Mermaid Sequence diagrams.
    Example: SequenceDiagram().participant("User").actor("System").message("User", "->>", "System", "Request")
    """
    def __init__(self):
        super().__init__(DiagramType.SEQUENCE)
        self._participants = set() # Set to prevent duplicate participants

    def participant(self, name: str) -> 'SequenceDiagram':
        """Adds a generic participant."""
        if name not in self._participants:
            self._add_element(f'participant {name}')
            self._participants.add(name)
        return self

    def actor(self, name: str) -> 'SequenceDiagram':
        """Adds an actor (person icon)."""
        if name not in self._participants:
            self._add_element(f'actor {name}')
            self._participants.add(name)
        return self

    def message(self, source: str, connector: str, target: str, message_text: str) -> 'SequenceDiagram':
        """Adds a message. Connector can be '->>', '->', '-->', '-->>', etc."""
        # Automatically add participants if not already registered
        if source not in self._participants:
            self.participant(source)
        if target not in self._participants:
            self.participant(target)

        return self._add_element(f'{source} {connector} {target}: {message_text}')
    
    def activate(self, participant_name: str) -> 'SequenceDiagram':
        """Activates a participant."""
        return self._add_element(f'activate {participant_name}')

    def deactivate(self, participant_name: str) -> 'SequenceDiagram':
        """Deactivates a participant."""
        return self._add_element(f'deactivate {participant_name}')

    def note(self, participant_name: str, position: str, text: str) -> 'SequenceDiagram':
        """Adds a note. Position can be 'left of', 'right of', 'over'."""
        return self._add_element(f'Note {position} {participant_name}: {text}')

    def loop(self, description: str, steps: list) -> 'SequenceDiagram':
        """Adds a loop block."""
        self._add_element(f'loop {description}')
        self._elements.extend(steps) # Extend with a list of predefined messages/steps
        self._add_element('end')
        return self