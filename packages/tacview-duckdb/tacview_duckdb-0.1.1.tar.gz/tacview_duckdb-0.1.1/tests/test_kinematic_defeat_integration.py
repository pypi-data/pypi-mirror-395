"""Test kinematic defeat detection integration."""

from pathlib import Path
from tacview_duckdb.enrichment import MissedWeaponAnalyzer

try:
    import pytest
    HAS_PYTEST = True
except ImportError:
    HAS_PYTEST = False
    # Mock pytest.raises for manual testing
    class MockRaises:
        def __init__(self, exc_class):
            self.exc_class = exc_class
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is None:
                raise AssertionError(f"Expected {self.exc_class.__name__} to be raised")
            return exc_type == self.exc_class
    
    class pytest:
        @staticmethod
        def raises(exc_class):
            return MockRaises(exc_class)


def test_kinematic_defeat_detector_integrated():
    """Verify KinematicDefeatDetector is integrated into MissedWeaponAnalyzer."""
    # Create analyzer with default settings
    analyzer = MissedWeaponAnalyzer()
    
    # Verify defeat detection is enabled by default
    assert analyzer.detect_kinematic_defeats is True
    
    # Verify defeat detection parameters are present
    assert hasattr(analyzer, 'defeat_analysis_window')
    assert hasattr(analyzer, 'min_opening_closure')
    assert hasattr(analyzer, 'peak_opening_closure')
    assert hasattr(analyzer, 'max_pointing_error')
    assert hasattr(analyzer, 'min_high_g_states')
    assert hasattr(analyzer, 'min_high_g_threshold')
    assert hasattr(analyzer, 'max_g_variance')
    assert hasattr(analyzer, 'min_effective_speed')
    assert hasattr(analyzer, 'min_speed_loss')
    
    # Verify method is present
    assert hasattr(analyzer, '_detect_kinematic_defeats')
    assert callable(analyzer._detect_kinematic_defeats)
    
    print("✓ KinematicDefeatDetector successfully integrated into MissedWeaponAnalyzer")


def test_kinematic_defeat_can_be_disabled():
    """Verify defeat detection can be disabled."""
    analyzer = MissedWeaponAnalyzer(detect_kinematic_defeats=False)
    
    assert analyzer.detect_kinematic_defeats is False
    
    print("✓ Kinematic defeat detection can be disabled")


def test_kinematic_defeat_custom_parameters():
    """Verify custom defeat detection parameters work."""
    analyzer = MissedWeaponAnalyzer(
        detect_kinematic_defeats=True,
        defeat_analysis_window=3.0,
        min_opening_closure=-40.0,
        peak_opening_closure=-60.0,
        max_pointing_error=15.0,
        min_high_g_states=5,
        min_high_g_threshold=12.0,
        max_g_variance=3.0,
        min_effective_speed=200.0,
        min_speed_loss=150.0
    )
    
    assert analyzer.defeat_analysis_window == 3.0
    assert analyzer.min_opening_closure == -40.0
    assert analyzer.peak_opening_closure == -60.0
    assert analyzer.max_pointing_error == 15.0
    assert analyzer.min_high_g_states == 5
    assert analyzer.min_high_g_threshold == 12.0
    assert analyzer.max_g_variance == 3.0
    assert analyzer.min_effective_speed == 200.0
    assert analyzer.min_speed_loss == 150.0
    
    print("✓ Custom kinematic defeat parameters work correctly")


def test_no_separate_kinematic_defeat_class():
    """Verify KinematicDefeatDetector class no longer exists as separate entity."""
    # Should not be able to import it
    with pytest.raises(ImportError):
        from tacview_duckdb.enrichment import KinematicDefeatDetector
    
    print("✓ Separate KinematicDefeatDetector class correctly removed")


if __name__ == "__main__":
    # Run tests manually
    test_kinematic_defeat_detector_integrated()
    test_kinematic_defeat_can_be_disabled()
    test_kinematic_defeat_custom_parameters()
    test_no_separate_kinematic_defeat_class()
    
    print("\n" + "=" * 60)
    print("All integration tests passed!")
    print("=" * 60)

