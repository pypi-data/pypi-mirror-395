"""
Pytest configuration and fixtures for COON tests.
"""

import pytest
from pathlib import Path


# Sample Dart code for testing
SAMPLE_DART_CODE = """
import 'package:flutter/material.dart';

class MyHomePage extends StatelessWidget {
  const MyHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('My App'),
        backgroundColor: Colors.blue,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Hello, World!'),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {},
              child: const Text('Click Me'),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        child: const Icon(Icons.add),
      ),
    );
  }
}
"""

SIMPLE_CLASS = "class MyWidget extends StatelessWidget {}"

SIMPLE_WIDGET = "Container(child: Text('hello'))"


@pytest.fixture
def sample_dart_code():
    """Provide sample Dart code for tests."""
    return SAMPLE_DART_CODE


@pytest.fixture
def simple_class():
    """Provide simple class definition."""
    return SIMPLE_CLASS


@pytest.fixture
def simple_widget():
    """Provide simple widget code."""
    return SIMPLE_WIDGET


@pytest.fixture
def spec_dir():
    """Get the spec directory path."""
    return Path(__file__).parent.parent.parent.parent / "spec"


@pytest.fixture
def fixtures_dir(spec_dir):
    """Get the fixtures directory path."""
    return spec_dir / "fixtures" / "conformance"


@pytest.fixture
def data_dir(spec_dir):
    """Get the data directory path."""
    return spec_dir / "data"
