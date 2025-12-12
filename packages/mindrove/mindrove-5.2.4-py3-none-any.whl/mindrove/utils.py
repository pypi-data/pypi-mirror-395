import enum

from mindrove.exit_codes import MindRoveExitCodes, MindRoveError


class LogLevels(enum.IntEnum):
    """Enum to store all log levels supported by MindRove"""

    LEVEL_TRACE = 0  #:
    LEVEL_DEBUG = 1  #:
    LEVEL_INFO = 2  #:
    LEVEL_WARN = 3  #:
    LEVEL_ERROR = 4  #:
    LEVEL_CRITICAL = 5  #:
    LEVEL_OFF = 6  #:


def check_memory_layout_row_major(data, ndim):
    if data is None:
        raise MindRoveError('data is None',
                             MindRoveExitCodes.EMPTY_BUFFER_ERROR.value)
    if len(data.shape) != ndim:
        raise MindRoveError('wrong shape for filter data array, it should be %dd array' % ndim,
                             MindRoveExitCodes.INVALID_ARGUMENTS_ERROR.value)
    if not data.flags['C_CONTIGUOUS']:
        raise MindRoveError('wrong memory layout, should be row major, make sure you didnt tranpose array',
                             MindRoveExitCodes.INVALID_ARGUMENTS_ERROR.value)
