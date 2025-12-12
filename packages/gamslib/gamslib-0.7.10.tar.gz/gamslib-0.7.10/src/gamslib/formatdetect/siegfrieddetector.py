"""A detector that uses the  pygfried library to detect file formats.

Pygfried is the python wrapper for the Siegfried file format identification tool.

This module provides the SiegrfriedDetector class, which uses Pygfried to identify file formats.
It includes logic to  to integrate with GAMSlib's
format detection infrastructure.
"""

import warnings
from pathlib import Path

import pygfried

from . import jsontypes, xmltypes
from .formatdetector import DEFAULT_TYPE, FormatDetector
from .formatinfo import FormatInfo


class SiegfriedDetector(FormatDetector):
    """
    Detector that uses the Pygfried library to detect file formats.

    Uses Siegfried's prediction engine to identify file types and MIME types.
    """

    def __init__(self):
        """
        Initialize the SiegfriedDetector.
        """
        self._detector_name = (
            f"{self.__class__.__name__} (Siegfried {pygfried.version()})"
        )

    def _extract_pronom_info(
        self,
        matches: list[dict[str, str]],
    ) -> dict[str, str] | None:
        "Return the pronom match info from the list of matches."
        for match in matches:
            if match["ns"] == "pronom":
                return match
        return None

    def guess_file_type(self, filepath: Path) -> FormatInfo:
        """
        Detect the format of a file using Pygfried and return a FormatInfo object.

        Args:
            filepath (Path): Path to the file to be analyzed.

        Returns:
            FormatInfo: An object containing the detected format information.
        """
        mime_type = DEFAULT_TYPE
        subtype = None
        subtype = None
        pronom_id = None

        data = pygfried.identify(str(filepath), detailed=True)
        if data and len(data["files"]) == 1:
            result = data["files"][0]
            pronom_info = self._extract_pronom_info(result.get("matches", []))
            mime_type = pronom_info.get("mime", DEFAULT_TYPE)
            pronom_id = pronom_info.get("id")
        else:
            warnings.warn(
                f"Could not determine mimetype for {filepath}. Using default type."
            )
        if mime_type is None or mime_type == "application/undefined":
            mime_type = DEFAULT_TYPE
            warnings.warn(
                f"Could not determine mimetype for {filepath}. Using default type."
            )
        elif xmltypes.is_xml_type(mime_type):
            mime_type, subtype = xmltypes.get_format_info(filepath, mime_type)
        elif jsontypes.is_json_type(mime_type):
            mime_type, subtype = jsontypes.get_format_info(filepath, mime_type)
        return FormatInfo(
            detector=self._detector_name,
            mimetype=mime_type,
            subtype=subtype,
            pronom_id=pronom_id,
        )

