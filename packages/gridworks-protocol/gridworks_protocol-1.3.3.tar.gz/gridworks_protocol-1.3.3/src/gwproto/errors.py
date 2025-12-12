class SchemaError(Exception):
    """Base class for Schema errors"""


class AlgoError(Exception):
    """Base class for errors related to Algorand"""


class DcError(Exception):
    """Base class for dataclass errors"""


class RegistryError(Exception):
    """Base class for registry errors"""
