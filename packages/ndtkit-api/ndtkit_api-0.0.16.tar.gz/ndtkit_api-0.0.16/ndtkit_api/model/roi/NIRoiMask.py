"""Wrapper for Java NIRoiMask class.

NIRoiMask is a specialized NIRoi representing mask ROIs. This module provides a
lightweight wrapper that mirrors the Java type and reuses the NIRoi wrapper behavior.
"""
from py4j.java_gateway import JavaObject

from ...ndtkit_socket_connection import gateway
from .NIRoi import NIRoi


class NIRoiMask(NIRoi):
    """Python wrapper for agi.ndtkit.api.model.roi.NIRoiMask."""

    def __init__(self, java_object: JavaObject):
        super().__init__(java_object)
