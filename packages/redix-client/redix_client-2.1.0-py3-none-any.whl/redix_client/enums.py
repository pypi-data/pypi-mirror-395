# redix_client/enums.py
from enum import Enum

class ConversionFlag(str, Enum):
    EDIFACT = "e - UN/EDIFACT/RMap"
    X12 = "x - X12"
    FIXED = "f - fixed-length flat file"
    XML = "c - XML"
    CSV = "t - CSV delimited variable-length flat file"
    NCPDP = "n - NCPDP"
    HL7 = "h - HL7"

class FileType(str, Enum):
    INPUT = "input"
    OUTPUT = "output"
    ERROR = "error"
    ACK = "ack"
    TA1 = "ta1"
    STAGING = "staging"
    SHARED = "shared"
    ARCHIVE = "archive"

class WarningLevel(int, Enum):
    STOP_ON_FIRST_ERROR = 0
    CONTINUE_WITH_WARNINGS = 1
    IGNORE_ALL_ERRORS = 2

class BatchJobStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    COMPLETED_WITH_ERRORS = "COMPLETED_WITH_ERRORS"
    FAILED = "FAILED"