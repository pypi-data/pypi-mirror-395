class MarshalError(RuntimeError):
    """
    Superclass of all marshalling or unmarshalling errors.
    """


class InvalidTypeCode(MarshalError):
    """
    Raised when an invalid type code is detected.
    """


class StreamFormatError(MarshalError):
    """
    Raised when the marshal stream is invalid in some form.
    """


class NotAMarshalFile(StreamFormatError):
    """
    Thrown when a file is not a valid Ruby marshal file.
    """


class StreamUnexpectedlyEndedError(StreamFormatError, EOFError):
    """
    Raised when there is an unexpected EOF.
    """


class ObjectMissingKeyError(MarshalError):
    """
    Raised when an object is missing a key when unmarshalling.
    """
