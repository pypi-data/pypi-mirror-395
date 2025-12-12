"""Unit tests for framework detector."""

from exe_analyzer_mcp.framework_detector import FrameworkDetector


class MockPE:
    """Mock PE object for testing."""

    def __init__(self, has_clr=False):
        self.has_clr = has_clr
        if has_clr:
            self.DIRECTORY_ENTRY_COM_DESCRIPTOR = True

    def parse_data_directories(self, directories):
        """Mock parse_data_directories method."""
        return None


def test_dotnet_framework_detection_with_clr_header():
    """Test .NET framework detection with CLR header present.

    Requirements: 1.2
    """
    detector = FrameworkDetector()

    # Create mock PE with CLR header
    mock_pe = MockPE(has_clr=True)

    # Provide .NET Framework strings
    strings = [
        "mscoree.dll",
        "mscorlib.dll",
        "System.Runtime",
        "v4.0.30319",
    ]

    frameworks = detector.detect_frameworks(mock_pe, strings)

    # Should detect .NET Framework
    assert len(frameworks) >= 1
    dotnet_frameworks = [f for f in frameworks if ".NET" in f.name]
    assert len(dotnet_frameworks) == 1

    dotnet = dotnet_frameworks[0]
    assert dotnet.name in [".NET Framework", ".NET Core"]
    assert dotnet.confidence == 1.0  # CLR header is definitive
    assert len(dotnet.indicators) > 0


def test_dotnet_core_detection():
    """Test .NET Core detection with specific indicators.

    Requirements: 1.2
    """
    detector = FrameworkDetector()

    # Create mock PE with CLR header
    mock_pe = MockPE(has_clr=True)

    # Provide .NET Core specific strings
    strings = [
        "System.Private.CoreLib",
        "coreclr.dll",
        "hostfxr.dll",
        "Microsoft.NETCore.App",
    ]

    frameworks = detector.detect_frameworks(mock_pe, strings)

    # Should detect .NET Core
    dotnet_frameworks = [f for f in frameworks if ".NET" in f.name]
    assert len(dotnet_frameworks) == 1

    dotnet = dotnet_frameworks[0]
    assert dotnet.name == ".NET Core"
    assert dotnet.confidence == 1.0


def test_qt_framework_detection():
    """Test Qt framework detection with signature strings.

    Requirements: 1.2
    """
    detector = FrameworkDetector()
    mock_pe = MockPE(has_clr=False)

    # Provide Qt signature strings
    strings = [
        "Qt5Core.dll",
        "QApplication",
        "QWidget",
        "Qt 5.15.2",
    ]

    frameworks = detector.detect_frameworks(mock_pe, strings)

    # Should detect Qt
    qt_frameworks = [f for f in frameworks if f.name == "Qt"]
    assert len(qt_frameworks) == 1

    qt = qt_frameworks[0]
    assert qt.name == "Qt"
    assert qt.version is not None  # Should extract version
    assert qt.confidence > 0.0
    assert len(qt.indicators) > 0


def test_electron_framework_detection():
    """Test Electron framework detection.

    Requirements: 1.2
    """
    detector = FrameworkDetector()
    mock_pe = MockPE(has_clr=False)

    # Provide Electron signature strings
    strings = [
        "electron.exe",
        "chrome_elf.dll",
        "node.dll",
        "Electron Framework",
    ]

    frameworks = detector.detect_frameworks(mock_pe, strings)

    # Should detect Electron
    electron_frameworks = [f for f in frameworks if f.name == "Electron"]
    assert len(electron_frameworks) == 1

    electron = electron_frameworks[0]
    assert electron.name == "Electron"
    assert electron.confidence > 0.0


def test_wxwidgets_framework_detection():
    """Test wxWidgets framework detection.

    Requirements: 1.2
    """
    detector = FrameworkDetector()
    mock_pe = MockPE(has_clr=False)

    strings = ["wxWidgets 3.1", "wxMSW", "wxbase"]

    frameworks = detector.detect_frameworks(mock_pe, strings)

    wx_frameworks = [f for f in frameworks if f.name == "wxWidgets"]
    assert len(wx_frameworks) == 1

    wx = wx_frameworks[0]
    assert wx.name == "wxWidgets"
    assert wx.confidence > 0.0


def test_mfc_framework_detection():
    """Test MFC framework detection.

    Requirements: 1.2
    """
    detector = FrameworkDetector()
    mock_pe = MockPE(has_clr=False)

    strings = ["MFC140.DLL", "Microsoft Foundation Classes"]

    frameworks = detector.detect_frameworks(mock_pe, strings)

    mfc_frameworks = [f for f in frameworks if f.name == "MFC"]
    assert len(mfc_frameworks) == 1

    mfc = mfc_frameworks[0]
    assert mfc.name == "MFC"
    assert mfc.confidence > 0.0


def test_gtk_framework_detection():
    """Test GTK framework detection.

    Requirements: 1.2
    """
    detector = FrameworkDetector()
    mock_pe = MockPE(has_clr=False)

    strings = ["gtk-3.dll", "libgtk-3", "glib-2.0"]

    frameworks = detector.detect_frameworks(mock_pe, strings)

    gtk_frameworks = [f for f in frameworks if f.name == "GTK"]
    assert len(gtk_frameworks) == 1

    gtk = gtk_frameworks[0]
    assert gtk.name == "GTK"
    assert gtk.confidence > 0.0


def test_empty_result_when_no_frameworks_present():
    """Test that empty result is returned when no frameworks are detected.

    Requirements: 1.5
    """
    detector = FrameworkDetector()
    mock_pe = MockPE(has_clr=False)

    # Provide strings with no framework signatures
    strings = [
        "Hello World",
        "Some random text",
        "C:\\Windows\\System32\\kernel32.dll",
    ]

    frameworks = detector.detect_frameworks(mock_pe, strings)

    # Should return empty list
    assert frameworks == []


def test_multiple_frameworks_detected():
    """Test detection of multiple frameworks in same executable.

    Requirements: 1.4
    """
    detector = FrameworkDetector()
    mock_pe = MockPE(has_clr=False)

    # Provide signatures for multiple frameworks
    strings = [
        "Qt5Core.dll",
        "QApplication",
        "MFC140.DLL",
        "Microsoft Foundation Classes",
        "gtk-3.dll",
    ]

    frameworks = detector.detect_frameworks(mock_pe, strings)

    # Should detect multiple frameworks
    assert len(frameworks) >= 2

    framework_names = {f.name for f in frameworks}
    assert "Qt" in framework_names
    assert "MFC" in framework_names or "GTK" in framework_names
