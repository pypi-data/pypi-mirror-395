import subprocess
import sys
import uuid
from abc import ABC, abstractmethod


class SExprSerializable(ABC):
    """
    Abstract base class for objects that can be represented as S-expressions.

    Subclasses must implement the :meth:`sexp_tree` method to return a nested list
    representation of the object's structure, suitable for serialization into an S-expression.
    """

    @abstractmethod
    def sexp_tree(self) -> list[list | str]:
        """
        Returns the internal representation of the object as a nested list,
        where each element is either a string or another list. This structure
        is used by the project to generate the final S-expression text.

        :raises NotImplementedError: If the subclass does not implement this method.
        :return: A nested list representing the structure of the S-expression.
        :rtype: list[list | str]
        """
        pass


class KiCadObject(SExprSerializable):
    """
    Abstract base class for KiCad-related objects.

    This class extends :class:`SExprSerializable` by adding a unique identifier (UUID)
    to each instance. It serves as a base for KiCad objects that require both
    an S-expression representation and a persistent unique ID.

    Subclasses must implement the :meth:`sexp_tree` method to define their S-expression structure.

    :ivar uuid: A unique identifier automatically generated for the instance.
    :vartype uuid: str
    """

    def __init__(self):
        """
        Initializes a new instance of :class:`KiCadObject` with an automatically
        generated UUID.
        """
        self.uuid = str(uuid.uuid4())


def get_kicad_version():
    """
    Execute 'kicad-cli version' and return the version string.
    Returns None if KiCadObject is not found or an error occurs.
    """
    try:
        # Exécute "kicad-cli version" et récupère la sortie
        result = subprocess.run(
            ["kicad-cli", "version"],
            capture_output=True,  # capture stdout and stderr
            text=True,  # return output as string
            check=True  # raise exception if the command fails
        )
        version = result.stdout.strip()
        try:
            return tuple(map(int, version.split('.')))
        except ValueError:
            return None
    except FileNotFoundError:
        # KiCadObject was not found
        return None
    except subprocess.CalledProcessError as e:
        # The command failed for another reason
        print(f"Erreur lors de l'exécution de KiCadObject : {e}", file=sys.stderr)
        return None
