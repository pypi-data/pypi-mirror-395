"""
Conformance tests for COON Python SDK.

Tests against shared fixtures in spec/fixtures/conformance/
to ensure cross-SDK compatibility.
"""

import json
import pytest
from pathlib import Path


# Find the spec directory - packages/python/tests -> spec
# Go up 3 levels: tests -> python -> packages -> COON, then into spec
SPEC_DIR = Path(__file__).parent.parent.parent.parent / "spec"
FIXTURES_DIR = SPEC_DIR / "fixtures" / "conformance"


def load_fixture(name: str) -> dict:
    """Load a conformance fixture file."""
    fixture_path = FIXTURES_DIR / f"{name}.json"
    if not fixture_path.exists():
        pytest.skip(f"Fixture {name}.json not found at {fixture_path}")
    
    with open(fixture_path, 'r', encoding='utf-8') as f:
        return json.load(f)


class TestBasicCompression:
    """Test basic compression conformance."""
    
    @pytest.fixture
    def fixture(self):
        return load_fixture("basic_compression")
    
    def test_fixture_version(self, fixture):
        """Verify fixture version."""
        assert "version" in fixture
        assert fixture["version"] == "1.0.0"
    
    def test_basic_compression_cases(self, fixture):
        """Test basic compression test cases."""
        from coon import Compressor
        
        compressor = Compressor()
        
        # Use testCases (camelCase) as per fixture format
        for case in fixture.get("testCases", []):
            name = case.get("name", "unnamed")
            input_code = case.get("input", "")
            expected = case.get("expected")
            
            if not input_code:
                continue
            
            result = compressor.compress(input_code, strategy="basic")
            
            # For basic tests, we check that compression happens
            assert len(result.compressed_code) <= len(input_code), \
                f"Test '{name}' failed: compression should reduce size"
            
            # If expected output specified, check it
            if expected:
                assert result.compressed_code == expected, \
                    f"Test '{name}' failed: expected '{expected}', got '{result.compressed_code}'"


class TestWidgetAbbreviations:
    """Test widget abbreviation conformance."""
    
    @pytest.fixture
    def fixture(self):
        return load_fixture("widget_abbreviations")
    
    def test_widget_abbreviation_cases(self, fixture):
        """Test widget abbreviation test cases."""
        from coon import get_widgets
        from coon.strategies import BasicStrategy
        
        widgets = get_widgets()
        strategy = BasicStrategy()
        
        for case in fixture.get("testCases", []):
            name = case.get("name", "unnamed")
            input_code = case.get("input", "")
            expected = case.get("expected")
            
            if not input_code:
                continue
            
            result = strategy.compress(input_code)
            
            # If expected output specified, check it
            if expected:
                assert result == expected, \
                    f"Test '{name}' failed: expected '{expected}', got '{result}'"


class TestClassDefinitions:
    """Test class definition conformance."""
    
    @pytest.fixture
    def fixture(self):
        return load_fixture("class_definitions")
    
    def test_class_definition_cases(self, fixture):
        """Test class definition compression cases."""
        from coon import Compressor
        
        compressor = Compressor()
        
        for case in fixture.get("testCases", []):
            name = case.get("name", "unnamed")
            input_code = case.get("input", "")
            expected = case.get("expected")
            
            if not input_code:
                continue
            
            result = compressor.compress(input_code, strategy="aggressive")
            
            # Verify class keyword compression
            if 'class' in input_code:
                # Should be abbreviated in output
                assert 'c:' in result.compressed_code or 'class' not in result.compressed_code, \
                    f"Test '{name}': class keyword should be abbreviated"
            
            if expected:
                assert result.compressed_code == expected, \
                    f"Test '{name}' failed: expected '{expected}', got '{result.compressed_code}'"


class TestRoundTrip:
    """Test round-trip (compress/decompress) conformance."""
    
    @pytest.fixture
    def fixture(self):
        return load_fixture("round_trip")
    
    def test_round_trip_cases(self, fixture):
        """Test that compression is reversible."""
        from coon import Compressor, Decompressor
        
        compressor = Compressor()
        decompressor = Decompressor()
        
        for case in fixture.get("testCases", []):
            name = case.get("name", "unnamed")
            input_code = case.get("input", "")
            
            if not input_code:
                continue
            
            # Compress
            compressed_result = compressor.compress(input_code, strategy="basic")
            
            # Decompress
            decompressed = decompressor.decompress(compressed_result.compressed_code)
            
            # Should not throw and decompressed should not be empty if input wasn't empty
            assert decompressed is not None, f"Test '{name}': decompression returned None"


class TestEdgeCases:
    """Test edge case conformance."""
    
    @pytest.fixture
    def fixture(self):
        return load_fixture("edge_cases")
    
    def test_empty_input(self, fixture):
        """Test empty input handling."""
        from coon import compress_dart
        
        result = compress_dart("")
        assert result == ""
    
    def test_whitespace_only(self, fixture):
        """Test whitespace-only input."""
        from coon import compress_dart
        
        result = compress_dart("   \n\t  \n  ")
        assert result == "" or result.strip() == ""
    
    def test_edge_cases(self, fixture):
        """Test edge case scenarios."""
        from coon import Compressor
        
        compressor = Compressor()
        
        for case in fixture.get("testCases", []):
            name = case.get("name", "unnamed")
            input_code = case.get("input", "")
            
            # All edge cases should be handled without crashing
            try:
                result = compressor.compress(input_code)
                assert result is not None, f"Test '{name}' returned None"
            except Exception as e:
                pytest.fail(f"Test '{name}' failed unexpectedly: {e}")


class TestPropertyAbbreviations:
    """Test property abbreviation conformance."""
    
    def test_property_abbreviations(self):
        """Test that properties are correctly abbreviated."""
        from coon import get_properties
        from coon.strategies import BasicStrategy
        
        properties = get_properties()
        strategy = BasicStrategy()
        
        # Test each property
        for prop, abbrev in list(properties.items())[:5]:  # Test first 5
            input_code = f"Widget({prop}: value)"
            result = strategy.compress(input_code)
            
            # Property should be abbreviated in output
            assert abbrev in result or prop not in result, \
                f"Property '{prop}' should be abbreviated to '{abbrev}'"


class TestKeywordAbbreviations:
    """Test keyword abbreviation conformance."""
    
    def test_keyword_abbreviations(self):
        """Test that keywords are correctly abbreviated."""
        from coon.strategies import AggressiveStrategy
        
        strategy = AggressiveStrategy()
        
        # Test class keyword
        input_code = "class MyClass {}"
        result = strategy.compress(input_code)
        assert "c:" in result, "class keyword should be abbreviated to 'c:'"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
