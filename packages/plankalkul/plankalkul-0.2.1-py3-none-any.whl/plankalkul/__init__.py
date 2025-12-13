"""
Plankalkul - The First High-Level Programming Language (1945)
============================================================

An interpreter for Konrad Zuse's Plankalkul, designed in 1945.

Building on the work of Rojas et al. (FU Berlin, 2000) who created the
first implementation, this package provides an accessible Python interface.

Usage:
    from plankalkul import run, parse
    
    result = run('''
        P1 factorial (V0[:8.0]) => R0[:8.0]
            1 => R0[:8.0]
            1 => Z0[:8.0]
            W [ Z0[:8.0] * R0[:8.0] => R0[:8.0]
                Z0[:8.0] + 1 => Z0[:8.0] ] (Z0[:8.0] <= V0[:8.0])
        END
    ''', 5)
    print(result['R0'])  # 120

Author: The Ian Index (2025)
License: MIT
"""

__version__ = "0.2.0"
__author__ = "Zane Hambly / The Ian Index"

from .interpreter import (
    parse,
    run,
    Lexer,
    Parser,
    Interpreter,
    Program,
    Variable,
    Literal,
    BinaryOp,
    UnaryOp,
    Assignment,
    Conditional,
    WhileLoop,
    ForLoop,
    CountedLoop,
    ArrayAccess,
    TypeAnnotation,
)

__all__ = [
    "parse",
    "run",
    "Lexer",
    "Parser", 
    "Interpreter",
    "Program",
    "Variable",
    "Literal",
    "BinaryOp",
    "UnaryOp",
    "Assignment",
    "Conditional",
    "WhileLoop",
    "ForLoop",
    "CountedLoop",
    "ArrayAccess",
    "TypeAnnotation",
]

