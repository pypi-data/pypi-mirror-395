"""Language inference component for determining programming language."""

from dataclasses import dataclass
from typing import List

import pefile

from exe_analyzer_mcp.config import load_compiler_signatures


@dataclass
class LanguageResult:
    """Represents an inferred programming language."""

    language: str
    confidence: float
    indicators: List[str]


@dataclass
class LanguageInference:
    """Results of language inference."""

    primary_language: LanguageResult
    alternative_languages: List[LanguageResult]


class LanguageInferrer:
    """Infers programming language used to create executable files."""

    def __init__(self):
        """Initialize language inferrer with compiler signature database."""
        config = load_compiler_signatures()
        self.compiler_configs = config.get("compilers", [])

    def infer_language(self, pe: pefile.PE, strings: List[str]) -> LanguageInference:
        """Infer the programming language used to create an executable.

        Args:
            pe: Parsed PE file object
            strings: List of extracted strings from the executable

        Returns:
            LanguageInference object with primary and alternative languages
        """
        # Check for .NET languages first (requires CLR header)
        has_clr = self._has_clr_header(pe)

        # Collect all language candidates
        language_candidates: List[LanguageResult] = []

        for compiler_config in self.compiler_configs:
            language_name = compiler_config["language"]
            signatures = compiler_config.get("signatures", [])
            clr_required = compiler_config.get("clr_required", False)

            # Skip if CLR is required but not present
            if clr_required and not has_clr:
                continue

            # Skip if CLR is not required but is present (for .NET languages)
            if not clr_required and has_clr and language_name in ["C#", "VB.NET"]:
                continue

            # Check for signature matches
            matched_indicators = []
            for string in strings:
                for signature in signatures:
                    if signature.lower() in string.lower():
                        matched_indicators.append(string)
                        break

            # If signatures matched, add as candidate
            if matched_indicators:
                confidence = self._calculate_confidence(
                    matched_indicators, signatures, has_clr and clr_required
                )
                language_candidates.append(
                    LanguageResult(
                        language=language_name,
                        confidence=confidence,
                        indicators=matched_indicators,
                    )
                )

        # If no candidates found, return unknown
        if not language_candidates:
            return LanguageInference(
                primary_language=LanguageResult(
                    language="Unknown", confidence=0.0, indicators=[]
                ),
                alternative_languages=[],
            )

        # Sort by confidence (highest first)
        language_candidates.sort(key=lambda x: x.confidence, reverse=True)

        # Primary language is the one with highest confidence
        primary = language_candidates[0]

        # Alternative languages are others with confidence > 0.3
        alternatives = [
            lang for lang in language_candidates[1:] if lang.confidence > 0.3
        ]

        return LanguageInference(
            primary_language=primary, alternative_languages=alternatives
        )

    def _has_clr_header(self, pe: pefile.PE) -> bool:
        """Check if PE file has a CLR (.NET) header.

        Args:
            pe: Parsed PE file object

        Returns:
            True if CLR header is present, False otherwise
        """
        try:
            pe.parse_data_directories(
                directories=[
                    pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_COM_DESCRIPTOR"]
                ]
            )
            return hasattr(pe, "DIRECTORY_ENTRY_COM_DESCRIPTOR")
        except Exception:
            return False

    def _calculate_confidence(
        self, matched_indicators: List[str], all_signatures: List[str], has_clr: bool
    ) -> float:
        """Calculate confidence score for language inference.

        Args:
            matched_indicators: List of matched signature strings
            all_signatures: List of all possible signatures for the language
            has_clr: Whether the executable has a CLR header

        Returns:
            Confidence score between 0.0 and 1.0
        """
        # Base confidence from signature match ratio
        signature_ratio = len(matched_indicators) / len(all_signatures)

        # CLR header provides high confidence for .NET languages
        if has_clr:
            # .NET languages get boosted confidence
            base_confidence = 0.7 + (signature_ratio * 0.3)
        else:
            # Non-.NET languages use signature ratio
            base_confidence = signature_ratio

        # Ensure confidence is between 0.0 and 1.0
        return min(1.0, max(0.0, base_confidence))
