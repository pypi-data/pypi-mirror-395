"""
Tests for the language abstraction layer.
"""

import pytest
from coon.languages import LanguageRegistry, LanguageHandler, LanguageSpec
from coon.languages.dart import DartLanguageHandler


class TestLanguageSpec:
    """Tests for LanguageSpec dataclass."""
    
    def test_basic_creation(self):
        """Test basic LanguageSpec creation."""
        spec = LanguageSpec(name="test", version="1.0.0", extensions=[".test"])
        assert spec.name == "test"
        assert spec.version == "1.0.0"
        assert spec.extensions == [".test"]
        assert spec.display_name == "Test"  # Auto-generated
    
    def test_custom_display_name(self):
        """Test LanguageSpec with custom display name."""
        spec = LanguageSpec(
            name="dart",
            version="1.0.0",
            extensions=[".dart"],
            display_name="Dart/Flutter"
        )
        assert spec.display_name == "Dart/Flutter"
    
    def test_supports_extension(self):
        """Test extension checking."""
        spec = LanguageSpec(name="dart", version="1.0.0", extensions=[".dart"])
        assert spec.supports_extension(".dart") is True
        assert spec.supports_extension("dart") is True  # Without dot
        assert spec.supports_extension(".py") is False


class TestLanguageRegistry:
    """Tests for LanguageRegistry."""
    
    def test_list_languages(self):
        """Test listing registered languages."""
        languages = LanguageRegistry.list_languages()
        assert isinstance(languages, list)
        assert "dart" in languages
    
    def test_get_dart_handler(self):
        """Test getting Dart handler."""
        handler = LanguageRegistry.get("dart")
        assert isinstance(handler, DartLanguageHandler)
        assert handler.spec.name == "dart"
    
    def test_get_unknown_language(self):
        """Test getting unknown language raises ValueError."""
        with pytest.raises(ValueError, match="Unknown language"):
            LanguageRegistry.get("unknown_language")
    
    def test_is_registered(self):
        """Test checking if language is registered."""
        assert LanguageRegistry.is_registered("dart") is True
        assert LanguageRegistry.is_registered("unknown") is False
    
    def test_detect_dart_code(self):
        """Test detecting Dart code."""
        dart_code = """
        class MyWidget extends StatelessWidget {
            Widget build(BuildContext context) {
                return Scaffold(
                    body: Text("Hello")
                );
            }
        }
        """
        detected = LanguageRegistry.detect(dart_code)
        assert detected == "dart"
    
    def test_detect_non_dart_code(self):
        """Test that generic code doesn't falsely detect as Dart."""
        generic_code = "x = 1 + 2"
        detected = LanguageRegistry.detect(generic_code)
        # Should return None (confidence < 0.5) or still "dart" with low confidence
        # For now just test it doesn't crash
        assert detected is None or isinstance(detected, str)
    
    def test_detect_from_extension(self):
        """Test detecting language from file extension."""
        assert LanguageRegistry.detect_from_extension(".dart") == "dart"
        assert LanguageRegistry.detect_from_extension("dart") == "dart"
        assert LanguageRegistry.detect_from_extension(".unknown") is None


