from .kicad import KiCadObject


class KNet(KiCadObject):
    """
    Represents a net within a KiCadObject schematic or PCB design.

    This class is used to handle a KiCadObject net, which is a logical connection
    between pins in circuit design. It provides methods for exporting the
    net in S-expression format, comparison of instances, and hashing for
    use in collections.

    :ivar name: The name of the net.
    :type name: str
    :ivar number: The identifier number of the net (must be unique across all nets in the design). Must be greater than 0.
    :type number: int
    """
    def __init__(self, number: int, name: str):
        super().__init__()
        if number <= 0:
            raise ValueError("Net number must be greater than 0.")
        self.number = number
        self.name = name

    def sexp_tree(self) -> list[list | str]:
        return ['net', f'{self.number}', f'"{self.name}"']

    def __repr__(self):
        return f"Net(number={self.number}, name={self.name})"

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.number == other.number

    def __hash__(self):
        return hash((self.__class__, self.number))