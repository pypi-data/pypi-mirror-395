"""
Hexadecimal text extraction module.

Extracts readable ASCII/UTF-8 text from binary files using pattern matching.
Useful for extracting text from files with unknown formats.
"""

import re
import logging
from typing import List, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


class HexExtractor:
    """
    Extract readable text from binary files.

    Uses pattern matching to find sequences of printable characters
    in binary data.
    """

    # Minimum length for a valid text string
    MIN_STRING_LENGTH = 4

    # Printable ASCII range
    PRINTABLE_ASCII = set(range(32, 127))
    PRINTABLE_ASCII.add(9)  # Tab
    PRINTABLE_ASCII.add(10)  # Line feed
    PRINTABLE_ASCII.add(13)  # Carriage return

    def __init__(self, min_length: int = 4, max_strings: int = 10000):
        """
        Initialize hex extractor.

        Args:
            min_length: Minimum string length to extract
            max_strings: Maximum number of strings to extract
        """
        self.min_length = max(min_length, 1)
        self.max_strings = max_strings

    def extract_from_file(
        self, file_path: Path, max_size: int = 10 * 1024 * 1024
    ) -> str:
        """
        Extract text from a binary file.

        Args:
            file_path: Path to file
            max_size: Maximum file size to process

        Returns:
            Extracted text
        """
        try:
            file_size = file_path.stat().st_size

            if file_size > max_size:
                logger.warning(
                    f"File {file_path} too large ({file_size} bytes), reading first {max_size} bytes"
                )
                read_size = max_size
            else:
                read_size = file_size

            with open(file_path, "rb") as f:
                data = f.read(read_size)

            return self.extract_from_bytes(data)

        except Exception as e:
            logger.error(f"Failed to extract text from {file_path}: {e}")
            return ""

    def extract_from_bytes(self, data: bytes) -> str:
        """
        Extract text from binary data.

        Args:
            data: Binary data

        Returns:
            Extracted text
        """
        strings = self._extract_strings(data)

        # Join strings with newlines and deduplicate
        text = "\n".join(strings)

        # Clean up excessive whitespace
        text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

        return text.strip()

    def _extract_strings(self, data: bytes) -> List[str]:
        """
        Extract printable strings from binary data.

        Args:
            data: Binary data

        Returns:
            List of extracted strings
        """
        strings = []
        current_string = []

        for byte in data:
            if byte in self.PRINTABLE_ASCII:
                current_string.append(chr(byte))
            else:
                if len(current_string) >= self.min_length:
                    string = "".join(current_string).strip()
                    if string:
                        strings.append(string)
                        if len(strings) >= self.max_strings:
                            break
                current_string = []

        # Don't forget the last string
        if len(current_string) >= self.min_length:
            string = "".join(current_string).strip()
            if string:
                strings.append(string)

        return strings[: self.max_strings]

    def extract_utf16_strings(self, data: bytes) -> List[str]:
        """
        Extract UTF-16 strings from binary data.

        Some binary formats (e.g., Windows executables) contain UTF-16 strings.

        Args:
            data: Binary data

        Returns:
            List of extracted UTF-16 strings
        """
        strings = []

        # Try both little-endian and big-endian
        for encoding in ["utf-16-le", "utf-16-be"]:
            try:
                # Decode and split on null characters
                decoded = data.decode(encoding, errors="ignore")
                parts = decoded.split("\x00")

                for part in parts:
                    # Filter out strings with too many non-printable chars
                    printable = "".join(c for c in part if c.isprintable())
                    if len(printable) >= self.min_length:
                        strings.append(printable.strip())

                        if len(strings) >= self.max_strings:
                            break

            except Exception as e:
                logger.debug(f"Failed to decode as {encoding}: {e}")
                continue

        return strings[: self.max_strings]

    def smart_extract(self, file_path: Path, max_size: int = 10 * 1024 * 1024) -> str:
        """
        Smart extraction that tries multiple methods.

        Args:
            file_path: Path to file
            max_size: Maximum file size to process

        Returns:
            Extracted text
        """
        try:
            file_size = file_path.stat().st_size

            if file_size > max_size:
                read_size = max_size
            else:
                read_size = file_size

            with open(file_path, "rb") as f:
                data = f.read(read_size)

            # Try ASCII extraction
            ascii_strings = self._extract_strings(data)

            # Try UTF-16 extraction
            utf16_strings = self.extract_utf16_strings(data)

            # Combine and deduplicate
            all_strings = list(dict.fromkeys(ascii_strings + utf16_strings))

            # Join with newlines
            text = "\n".join(all_strings)

            # Clean up
            text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

            return text.strip()

        except Exception as e:
            logger.error(f"Failed to extract text from {file_path}: {e}")
            return ""


def extract_text_from_unknown(file_path: Path, min_length: int = 4) -> str:
    """
    Convenience function to extract text from unknown file formats.

    Args:
        file_path: Path to file
        min_length: Minimum string length

    Returns:
        Extracted text
    """
    extractor = HexExtractor(min_length=min_length)
    return extractor.smart_extract(file_path)
