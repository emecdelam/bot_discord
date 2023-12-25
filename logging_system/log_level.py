from dataclasses import dataclass


@dataclass
class Level:
    DEBUG: str = 'DEBUG'
    INFO: str = 'INFO'
    WARNING: str = 'WARNING'
    ERROR: str = 'ERROR'
    CRITICAL: str = 'CRITICAL'