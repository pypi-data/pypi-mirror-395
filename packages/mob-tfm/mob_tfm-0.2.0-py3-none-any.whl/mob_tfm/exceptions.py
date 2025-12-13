

class InvalidGeneratorArgumentFormat(Exception):
    """Raised when an invalid format is provided to a generator argument."""
    pass

class InvalidColumnFormat(Exception):
    """Raised when an invalid column format is encountered."""
    pass

class UnknownGenerator(Exception):
    """Raised when the specified generator is unknown."""
    pass

class ImpossibleGeneration(Exception):
    """Raised when a generation is assumed impossible"""
    pass

class UnknownConverter(Exception):
    """Raised when the specified converter is unknown"""

class ImpossibleRowConvertion(Exception):
    """Raised when the convertion of a given row is impossible

    a convertion is impossible if:
    
        the length of the row is different from the one the converters
    """

