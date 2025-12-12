from enum import Enum


class JobStatus(Enum):
    QUEUED = 'QUEUED'
    RUNNING = 'RUNNING'
    FAILED = 'FAILED'
    COMPLETE = 'COMPLETE'
    CANCELLED = 'CANCELLED'
