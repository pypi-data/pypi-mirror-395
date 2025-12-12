"""Enums for Validio resources."""

from enum import Enum


class IncidentGroupPriority(str, Enum):
    """Priority to use for incident groups."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
