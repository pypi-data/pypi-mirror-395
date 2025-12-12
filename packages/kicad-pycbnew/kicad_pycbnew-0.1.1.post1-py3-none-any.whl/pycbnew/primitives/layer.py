from enum import auto
from strenum import LowercaseStrEnum

from .kicad import SExprSerializable


class LayerCategory(LowercaseStrEnum):
    """
    Represents an enumeration for categorizing layers.

    This enumeration defines categories for different types of layers,
    each associated with a specific string value. It is primarily used
    for distinguishing between different application layers, such as
    signal-related layers and user-related layers.

    Attributes:
        Signal: Represents a layer related to signals.
        User: Represents a layer that pertains to users.
    """
    Signal = auto()
    User = auto()


class KLayer(SExprSerializable):
    """
    Represents a layer defined in the `KProject` class.

    This class encapsulates the properties and functionality for handling a
    specific layer in `KProject`. Each layer is defined by its `number`, `name`,
    `category`, and optionally a `nickname`. It provides method the `sexp_tree` for generating
    its own S-expression.

    :ivar number: The unique identifier of the layer.
    :type number: int
    :ivar name: The name of the layer.
    :type name: str
    :ivar category: The category of the layer.
    :type category: LayerCategory
    :ivar nickname: An optional nickname for the layer, defaults to None.
    :type nickname: str | None
    """
    def __init__(self,
                 number: int,
                 name: str,
                 category: LayerCategory,
                 nickname: str | None = None):
        super().__init__()
        self.nickname = nickname
        self.category = category
        self.number = number
        self.name = name

    def sexp_tree(self) -> list[list | str]:
        ret = [f'{self.number}', f'"{self.name}"', f'{self.category}']
        if self.nickname:
            ret.append(f'"{self.nickname}"')
        return ret
