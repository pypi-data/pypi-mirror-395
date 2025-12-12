class DCSException(Exception):
    """Base exception for DCS client"""
    pass

class ValidationError(DCSException):
    """Raised when data does not match the contract"""
    pass

class ContractNotFoundError(DCSException):
    """Raised when the requested contract does not exist"""
    pass

class AuthenticationError(DCSException):
    """Raised when API key is invalid"""
    pass
