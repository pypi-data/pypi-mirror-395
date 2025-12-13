"""Exceptions for the MSunPV library."""


class MSunPVException(Exception):
    """Base exception of the pysma library."""


class MSunPVConnectionException(MSunPVException):
    """An error occurred in the connection with the device."""

class MSunPVXMLDataException(MSunPVException):
    """XML Data Exception"""
