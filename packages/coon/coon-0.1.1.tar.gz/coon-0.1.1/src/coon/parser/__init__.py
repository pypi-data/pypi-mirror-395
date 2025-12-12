"""
Parser module for COON.

Provides lexical analysis and parsing of Dart code into an AST.
"""

from .tokens import Token, TokenType, DART_KEYWORDS, FLUTTER_WIDGETS, classify_identifier
from .lexer import DartLexer
from .ast_nodes import ASTNode, NodeType, create_root_node, create_class_node, create_function_node, create_variable_node, create_import_node
from .parser import DartParser


__all__ = [
    # Token classes
    "Token",
    "TokenType",
    
    # Token constants
    "DART_KEYWORDS",
    "FLUTTER_WIDGETS",
    "classify_identifier",
    
    # Lexer
    "DartLexer",
    
    # AST
    "ASTNode",
    "NodeType",
    "create_root_node",
    "create_class_node",
    "create_function_node",
    "create_variable_node",
    "create_import_node",
    
    # Parser
    "DartParser",
]
