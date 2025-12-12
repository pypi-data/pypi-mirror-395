"""Framework detection component with signature matching."""

import re
from dataclasses import dataclass
from typing import List, Optional

import pefile

from exe_analyzer_mcp.config import load_framework_signatures


@dataclass
class Framework:
    """Represents a detected framework."""

    name: str
    version: Optional[str]
    confidence: float
    indicators: List[str]


class FrameworkDetector:
    """Detects frameworks used in executable files."""

    def __init__(self):
        """Initialize framework detector with signature database."""
        config = load_framework_signatures()
        self.framework_configs = config.get("frameworks", [])

    def detect_frameworks(self, pe: pefile.PE, strings: List[str]) -> List[Framework]:
        """Detect frameworks in a PE file.

        Args:
            pe: Parsed PE file object
            strings: List of extracted strings from the executable

        Returns:
            List of detected Framework objects
        """
        detected_frameworks: List[Framework] = []

        # Check for .NET framework first (uses CLR header)
        dotnet_framework = self._check_dotnet(pe, strings)
        if dotnet_framework:
            detected_frameworks.append(dotnet_framework)

        # Check other frameworks using string pattern matching
        for framework_config in self.framework_configs:
            framework_name = framework_config["name"]

            # Skip .NET frameworks as they're already checked
            if framework_name in [".NET Framework", ".NET Core"]:
                continue

            framework = self._check_framework_signatures(framework_config, strings)
            if framework:
                detected_frameworks.append(framework)

        return detected_frameworks

    def _check_dotnet(self, pe: pefile.PE, strings: List[str]) -> Optional[Framework]:
        """Check for .NET framework using CLR header.

        Args:
            pe: Parsed PE file object
            strings: List of extracted strings

        Returns:
            Framework object if .NET is detected, None otherwise
        """
        # Check for CLR header
        has_clr = False
        try:
            pe.parse_data_directories(
                directories=[
                    pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_COM_DESCRIPTOR"]
                ]
            )
            has_clr = hasattr(pe, "DIRECTORY_ENTRY_COM_DESCRIPTOR")
        except Exception:
            has_clr = False

        if not has_clr:
            return None

        # Determine if .NET Framework or .NET Core
        indicators = []
        version = None
        framework_name = ".NET Framework"

        # Check for .NET Core indicators
        dotnet_core_indicators = [
            "System.Private.CoreLib",
            "coreclr.dll",
            "hostfxr.dll",
            "hostpolicy.dll",
        ]

        for string in strings:
            for indicator in dotnet_core_indicators:
                if indicator.lower() in string.lower():
                    framework_name = ".NET Core"
                    indicators.append(string)
                    break

        # If not .NET Core, check for .NET Framework indicators
        if framework_name == ".NET Framework":
            dotnet_framework_indicators = [
                "mscoree.dll",
                "mscorlib",
                "System.Runtime",
                "clr.dll",
            ]

            for string in strings:
                for indicator in dotnet_framework_indicators:
                    if indicator.lower() in string.lower():
                        indicators.append(string)
                        break

        # Extract version if possible
        version_patterns = [
            r"v(\d+\.\d+\.\d+)",
            r"Version=(\d+\.\d+\.\d+\.\d+)",
        ]

        for string in strings:
            for pattern in version_patterns:
                match = re.search(pattern, string)
                if match:
                    version = match.group(1)
                    break
            if version:
                break

        # Add CLR header as indicator
        if not indicators:
            indicators = ["CLR Header Present"]

        return Framework(
            name=framework_name,
            version=version,
            confidence=1.0,  # CLR header is definitive
            indicators=indicators,
        )

    def _check_framework_signatures(
        self, framework_config: dict, strings: List[str]
    ) -> Optional[Framework]:
        """Check for framework using signature matching.

        Args:
            framework_config: Framework configuration with signatures
            strings: List of extracted strings

        Returns:
            Framework object if detected, None otherwise
        """
        framework_name = framework_config["name"]
        signatures = framework_config.get("signatures", [])
        version_patterns = framework_config.get("version_patterns", [])

        matched_indicators = []

        # Check for signature matches
        for string in strings:
            for signature in signatures:
                if signature.lower() in string.lower():
                    matched_indicators.append(string)
                    break

        # If no signatures matched, framework not detected
        if not matched_indicators:
            return None

        # Try to extract version
        version = None
        for string in strings:
            for pattern in version_patterns:
                if pattern.lower() in string.lower():
                    # Try to extract version number
                    version_match = re.search(r"(\d+\.\d+(?:\.\d+)?)", string)
                    if version_match:
                        version = version_match.group(1)
                        break
            if version:
                break

        # Calculate confidence based on number of matched signatures
        confidence = min(1.0, len(matched_indicators) / len(signatures))

        return Framework(
            name=framework_name,
            version=version,
            confidence=confidence,
            indicators=matched_indicators,
        )
