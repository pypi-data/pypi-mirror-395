"""Property-based tests for framework detector."""

from hypothesis import given, settings
from hypothesis import strategies as st

from exe_analyzer_mcp.framework_detector import Framework, FrameworkDetector


# Custom strategies for generating test data
@st.composite
def framework_strings(draw):
    """Generate strings that contain framework signatures."""
    framework_signatures = {
        "Qt": ["Qt5Core.dll", "QApplication", "Qt6Core", "libQt5"],
        "Electron": ["electron.exe", "chrome_elf.dll", "node.dll"],
        "wxWidgets": ["wxWidgets 3.1", "wxMSW", "wxbase"],
        "MFC": ["MFC140.DLL", "Microsoft Foundation Classes"],
        "GTK": ["gtk-3.dll", "libgtk-3", "glib-2.0"],
    }

    framework = draw(st.sampled_from(list(framework_signatures.keys())))
    signature = draw(st.sampled_from(framework_signatures[framework]))

    # Generate a list of strings that includes the signature
    num_strings = draw(st.integers(min_value=1, max_value=20))
    strings = [signature]

    for _ in range(num_strings - 1):
        strings.append(draw(st.text(min_size=4, max_size=50)))

    return strings


@st.composite
def dotnet_pe_mock(draw):
    """Generate a mock PE object that appears to be .NET."""

    # This is a simplified mock - in real tests we'd use actual PE files
    class MockPE:
        def __init__(self, has_clr):
            self.has_clr = has_clr
            if has_clr:
                self.DIRECTORY_ENTRY_COM_DESCRIPTOR = True

        def parse_data_directories(self, directories):
            pass

    has_clr = draw(st.booleans())
    return MockPE(has_clr)


# Feature: exe-analyzer-mcp, Property 2: Framework detection returns
# structured results
@settings(max_examples=100)
@given(strings=framework_strings())
def test_framework_detection_returns_structured_results(strings):
    """Property: For any executable where frameworks are detected,
    each detected framework should include a name field and optionally
    a version field.

    Validates: Requirements 1.3, 1.4
    """
    detector = FrameworkDetector()

    # Create a minimal mock PE object (we're testing string-based detection)
    class MockPE:
        def parse_data_directories(self, directories):
            pass

    mock_pe = MockPE()

    # Detect frameworks
    frameworks = detector.detect_frameworks(mock_pe, strings)

    # Property: All detected frameworks must have required structure
    for framework in frameworks:
        # Must be a Framework instance
        assert isinstance(framework, Framework)

        # Must have a name field that is a non-empty string
        assert isinstance(framework.name, str)
        assert len(framework.name) > 0

        # Version can be None or a string
        assert framework.version is None or isinstance(framework.version, str)

        # Must have confidence score between 0 and 1
        assert isinstance(framework.confidence, float)
        assert 0.0 <= framework.confidence <= 1.0

        # Must have indicators list
        assert isinstance(framework.indicators, list)
        assert len(framework.indicators) > 0


# Feature: exe-analyzer-mcp, Property 3: Multiple framework detection
# completeness
@settings(max_examples=100)
@given(
    qt_strings=st.lists(
        st.sampled_from(["Qt5Core", "QApplication", "Qt6Core"]),
        min_size=1,
        max_size=3,
    ),
    electron_strings=st.lists(
        st.sampled_from(["electron", "chrome_elf.dll", "node.dll"]),
        min_size=1,
        max_size=3,
    ),
    other_strings=st.lists(st.text(min_size=4, max_size=30), min_size=0, max_size=10),
)
def test_multiple_framework_detection_completeness(
    qt_strings, electron_strings, other_strings
):
    """Property: For any executable containing signatures for multiple
    frameworks, all frameworks with valid signatures should appear in the
    detection result.

    Validates: Requirements 1.4
    """
    detector = FrameworkDetector()

    # Create a minimal mock PE object
    class MockPE:
        def parse_data_directories(self, directories):
            pass

    mock_pe = MockPE()

    # Combine all strings
    all_strings = qt_strings + electron_strings + other_strings

    # Detect frameworks
    frameworks = detector.detect_frameworks(mock_pe, all_strings)

    # Extract framework names
    detected_names = {f.name for f in frameworks}

    # Property: Both Qt and Electron should be detected
    # (since we provided signatures for both)
    assert "Qt" in detected_names, "Qt framework should be detected"
    assert "Electron" in detected_names, "Electron framework should be detected"

    # Property: Each framework should appear only once
    framework_name_counts = {}
    for framework in frameworks:
        framework_name_counts[framework.name] = (
            framework_name_counts.get(framework.name, 0) + 1
        )

    for name, count in framework_name_counts.items():
        assert count == 1, f"Framework {name} should appear exactly once"