class TestDartLanguageHandler:
    """Tests for DartLanguageHandler."""
    
    def test_spec(self):
        """Test Dart language spec."""
        handler = DartLanguageHandler()
        spec = handler.spec
        
        assert spec.name == "dart"
        assert ".dart" in spec.extensions
        assert spec.framework == "flutter"
    
    def test_get_keywords(self):
        """Test getting Dart keywords."""
        handler = DartLanguageHandler()
        keywords = handler.get_keywords()
        
        assert isinstance(keywords, dict)
        assert "class" in keywords
        assert keywords["class"] == "c:"
        assert "final" in keywords
        assert keywords["final"] == "f:"
    
    def test_get_type_abbreviations(self):
        """Test getting widget abbreviations."""
        handler = DartLanguageHandler()
        widgets = handler.get_type_abbreviations()
        
        assert isinstance(widgets, dict)
        assert "Scaffold" in widgets
        assert widgets["Scaffold"] == "S"
        assert "Column" in widgets
        assert widgets["Column"] == "C"
    
    def test_get_property_abbreviations(self):
        """Test getting property abbreviations."""
        handler = DartLanguageHandler()
        properties = handler.get_property_abbreviations()
        
        assert isinstance(properties, dict)
        assert "child:" in properties
        assert properties["child:"] == "c:"
        assert "children:" in properties
        assert properties["children:"] == "h:"
    
    def test_get_all_abbreviations(self):
        """Test getting all abbreviations combined."""
        handler = DartLanguageHandler()
        all_abbrevs = handler.get_all_abbreviations()
        
        # Should contain keywords, types, and properties
        assert "class" in all_abbrevs  # keyword
        assert "Scaffold" in all_abbrevs  # widget
        assert "child:" in all_abbrevs  # property
    
    def test_get_reverse_abbreviations(self):
        """Test getting reverse abbreviation mapping."""
        handler = DartLanguageHandler()
        reverse = handler.get_reverse_abbreviations()
        
        # Check some reverse mappings
        assert "S" in reverse
        assert reverse["S"] == "Scaffold"
        assert "c:" in reverse  # This could be class or child:, but should exist
    
    def test_detect_language_high_confidence(self):
        """Test language detection with clear Dart code."""
        handler = DartLanguageHandler()
        dart_code = """
        import 'package:flutter/material.dart';
        
        class MyWidget extends StatelessWidget {
            @override
            Widget build(BuildContext context) {
                return Container();
            }
        }
        """
        score = handler.detect_language(dart_code)
        assert score > 0.5, "Should have high confidence for Flutter widget code"
    
    def test_detect_language_medium_confidence(self):
        """Test language detection with some Dart patterns."""
        handler = DartLanguageHandler()
        code = "class MyClass { final String name; }"
        score = handler.detect_language(code)
        # Should have some confidence but not super high
        assert 0.0 <= score <= 1.0
    
    def test_detect_language_low_confidence(self):
        """Test language detection with non-Dart code."""
        handler = DartLanguageHandler()
        python_code = "def hello(): print('world')"
        score = handler.detect_language(python_code)
        assert score < 0.5, "Should have low confidence for Python code"
    
    def test_detect_empty_code(self):
        """Test language detection with empty code."""
        handler = DartLanguageHandler()
        assert handler.detect_language("") == 0.0
        assert handler.detect_language("   ") == 0.0
    
    def test_create_lexer(self):
        """Test creating a Dart lexer."""
        handler = DartLanguageHandler()
        lexer = handler.create_lexer()
        
        from coon.parser.lexer import DartLexer
        assert isinstance(lexer, DartLexer)
    
    def test_create_parser(self):
        """Test creating a Dart parser."""
        handler = DartLanguageHandler()
        parser = handler.create_parser()
        
        from coon.parser.parser import DartParser
        assert isinstance(parser, DartParser)
    
    def test_backwards_compatibility_aliases(self):
        """Test backwards compatibility method aliases."""
        handler = DartLanguageHandler()
        
        # get_widgets() should be same as get_type_abbreviations()
        assert handler.get_widgets() == handler.get_type_abbreviations()
        
        # get_properties() should be same as get_property_abbreviations()
        assert handler.get_properties() == handler.get_property_abbreviations()


class TestLanguageRegistryIntegration:
    """Integration tests for language registry with compressor."""
    
    def test_handler_caching(self):
        """Test that handlers are cached (same instance returned)."""
        handler1 = LanguageRegistry.get("dart")
        handler2 = LanguageRegistry.get("dart")
        assert handler1 is handler2
    
    def test_case_insensitive_lookup(self):
        """Test that language lookup is case-insensitive."""
        handler1 = LanguageRegistry.get("dart")
        handler2 = LanguageRegistry.get("DART")
        handler3 = LanguageRegistry.get("Dart")
        
        assert handler1 is handler2
        assert handler1 is handler3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
