"""
Unit tests for COON core module.
"""

import pytest
from coon.core import (
    Compressor,
    Decompressor,
    CompressionConfig,
    CompressionResult,
    compress_dart,
    decompress_coon,
    count_tokens,
)


class TestCountTokens:
    """Tests for token counting."""
    
    def test_empty_string(self):
        """Test token count for empty string."""
        assert count_tokens("") == 0
    
    def test_short_string(self):
        """Test token count for short strings."""
        assert count_tokens("test") == 1  # 4 chars = 1 token
        assert count_tokens("ab") == 0    # 2 chars = 0 tokens (integer division)
    
    def test_longer_string(self):
        """Test token count for longer strings."""
        assert count_tokens("a" * 100) == 25  # 100/4 = 25


class TestCompressor:
    """Tests for Compressor class."""
    
    def test_init_default_config(self):
        """Test compressor initialization with default config."""
        compressor = Compressor()
        assert compressor.config is not None
        assert compressor.config.strategy == "auto"
    
    def test_init_custom_config(self):
        """Test compressor initialization with custom config."""
        config = CompressionConfig(strategy="aggressive")
        compressor = Compressor(config)
        assert compressor.config.strategy == "aggressive"
    
    def test_compress_empty_input(self):
        """Test compression of empty input."""
        compressor = Compressor()
        result = compressor.compress("")
        
        assert result.compressed_code == ""
        assert result.original_tokens == 0
        assert result.compressed_tokens == 0
        assert result.compression_ratio == 0.0
    
    def test_compress_simple_code(self):
        """Test compression of simple Dart code."""
        compressor = Compressor()
        dart_code = "class MyWidget extends StatelessWidget {}"
        
        result = compressor.compress(dart_code, strategy="basic")
        
        assert isinstance(result, CompressionResult)
        assert result.compressed_code is not None
        assert result.original_tokens > 0
        assert result.strategy_used is not None
    
    def test_compress_with_strategy(self):
        """Test compression with specific strategy."""
        compressor = Compressor()
        dart_code = "class MyWidget extends StatelessWidget {}"
        
        result = compressor.compress(dart_code, strategy="aggressive")
        
        assert result.strategy_used == "aggressive"
    
    def test_compression_result_properties(self):
        """Test CompressionResult properties."""
        result = CompressionResult(
            compressed_code="compressed",
            original_tokens=100,
            compressed_tokens=40,
            compression_ratio=0.6,
            strategy_used="aggressive",
            processing_time_ms=5.0
        )
        
        assert result.token_savings == 60
        assert result.percentage_saved == 60.0
        assert result.original_size == 100
        assert result.compressed_size == 40


class TestDecompressor:
    """Tests for Decompressor class."""
    
    def test_decompress_empty_input(self):
        """Test decompression of empty input."""
        decompressor = Decompressor()
        result = decompressor.decompress("")
        assert result == ""
    
    def test_decompress_whitespace(self):
        """Test decompression of whitespace."""
        decompressor = Decompressor()
        result = decompressor.decompress("   ")
        assert result == ""


class TestConvenienceFunctions:
    """Tests for convenience functions."""
    
    def test_compress_dart(self):
        """Test compress_dart convenience function."""
        dart_code = "class MyClass {}"
        result = compress_dart(dart_code)
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_decompress_coon(self):
        """Test decompress_coon convenience function."""
        # First compress, then decompress
        dart_code = "class MyClass {}"
        compressed = compress_dart(dart_code)
        decompressed = decompress_coon(compressed)
        
        assert isinstance(decompressed, str)


class TestCompressionConfig:
    """Tests for CompressionConfig."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = CompressionConfig()
        
        assert config.strategy == "auto"
        assert config.registry_path is None
        assert config.enable_metrics is False
        assert config.validate_output is False
        assert config.strict_mode is False
    
    def test_custom_values(self):
        """Test custom configuration values."""
        config = CompressionConfig(
            strategy="aggressive",
            enable_metrics=True,
            validate_output=True
        )
        
        assert config.strategy == "aggressive"
        assert config.enable_metrics is True
        assert config.validate_output is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
