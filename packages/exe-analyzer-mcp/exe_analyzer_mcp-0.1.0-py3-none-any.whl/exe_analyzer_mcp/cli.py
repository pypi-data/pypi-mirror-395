"""Command-line interface for exe-analyzer-mcp testing."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

from exe_analyzer_mcp.analysis_orchestrator import (
    AnalysisOrchestrator,
    FrameworkAnalysisResult,
    LanguageAnalysisResult,
    LibraryAnalysisResult,
    StringAnalysisResult,
)


class Colors:
    """ANSI color codes for terminal output."""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class CLIFormatter:
    """Formats analysis results for CLI output."""

    def __init__(self, use_colors: bool = True, verbose: bool = False):
        """Initialize formatter.

        Args:
            use_colors: Whether to use ANSI colors in output
            verbose: Whether to include verbose debugging information
        """
        self.use_colors = use_colors
        self.verbose = verbose

    def _colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled.

        Args:
            text: Text to colorize
            color: Color code to apply

        Returns:
            Colorized text or plain text if colors disabled
        """
        if self.use_colors:
            return f"{color}{text}{Colors.ENDC}"
        return text

    def format_frameworks(self, result: FrameworkAnalysisResult) -> str:
        """Format framework analysis results.

        Args:
            result: Framework analysis result

        Returns:
            Formatted string output
        """
        output = []
        output.append(self._colorize("=" * 60, Colors.HEADER))
        output.append(self._colorize("FRAMEWORK ANALYSIS", Colors.HEADER))
        output.append(self._colorize("=" * 60, Colors.HEADER))

        if result.error:
            output.append(self._colorize(f"\n✗ Error: {result.error.message}", Colors.FAIL))
            output.append(self._colorize(f"  Type: {result.error.error_type}", Colors.FAIL))
            output.append(self._colorize(f"  Phase: {result.error.phase}", Colors.FAIL))
            if self.verbose and result.error.partial_results:
                output.append("\nPartial Results:")
                output.append(json.dumps(result.error.partial_results, indent=2))
        else:
            if not result.frameworks:
                output.append(self._colorize("\n✓ No frameworks detected", Colors.WARNING))
            else:
                output.append(
                    self._colorize(
                        f"\n✓ Found {len(result.frameworks)} framework(s)",
                        Colors.OKGREEN,
                    )
                )
                for i, framework in enumerate(result.frameworks, 1):
                    output.append(f"\n{self._colorize(f'Framework {i}:', Colors.BOLD)}")
                    output.append(f"  Name: {framework.name}")
                    if framework.version:
                        output.append(f"  Version: {framework.version}")
                    output.append(f"  Confidence: {framework.confidence:.2f}")
                    if self.verbose and framework.indicators:
                        output.append("  Indicators:")
                        for indicator in framework.indicators[:5]:
                            output.append(f"    - {indicator}")
                        if len(framework.indicators) > 5:
                            remaining = len(framework.indicators) - 5
                            output.append(f"    ... and {remaining} more")

        return "\n".join(output)

    def format_libraries(self, result: LibraryAnalysisResult) -> str:
        """Format library analysis results.

        Args:
            result: Library analysis result

        Returns:
            Formatted string output
        """
        output = []
        output.append(self._colorize("=" * 60, Colors.HEADER))
        output.append(self._colorize("LIBRARY ANALYSIS", Colors.HEADER))
        output.append(self._colorize("=" * 60, Colors.HEADER))

        if result.error:
            output.append(self._colorize(f"\n✗ Error: {result.error.message}", Colors.FAIL))
            output.append(self._colorize(f"  Type: {result.error.error_type}", Colors.FAIL))
            output.append(self._colorize(f"  Phase: {result.error.phase}", Colors.FAIL))
        else:
            analysis = result.analysis
            output.append(
                self._colorize(f"\n✓ Total Imports: {analysis.total_imports}", Colors.OKGREEN)
            )

            # System libraries
            output.append(
                f"\n{self._colorize('System Libraries:', Colors.BOLD)} "
                f"({len(analysis.system_libraries)})"
            )
            for lib in analysis.system_libraries[:10]:
                output.append(f"  • {lib.name}")
                if self.verbose and lib.functions:
                    for func in lib.functions[:3]:
                        output.append(f"      - {func}")
                    if len(lib.functions) > 3:
                        output.append(f"      ... and {len(lib.functions) - 3} more")
            if len(analysis.system_libraries) > 10:
                remaining = len(analysis.system_libraries) - 10
                output.append(f"  ... and {remaining} more")

            # External libraries
            output.append(
                f"\n{self._colorize('External Libraries:', Colors.BOLD)} "
                f"({len(analysis.external_libraries)})"
            )
            if not analysis.external_libraries:
                output.append("  (none)")
            else:
                for lib in analysis.external_libraries[:10]:
                    output.append(f"  • {lib.name}")
                    if self.verbose and lib.functions:
                        for func in lib.functions[:3]:
                            output.append(f"      - {func}")
                        if len(lib.functions) > 3:
                            output.append(f"      ... and {len(lib.functions) - 3} more")
                if len(analysis.external_libraries) > 10:
                    remaining = len(analysis.external_libraries) - 10
                    output.append(f"  ... and {remaining} more")

        return "\n".join(output)

    def format_strings(self, result: StringAnalysisResult) -> str:
        """Format string extraction results.

        Args:
            result: String extraction result

        Returns:
            Formatted string output
        """
        output = []
        output.append(self._colorize("=" * 60, Colors.HEADER))
        output.append(self._colorize("STRING EXTRACTION", Colors.HEADER))
        output.append(self._colorize("=" * 60, Colors.HEADER))

        if result.error:
            output.append(self._colorize(f"\n✗ Error: {result.error.message}", Colors.FAIL))
            output.append(self._colorize(f"  Type: {result.error.error_type}", Colors.FAIL))
            output.append(self._colorize(f"  Phase: {result.error.phase}", Colors.FAIL))
        else:
            strings = result.strings
            output.append(
                self._colorize(f"\n✓ Total Strings: {strings.total_count}", Colors.OKGREEN)
            )
            if strings.truncated:
                output.append(
                    self._colorize("  (Results truncated to 10,000 entries)", Colors.WARNING)
                )

            for category, strings_list in strings.strings_by_category.items():
                if not strings_list:
                    continue

                category_name = category.value if hasattr(category, "value") else str(category)
                output.append(
                    f"\n{self._colorize(f'{category_name}:', Colors.BOLD)} ({len(strings_list)})"
                )

                # Show first few strings from each category
                display_count = 5 if not self.verbose else 10
                for string in strings_list[:display_count]:
                    # Truncate long strings
                    value = string.value
                    if len(value) > 80:
                        value = value[:77] + "..."
                    output.append(f"  • {value}")
                    if self.verbose:
                        output.append(
                            f"      Offset: 0x{string.offset:08x}, "
                            f"Encoding: {string.encoding}, "
                            f"Entropy: {string.entropy:.2f}"
                        )

                if len(strings_list) > display_count:
                    remaining = len(strings_list) - display_count
                    output.append(f"  ... and {remaining} more")

        return "\n".join(output)

    def format_language(self, result: LanguageAnalysisResult) -> str:
        """Format language inference results.

        Args:
            result: Language inference result

        Returns:
            Formatted string output
        """
        output = []
        output.append(self._colorize("=" * 60, Colors.HEADER))
        output.append(self._colorize("LANGUAGE INFERENCE", Colors.HEADER))
        output.append(self._colorize("=" * 60, Colors.HEADER))

        if result.error:
            output.append(self._colorize(f"\n✗ Error: {result.error.message}", Colors.FAIL))
            output.append(self._colorize(f"  Type: {result.error.error_type}", Colors.FAIL))
            output.append(self._colorize(f"  Phase: {result.error.phase}", Colors.FAIL))
        else:
            inference = result.inference
            output.append(
                self._colorize(
                    f"\n✓ Primary Language: {inference.primary_language.language}",
                    Colors.OKGREEN,
                )
            )
            output.append(f"  Confidence: {inference.primary_language.confidence:.2f}")
            if self.verbose and inference.primary_language.indicators:
                output.append("  Indicators:")
                for indicator in inference.primary_language.indicators[:5]:
                    output.append(f"    - {indicator}")
                if len(inference.primary_language.indicators) > 5:
                    remaining = len(inference.primary_language.indicators) - 5
                    output.append(f"    ... and {remaining} more")

            if inference.alternative_languages:
                output.append(f"\n{self._colorize('Alternative Languages:', Colors.BOLD)}")
                for alt in inference.alternative_languages:
                    output.append(f"  • {alt.language} (confidence: {alt.confidence:.2f})")
                    if self.verbose and alt.indicators:
                        for indicator in alt.indicators[:3]:
                            output.append(f"      - {indicator}")

        return "\n".join(output)

    def format_json(self, data: Dict[str, Any]) -> str:
        """Format data as JSON.

        Args:
            data: Data to format

        Returns:
            JSON formatted string
        """
        return json.dumps(data, indent=2, default=str)


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser.

    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        prog="exe-analyzer",
        description="Analyze Windows executable files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze frameworks
  exe-analyzer frameworks notepad.exe

  # Analyze libraries with verbose output
  exe-analyzer libraries --verbose calc.exe

  # Extract strings in JSON format
  exe-analyzer strings --json cmd.exe

  # Infer language without colors
  exe-analyzer language --no-color python.exe

  # Run all analyses
  exe-analyzer all explorer.exe
        """,
    )

    parser.add_argument(
        "command",
        choices=["frameworks", "libraries", "strings", "language", "all"],
        help="Analysis type to perform",
    )

    parser.add_argument(
        "file_path",
        help="Path to the executable file to analyze",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output with additional details",
    )

    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="Output results in JSON format",
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )

    return parser


def main() -> int:
    """Main CLI entry point.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = create_parser()
    args = parser.parse_args()

    # Validate file exists
    file_path = Path(args.file_path)
    if not file_path.exists():
        print(f"Error: File not found: {args.file_path}", file=sys.stderr)
        return 1

    # Initialize orchestrator and formatter
    orchestrator = AnalysisOrchestrator()
    use_colors = not args.no_color and sys.stdout.isatty()
    formatter = CLIFormatter(use_colors=use_colors, verbose=args.verbose)

    try:
        if args.command == "frameworks":
            result = orchestrator.analyze_frameworks(str(file_path))
            if args.json:
                from dataclasses import asdict

                data = {
                    "frameworks": [asdict(f) for f in result.frameworks],
                    "error": (asdict(result.error) if result.error else None),
                }
                print(formatter.format_json(data))
            else:
                print(formatter.format_frameworks(result))
            return 1 if result.error else 0

        elif args.command == "libraries":
            result = orchestrator.analyze_libraries(str(file_path))
            if args.json:
                from dataclasses import asdict

                data = {
                    "analysis": (asdict(result.analysis) if result.analysis else None),
                    "error": (asdict(result.error) if result.error else None),
                }
                print(formatter.format_json(data))
            else:
                print(formatter.format_libraries(result))
            return 1 if result.error else 0

        elif args.command == "strings":
            result = orchestrator.extract_strings(str(file_path))
            if args.json:
                from dataclasses import asdict

                if result.strings:
                    # Convert enum keys to strings for JSON
                    strings_by_category = {}
                    for cat, strs in result.strings.strings_by_category.items():
                        cat_key = cat.value if hasattr(cat, "value") else str(cat)
                        strings_by_category[cat_key] = [asdict(s) for s in strs]
                    data = {
                        "strings": {
                            "strings_by_category": strings_by_category,
                            "total_count": result.strings.total_count,
                            "truncated": result.strings.truncated,
                        },
                        "error": (asdict(result.error) if result.error else None),
                    }
                else:
                    data = {
                        "strings": None,
                        "error": (asdict(result.error) if result.error else None),
                    }
                print(formatter.format_json(data))
            else:
                print(formatter.format_strings(result))
            return 1 if result.error else 0

        elif args.command == "language":
            result = orchestrator.infer_language(str(file_path))
            if args.json:
                from dataclasses import asdict

                data = {
                    "inference": (asdict(result.inference) if result.inference else None),
                    "error": (asdict(result.error) if result.error else None),
                }
                print(formatter.format_json(data))
            else:
                print(formatter.format_language(result))
            return 1 if result.error else 0

        elif args.command == "all":
            # Run all analyses
            print(formatter._colorize("\n" + "=" * 60 + "\n", Colors.HEADER))
            print(formatter._colorize(f"ANALYZING: {file_path.name}", Colors.HEADER))
            print(formatter._colorize("=" * 60 + "\n", Colors.HEADER))

            has_error = False

            # Frameworks
            result = orchestrator.analyze_frameworks(str(file_path))
            print(formatter.format_frameworks(result))
            print()
            if result.error:
                has_error = True

            # Libraries
            result = orchestrator.analyze_libraries(str(file_path))
            print(formatter.format_libraries(result))
            print()
            if result.error:
                has_error = True

            # Strings
            result = orchestrator.extract_strings(str(file_path))
            print(formatter.format_strings(result))
            print()
            if result.error:
                has_error = True

            # Language
            result = orchestrator.infer_language(str(file_path))
            print(formatter.format_language(result))
            print()
            if result.error:
                has_error = True

            return 1 if has_error else 0

    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"\nUnexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
