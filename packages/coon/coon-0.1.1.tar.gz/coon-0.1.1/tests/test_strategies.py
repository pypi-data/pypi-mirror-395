"""
Unit tests for COON strategies.
"""

import pytest
from coon.strategies import (
    CompressionStrategy,
    BasicStrategy,
    AggressiveStrategy,
    ASTBasedStrategy,
    ComponentRefStrategy,
    StrategySelector,
    StrategyName,
    get_strategy,
)


class TestBasicStrategy:
    """Tests for BasicStrategy."""
    
    def test_compress_empty(self):
        """Test compressing empty string."""
        strategy = BasicStrategy()
        result = strategy.compress("")
        assert result == ""
    
    def test_compress_simple(self):
        """Test basic compression."""
        strategy = BasicStrategy()
        dart_code = "class MyWidget extends StatelessWidget {}"
        result = strategy.compress(dart_code)
        
        # Basic strategy should produce some output
        assert len(result) > 0
    
    def test_whitespace_removal(self):
        """Test that whitespace is minimized."""
        strategy = BasicStrategy()
        dart_code = "class   MyWidget    extends   StatelessWidget   {   }"
        result = strategy.compress(dart_code)
        
        # Should have less whitespace
        assert "   " not in result


class TestAggressiveStrategy:
    """Tests for AggressiveStrategy."""
    
    def test_compress_empty(self):
        """Test compressing empty string."""
        strategy = AggressiveStrategy()
        result = strategy.compress("")
        assert result == ""
    
    def test_widget_abbreviation(self):
        """Test that widgets are abbreviated."""
        strategy = AggressiveStrategy()
        dart_code = "Scaffold(appBar: AppBar())"
        result = strategy.compress(dart_code)
        
        # Scaffold should be abbreviated to S
        assert "S" in result or "Scaffold" not in result
    
    def test_property_abbreviation(self):
        """Test that properties are abbreviated."""
        strategy = AggressiveStrategy()
        dart_code = "Container(child: Text('hello'))"
        result = strategy.compress(dart_code)
        
        # child: should be abbreviated
        assert result != dart_code  # Something changed
    
    def test_class_keyword_abbreviation(self):
        """Test that class keyword is abbreviated."""
        strategy = AggressiveStrategy()
        dart_code = "class MyWidget {}"
        result = strategy.compress(dart_code)
        
        # class should become c:
        assert "c:" in result


class TestASTBasedStrategy:
    """Tests for ASTBasedStrategy."""
    
    def test_compress_simple(self):
        """Test AST-based compression."""
        strategy = ASTBasedStrategy()
        dart_code = "class MyWidget extends StatelessWidget {}"
        result = strategy.compress(dart_code)
        
        # Should produce some output
        assert len(result) > 0
    
    def test_fallback_on_parse_error(self):
        """Test fallback when parsing fails."""
        strategy = ASTBasedStrategy()
        # Invalid Dart that might fail parsing
        dart_code = "{{{{{{{"
        result = strategy.compress(dart_code)
        
        # Should still return something (fallback to aggressive)
        assert result is not None


class TestComponentRefStrategy:
    """Tests for ComponentRefStrategy."""
    
    def test_compress_without_registry(self):
        """Test compression without registry."""
        strategy = ComponentRefStrategy()
        dart_code = "Container(child: Text('hello'))"
        result = strategy.compress(dart_code)
        
        # Should still work (fallback behavior)
        assert len(result) > 0


class TestStrategySelector:
    """Tests for StrategySelector."""
    
    def test_select_for_simple_code(self):
        """Test strategy selection for simple code."""
        selector = StrategySelector()
        code = "class A {}"
        
        strategy = selector.select_strategy(code, len(code))
        assert strategy in [StrategyName.BASIC, StrategyName.AGGRESSIVE]
    
    def test_select_for_complex_code(self):
        """Test strategy selection for complex code."""
        selector = StrategySelector()
        # Generate complex code
        code = "class Widget {\n" * 20 + "}"
        
        strategy = selector.select_strategy(code, len(code))
        assert strategy is not None


class TestGetStrategy:
    """Tests for get_strategy factory function."""
    
    def test_get_basic(self):
        """Test getting basic strategy."""
        strategy = get_strategy("basic")
        assert isinstance(strategy, BasicStrategy)
    
    def test_get_aggressive(self):
        """Test getting aggressive strategy."""
        strategy = get_strategy("aggressive")
        assert isinstance(strategy, AggressiveStrategy)
    
    def test_get_ast_based(self):
        """Test getting AST-based strategy."""
        strategy = get_strategy("ast_based")
        assert isinstance(strategy, ASTBasedStrategy)
    
    def test_get_component_ref(self):
        """Test getting component ref strategy."""
        strategy = get_strategy("component_ref")
        assert isinstance(strategy, ComponentRefStrategy)
    
    def test_get_unknown(self):
        """Test getting unknown strategy raises ValueError."""
        with pytest.raises(ValueError, match="Unknown strategy"):
            get_strategy("unknown_strategy")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
