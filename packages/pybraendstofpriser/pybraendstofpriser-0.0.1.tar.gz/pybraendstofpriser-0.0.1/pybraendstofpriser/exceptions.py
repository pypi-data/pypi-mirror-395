"""Exceptions for pybraendstofpriser."""


class ErrorFetchingData(Exception):
    """Exception raised for errors in fetching data from the website."""


class ErrorFetchingProduct(Exception):
    """Exception raised for errors in fetching a specific product."""
