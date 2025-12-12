"""String extraction component with multi-encoding support and categorization."""

import math
import mmap
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List


class StringCategory(Enum):
    """Categories for extracted strings."""

    URL = "url"
    FILE_PATH = "file_path"
    REGISTRY_KEY = "registry_key"
    ERROR_MESSAGE = "error_message"
    GENERAL = "general"


@dataclass
class ExtractedString:
    """Represents an extracted string with metadata."""

    value: str
    category: StringCategory
    offset: int
    encoding: str
    entropy: float


@dataclass
class StringResult:
    """Result of string extraction operation."""

    strings_by_category: dict[StringCategory, List[ExtractedString]]
    total_count: int
    truncated: bool


class StringExtractor:
    """Extracts and categorizes meaningful strings from executable files."""

    # Entropy threshold for filtering random/binary data
    ENTROPY_THRESHOLD = 4.5

    # Maximum number of strings to return
    MAX_STRINGS = 10000

    # File size threshold for using memory-mapped files (100MB)
    MMAP_THRESHOLD = 100 * 1024 * 1024

    # Chunk size for processing large files (10MB)
    CHUNK_SIZE = 10 * 1024 * 1024

    # Regex patterns for categorization
    URL_PATTERN = re.compile(r"(https?://|ftp://|file://)", re.IGNORECASE)
    FILE_PATH_PATTERN = re.compile(
        r"([a-zA-Z]:\\|\\\\|/[a-zA-Z0-9_\-./]+)", re.IGNORECASE
    )
    REGISTRY_KEY_PATTERN = re.compile(
        r"(HKEY_|Software\\|SYSTEM\\|CurrentVersion)", re.IGNORECASE
    )
    ERROR_MESSAGE_PATTERN = re.compile(
        r"(error|exception|failed|failure|warning|fatal)", re.IGNORECASE
    )

    def __init__(self, min_length: int = 4):
        """Initialize string extractor.

        Args:
            min_length: Minimum string length to extract (default: 4)
        """
        self.min_length = min_length

    def extract_strings(self, file_path: str) -> StringResult:
        """Extract meaningful strings from an executable file.

        Args:
            file_path: Path to the executable file

        Returns:
            StringResult containing categorized strings

        Raises:
            FileNotFoundError: If file does not exist
            PermissionError: If file cannot be read
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")

        # Get file size to determine processing strategy
        file_size = path.stat().st_size

        # Read file data using appropriate method
        try:
            if file_size > self.MMAP_THRESHOLD:
                # Use memory-mapped file for large files
                data = self._read_with_mmap(path)
            else:
                # Read entire file for smaller files
                with open(path, "rb") as f:
                    data = f.read()
        except PermissionError as e:
            raise PermissionError(f"Cannot read file: {file_path}") from e

        # Extract strings with multiple encodings
        all_strings: List[ExtractedString] = []

        # Try ASCII encoding
        all_strings.extend(self._extract_with_encoding(data, "ascii", "ascii"))

        # Try UTF-8 encoding
        all_strings.extend(self._extract_with_encoding(data, "utf-8", "utf-8"))

        # Try UTF-16 LE encoding
        all_strings.extend(self._extract_with_encoding(data, "utf-16-le", "utf-16"))

        # Remove duplicates (same value at same offset)
        unique_strings = self._deduplicate_strings(all_strings)

        # Filter by entropy and length
        filtered_strings = [
            s
            for s in unique_strings
            if len(s.value) >= self.min_length and s.entropy <= self.ENTROPY_THRESHOLD
        ]

        # Limit to MAX_STRINGS
        truncated = len(filtered_strings) > self.MAX_STRINGS
        if truncated:
            filtered_strings = filtered_strings[: self.MAX_STRINGS]

        # Group by category
        strings_by_category: dict[StringCategory, List[ExtractedString]] = {
            category: [] for category in StringCategory
        }

        for string in filtered_strings:
            strings_by_category[string.category].append(string)

        return StringResult(
            strings_by_category=strings_by_category,
            total_count=len(filtered_strings),
            truncated=truncated,
        )

    def _read_with_mmap(self, path: Path) -> bytes:
        """Read file using memory-mapped I/O for large files.

        Args:
            path: Path to the file

        Returns:
            File contents as bytes

        Raises:
            PermissionError: If file cannot be read
        """
        try:
            with open(path, "rb") as f:
                # Create memory-mapped file
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mmapped:
                    # Read the entire mapped region
                    return mmapped.read()
        except PermissionError as e:
            raise PermissionError(f"Cannot read file: {path}") from e

    def _extract_with_encoding(
        self, data: bytes, encoding: str, encoding_name: str, offset: int = 0
    ) -> List[ExtractedString]:
        """Extract strings using a specific encoding.

        Args:
            data: Raw file data
            encoding: Encoding to use for decoding
            encoding_name: Name to store in ExtractedString
            offset: Base offset to add to all string offsets (for chunked processing)

        Returns:
            List of extracted strings
        """
        strings: List[ExtractedString] = []

        # For UTF-16, we need to handle 2-byte characters
        if encoding == "utf-16-le":
            step = 2
        else:
            step = 1

        current_string: list[str] = []
        current_offset = 0
        i = 0

        while i < len(data):
            try:
                if encoding == "utf-16-le":
                    if i + 1 >= len(data):
                        break
                    char_bytes = data[i : i + 2]
                    char = char_bytes.decode(encoding, errors="strict")
                else:
                    char_bytes = bytes([data[i]])
                    char = char_bytes.decode(encoding, errors="strict")

                # Check if printable
                if char.isprintable() and not char.isspace():
                    if not current_string:
                        current_offset = i
                    current_string.append(char)
                elif char.isspace() and current_string:
                    # Allow spaces within strings
                    current_string.append(char)
                else:
                    # End of string
                    if current_string:
                        string_value = "".join(current_string).strip()
                        if len(string_value) >= self.min_length:
                            entropy = self._calculate_entropy(string_value)
                            category = self._categorize_string(string_value)
                            strings.append(
                                ExtractedString(
                                    value=string_value,
                                    category=category,
                                    offset=offset + current_offset,
                                    encoding=encoding_name,
                                    entropy=entropy,
                                )
                            )
                        current_string = []

                i += step
            except (UnicodeDecodeError, UnicodeError):
                # End current string and move on
                if current_string:
                    string_value = "".join(current_string).strip()
                    if len(string_value) >= self.min_length:
                        entropy = self._calculate_entropy(string_value)
                        category = self._categorize_string(string_value)
                        strings.append(
                            ExtractedString(
                                value=string_value,
                                category=category,
                                offset=offset + current_offset,
                                encoding=encoding_name,
                                entropy=entropy,
                            )
                        )
                    current_string = []
                i += step

        # Handle final string
        if current_string:
            string_value = "".join(current_string).strip()
            if len(string_value) >= self.min_length:
                entropy = self._calculate_entropy(string_value)
                category = self._categorize_string(string_value)
                strings.append(
                    ExtractedString(
                        value=string_value,
                        category=category,
                        offset=offset + current_offset,
                        encoding=encoding_name,
                        entropy=entropy,
                    )
                )

        return strings

    def _calculate_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of a string.

        Args:
            text: String to calculate entropy for

        Returns:
            Entropy value (higher = more random)
        """
        if not text:
            return 0.0

        # Count character frequencies
        char_counts: dict[str, int] = {}
        for char in text:
            char_counts[char] = char_counts.get(char, 0) + 1

        # Calculate entropy
        entropy = 0.0
        text_len = len(text)

        for count in char_counts.values():
            probability = count / text_len
            if probability > 0:
                entropy -= probability * math.log2(probability)

        return entropy

    def _categorize_string(self, text: str) -> StringCategory:
        """Categorize a string based on its content.

        Args:
            text: String to categorize

        Returns:
            StringCategory enum value
        """
        # Check patterns in order of specificity
        if self.URL_PATTERN.search(text):
            return StringCategory.URL

        if self.REGISTRY_KEY_PATTERN.search(text):
            return StringCategory.REGISTRY_KEY

        if self.FILE_PATH_PATTERN.search(text):
            return StringCategory.FILE_PATH

        if self.ERROR_MESSAGE_PATTERN.search(text):
            return StringCategory.ERROR_MESSAGE

        return StringCategory.GENERAL

    def _deduplicate_strings(
        self, strings: List[ExtractedString]
    ) -> List[ExtractedString]:
        """Remove duplicate strings (same value at same offset).

        Args:
            strings: List of extracted strings

        Returns:
            Deduplicated list
        """
        seen = set()
        unique = []

        for string in strings:
            key = (string.value, string.offset)
            if key not in seen:
                seen.add(key)
                unique.append(string)

        return unique
