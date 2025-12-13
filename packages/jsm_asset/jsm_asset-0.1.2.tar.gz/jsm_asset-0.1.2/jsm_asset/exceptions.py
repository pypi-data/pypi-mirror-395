"""
Custom exceptions for jsm_asset
"""
class AQLQueryError(Exception):
    """Exception raised when an AQL query fails or cannot be parsed.

    Attributes:
      message (str): Human-readable error message.
      query (str): The AQL query string that caused the error.
    """

    def __init__(self, message, query):
        """Initialize the AQLQueryError.

        Args:
            message (str): A human-readable error message.
            query (str): The AQL query which caused the error.
        """
        super().__init__(message)
        self.query = query
