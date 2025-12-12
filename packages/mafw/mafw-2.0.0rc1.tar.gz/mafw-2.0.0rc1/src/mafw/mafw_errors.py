#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Module defines MAFw exceptions
"""


class MAFwException(Exception):
    """Base class for MAFwException"""

    pass


class ProcessorParameterError(MAFwException):
    """Error with a processor parameter"""

    pass


class InvalidConfigurationError(MAFwException):
    """Error with the configuration of a processor"""

    pass


class MissingOverloadedMethod(UserWarning):
    """
    Warning issued when the user did not overload a required method.

    It is a warning and not an error because the execution framework might still work, but the results might be
    different from what is expected.
    """

    pass


class MissingSuperCall(UserWarning):
    """
    Warning issued when the user did not invoke the super method for some specific processor methods.

    Those methods (like :meth:`~mafw.processor.Processor.start` and :meth:`~mafw.processor.Processor.finish`) have not
    empty implementation also in the base class, meaning that if the user forgets to call *super* in their overloads,
    then the basic implementation will be gone.

    It is a warning and not an error because the execution framework might sill work, but the results might be
    different from what is expected.
    """

    pass


class AbortProcessorException(MAFwException):
    """Exception raised during the execution of a processor requiring immediate exit."""

    pass


class RunnerNotInitialized(MAFwException):
    """Exception raised when attempting to run a not initialized Runner."""

    pass


class InvalidSteeringFile(MAFwException):
    """Exception raised when validating an invalid steering file"""

    pass


class UnknownProcessor(MAFwException):
    """Exception raised when an attempt is made to create an unknown processor"""

    pass


class UnknownDBEngine(MAFwException):
    """Exception raised when the user provided an unknown db engine"""

    pass


class MissingDatabase(MAFwException):
    """Exception raised when a processor requiring a database connection is being operated without a database"""


class MissingAttribute(MAFwException):
    """Exception raised when an attempt is made to execute a statement without a required parameter/attributes"""


class ParserConfigurationError(MAFwException):
    """Exception raised when an error occurred during the configuration of a filename parser"""


class ParsingError(MAFwException):
    """Exception raised when a regular expression parsing failed"""


class MissingSQLStatement(MAFwException):
    """Exception raised when a Trigger is created without any SQL statements."""


class UnsupportedDatabaseError(Exception):
    """Error raised when a feature is not supported by the database."""


class ModelError(MAFwException):
    """Exception raised when an error in a DB Model class occurs"""


class MissingOptionalDependency(UserWarning):
    """UserWarning raised when an optional dependency is required"""


class PlotterMixinNotInitialized(MAFwException):
    """Exception raised when a plotter mixin has not properly initialized"""
