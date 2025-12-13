"""Wrapper for Java NIRoiSelection class.

NIRoiSelection extends NIRoi and provides selection-specific helpers like
statistics computation. This module mirrors the Java API and returns
"""
from py4j.java_gateway import JavaObject
from .NIRoi import NIRoi


class NIRoiSelection(NIRoi):
    """Python wrapper for agi.ndtkit.api.model.roi.NIRoiSelection."""

    def __init__(self, java_object: JavaObject):
        super().__init__(java_object)
