#!/usr/bin/env python3
"""
Plankalkül Interpreter
======================

The first high-level programming language, designed by Konrad Zuse in 1945.
This implementation completes Zuse's vision - 80 years later.

Author: The Ian Index (2025)
Building on: Rojas et al., FU Berlin (2000) - first implementation
License: MIT

Historical Note:
    Plankalkül ("Plan Calculus") was designed by Konrad Zuse between 1942-1945
    during World War II in Germany. It introduced:
    - Data structures (Komponente)
    - User-defined types
    - Assertions
    - Structured control flow
    - Arrays with arbitrary dimensions
    
    It was never implemented during Zuse's lifetime. The first implementation
    was by FU Berlin in 2000 - 55 years after design.
    
    This implementation aims to be faithful to Zuse's original notation while
    being practical to use in the modern era.

Syntax Reference:
    Types:
        [:8.0]      8-bit integer
        [:1.0]      1-bit (boolean)
        [:n×m.0]    n×m array
    
    Variables:
        V0, V1...   Input parameters
        Z0, Z1...   Local/intermediate variables
        R0, R1...   Return values
    
    Operations:
        →  or =>    Assignment
        +, -, ×, :  Arithmetic (: is division)
        =, ≠, <, >  Comparison
        ∧, ∨, ¬     Logical
    
    Control Flow:
        (cond) → stmt           Conditional execution
        W [ stmts ] (cond)      While loop
        W [ stmts ] (i: 0...n)  For loop
    
    Program Structure:
        P<n> name (params) → results
            statements
        END
"""

import sys
import re
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple, Union
from enum import Enum, auto

# Ensure UTF-8 output
if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')

# ============================================================================
# TOKEN DEFINITIONS
# ============================================================================

class TokenType(Enum):
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    BOOLEAN = auto()
    
    # Identifiers  
    VAR_V = auto()      # Input variable (V0, V1...)
    VAR_Z = auto()      # Intermediate variable (Z0, Z1...)
    VAR_R = auto()      # Result variable (R0, R1...)
    IDENTIFIER = auto() # Program/function name
    
    # Type annotations
    TYPE_ANNOTATION = auto()  # [:8.0]
    
    # Operators
    ARROW = auto()      # → or =>
    PLUS = auto()       # +
    MINUS = auto()      # -
    MULTIPLY = auto()   # × or *
    DIVIDE = auto()     # : or /
    
    # Comparison
    EQ = auto()         # =
    NEQ = auto()        # ≠ or !=
    LT = auto()         # <
    GT = auto()         # >
    LEQ = auto()        # ≤ or <=
    GEQ = auto()        # ≥ or >=
    
    # Logical
    AND = auto()        # ∧ or &
    OR = auto()         # ∨ or |
    NOT = auto()        # ¬ or !
    
    # Delimiters
    LPAREN = auto()     # (
    RPAREN = auto()     # )
    LBRACKET = auto()   # [
    RBRACKET = auto()   # ]
    COMMA = auto()      # ,
    COLON = auto()      # :
    SEMICOLON = auto()  # ;
    
    # Keywords
    P = auto()          # Program declaration
    END = auto()        # End of program
    W = auto()          # While/for loop
    W1 = auto()         # Counted loop (0 to n-1)
    FIN = auto()        # Terminate
    
    # Block delimiters
    LBRACE = auto()     # {
    RBRACE = auto()     # }
    
    # Special
    NEWLINE = auto()
    EOF = auto()
    COMMENT = auto()

@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r})"

# ============================================================================
# LEXER
# ============================================================================

class Lexer:
    """Tokenizer for Plankalkül source code."""
    
    # Unicode to ASCII equivalents
    UNICODE_MAP = {
        '→': '=>',
        '×': '*',
        '≠': '!=',
        '≤': '<=', 
        '≥': '>=',
        '∧': '&',
        '∨': '|',
        '¬': '!',
    }
    
    def __init__(self, source: str):
        self.source = self._normalize_unicode(source)
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def _normalize_unicode(self, source: str) -> str:
        """Replace Unicode symbols with ASCII equivalents."""
        for unicode_char, ascii_equiv in self.UNICODE_MAP.items():
            source = source.replace(unicode_char, ascii_equiv)
        return source
    
    def _current_char(self) -> Optional[str]:
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def _peek(self, offset: int = 1) -> Optional[str]:
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def _advance(self) -> str:
        char = self._current_char()
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def _skip_whitespace(self):
        while self._current_char() and self._current_char() in ' \t\r':
            self._advance()
    
    def _skip_comment(self):
        """Skip comment (starts with ; until end of line)."""
        while self._current_char() and self._current_char() != '\n':
            self._advance()
    
    def _read_number(self) -> Token:
        """Read integer or float literal."""
        start_col = self.column
        num_str = ''
        
        while self._current_char() and (self._current_char().isdigit() or self._current_char() == '.'):
            num_str += self._advance()
        
        if '.' in num_str:
            return Token(TokenType.FLOAT, float(num_str), self.line, start_col)
        return Token(TokenType.INTEGER, int(num_str), self.line, start_col)
    
    def _read_identifier(self) -> Token:
        """Read identifier or keyword."""
        start_col = self.column
        ident = ''
        
        while self._current_char() and (self._current_char().isalnum() or self._current_char() == '_'):
            ident += self._advance()
        
        # Check for keywords
        upper = ident.upper()
        if upper == 'END':
            return Token(TokenType.END, ident, self.line, start_col)
        elif upper == 'FIN':
            return Token(TokenType.FIN, ident, self.line, start_col)
        elif upper == 'TRUE' or upper == '#T':
            return Token(TokenType.BOOLEAN, True, self.line, start_col)
        elif upper == 'FALSE' or upper == '#F':
            return Token(TokenType.BOOLEAN, False, self.line, start_col)
        
        # Check for P followed by number (P1, P2, etc.) - program declaration
        if len(ident) >= 2 and ident[0].upper() == 'P' and ident[1:].isdigit():
            # Return P token, but we need to put the number back
            # Actually, return P token and let parser expect INTEGER next
            # We'll handle this by making P1 return P then 1
            self.pos -= len(ident) - 1  # Put back all but 'P'
            self.column -= len(ident) - 1
            return Token(TokenType.P, 'P', self.line, start_col)
        
        # Check for bare P (Hovestar format: P FunctionName(...))
        if upper == 'P':
            return Token(TokenType.P, 'P', self.line, start_col)
        
        # Check for W1 (counted loop keyword)
        if upper == 'W1':
            return Token(TokenType.W1, ident, self.line, start_col)
        
        # Check for W (loop keyword)
        if upper == 'W':
            return Token(TokenType.W, ident, self.line, start_col)
        
        # Check for variable names (V0, Z1, R2, etc.)
        if len(ident) >= 2 and ident[0] in 'VZR' and ident[1:].isdigit():
            var_type = {
                'V': TokenType.VAR_V,
                'Z': TokenType.VAR_Z,
                'R': TokenType.VAR_R
            }[ident[0]]
            return Token(var_type, int(ident[1:]), self.line, start_col)
        
        return Token(TokenType.IDENTIFIER, ident, self.line, start_col)
    
    def _read_type_annotation(self) -> Token:
        """Read type annotation like [:8.0]."""
        start_col = self.column
        self._advance()  # [
        
        annotation = '['
        bracket_depth = 1
        
        while bracket_depth > 0 and self._current_char():
            char = self._advance()
            annotation += char
            if char == '[':
                bracket_depth += 1
            elif char == ']':
                bracket_depth -= 1
        
        return Token(TokenType.TYPE_ANNOTATION, annotation, self.line, start_col)
    
    def tokenize(self) -> List[Token]:
        """Tokenize the source code."""
        self.tokens = []
        
        while self._current_char():
            char = self._current_char()
            
            # Skip whitespace (except newlines)
            if char in ' \t\r':
                self._skip_whitespace()
                continue
            
            # Comments
            if char == ';':
                self._skip_comment()
                continue
            
            # Newlines (significant in some contexts)
            if char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
                self._advance()
                continue
            
            # Numbers
            if char.isdigit():
                self.tokens.append(self._read_number())
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                self.tokens.append(self._read_identifier())
                continue
            
            # Type annotations
            if char == '[' and self._peek() == ':':
                self.tokens.append(self._read_type_annotation())
                continue
            
            # Two-character operators
            if char == '=' and self._peek() == '>':
                self.tokens.append(Token(TokenType.ARROW, '=>', self.line, self.column))
                self._advance()
                self._advance()
                continue
            
            if char == '!' and self._peek() == '=':
                self.tokens.append(Token(TokenType.NEQ, '!=', self.line, self.column))
                self._advance()
                self._advance()
                continue
            
            if char == '<' and self._peek() == '=':
                self.tokens.append(Token(TokenType.LEQ, '<=', self.line, self.column))
                self._advance()
                self._advance()
                continue
            
            if char == '>' and self._peek() == '=':
                self.tokens.append(Token(TokenType.GEQ, '>=', self.line, self.column))
                self._advance()
                self._advance()
                continue
            
            # Single-character operators
            single_char_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '=': TokenType.EQ,
                '<': TokenType.LT,
                '>': TokenType.GT,
                '&': TokenType.AND,
                '|': TokenType.OR,
                '!': TokenType.NOT,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                ',': TokenType.COMMA,
                ':': TokenType.COLON,
            }
            
            if char in single_char_tokens:
                self.tokens.append(Token(single_char_tokens[char], char, self.line, self.column))
                self._advance()
                continue
            
            # Unknown character
            raise SyntaxError(f"Unexpected character '{char}' at line {self.line}, column {self.column}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

# ============================================================================
# AST NODES
# ============================================================================

@dataclass
class TypeAnnotation:
    """Type annotation like [:8.0] (8-bit integer)."""
    bits: int
    is_array: bool = False
    dimensions: List[int] = None
    
    @classmethod
    def parse(cls, annotation: str) -> 'TypeAnnotation':
        """Parse a type annotation string."""
        # Remove brackets
        inner = annotation[2:-1] if annotation.startswith('[:') else annotation
        
        # Check for array dimensions (n×m or n*m)
        if '×' in inner or '*' in inner:
            parts = re.split(r'[×*]', inner)
            dims = [int(p) for p in parts[:-1]]
            bits = int(parts[-1].split('.')[0])
            return cls(bits=bits, is_array=True, dimensions=dims)
        
        # Simple type
        bits = int(inner.split('.')[0])
        return cls(bits=bits)
    
    def __repr__(self):
        if self.is_array:
            dims = '×'.join(str(d) for d in self.dimensions)
            return f"[:{dims}×{self.bits}.0]"
        return f"[:{self.bits}.0]"

@dataclass
class Variable:
    """Variable reference (V0, Z1, R2, etc.)."""
    kind: str  # 'V', 'Z', or 'R'
    index: int
    type_annotation: Optional[TypeAnnotation] = None
    array_index: Optional['Expression'] = None

@dataclass
class Literal:
    """Literal value (integer, float, boolean)."""
    value: Union[int, float, bool]

@dataclass 
class BinaryOp:
    """Binary operation (e.g., V0 + V1)."""
    left: 'Expression'
    operator: str
    right: 'Expression'

@dataclass
class UnaryOp:
    """Unary operation (e.g., !V0)."""
    operator: str
    operand: 'Expression'

@dataclass
class Assignment:
    """Assignment statement (expr => var)."""
    expression: 'Expression'
    target: Variable

@dataclass
class Conditional:
    """Conditional statement ((cond) => stmt)."""
    condition: 'Expression'
    body: 'Statement'

@dataclass
class WhileLoop:
    """While loop (W [ stmts ] (cond))."""
    condition: 'Expression'
    body: List['Statement']

@dataclass
class ForLoop:
    """For loop (W [ stmts ] (i: 0...n))."""
    variable: str
    start: int
    end: 'Expression'
    body: List['Statement']

@dataclass
class CountedLoop:
    """Counted loop W1(n) => counter { body }.
    
    This is the more advanced Plankalkul loop that iterates from 0 to n-1,
    storing the counter in the specified variable.
    
    Example: W1(V0[:i]) => R1[:i] { R0[:i] * (R1[:i]+1) => R0[:i] }
    """
    count: 'Expression'  # Number of iterations
    counter_var: Variable  # Loop counter variable
    body: List['Statement']

@dataclass
class ArrayAccess:
    """Array element access: arr[index:type].
    
    Example: Z0[R1[:i]:X] accesses element at index R1 of array Z0
    """
    array_var: Variable
    index: 'Expression'
    element_type: Optional[str] = None

@dataclass
class Program:
    """Program definition."""
    number: int
    name: str
    parameters: List[Variable]
    returns: List[Variable]
    body: List['Statement']

# Type aliases
Expression = Union[Variable, Literal, BinaryOp, UnaryOp, ArrayAccess]
Statement = Union[Assignment, Conditional, WhileLoop, ForLoop, CountedLoop]

# ============================================================================
# PARSER
# ============================================================================

class Parser:
    """Parser for Plankalkül programs."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = [t for t in tokens if t.type != TokenType.NEWLINE]
        self.pos = 0
    
    def _current(self) -> Token:
        if self.pos >= len(self.tokens):
            return self.tokens[-1]  # EOF
        return self.tokens[self.pos]
    
    def _peek(self, offset: int = 1) -> Token:
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[pos]
    
    def _advance(self) -> Token:
        token = self._current()
        self.pos += 1
        return token
    
    def _expect(self, token_type: TokenType, value: Any = None) -> Token:
        token = self._current()
        if token.type != token_type:
            raise SyntaxError(f"Expected {token_type.name}, got {token.type.name} at line {token.line}")
        if value is not None and token.value != value:
            raise SyntaxError(f"Expected '{value}', got '{token.value}' at line {token.line}")
        return self._advance()
    
    def _match(self, *types: TokenType) -> bool:
        return self._current().type in types
    
    def parse_program(self) -> Program:
        """Parse a complete program.
        
        Supports two formats:
        1. P<n> name (params) => returns   (Zuse format: P2 factorial)
        2. P name (params) => returns      (Hovestar format: P Factorial)
        """
        self._expect(TokenType.P)
        
        # Number is optional (Hovestar format doesn't use it)
        number = 0
        if self._match(TokenType.INTEGER):
            number_token = self._advance()
            number = number_token.value
        
        name_token = self._expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        # Parameters
        self._expect(TokenType.LPAREN)
        params = self._parse_var_list()
        self._expect(TokenType.RPAREN)
        
        # Arrow
        self._expect(TokenType.ARROW)
        
        # Returns
        returns = []
        if self._match(TokenType.LPAREN):
            self._advance()
            returns = self._parse_var_list()
            self._expect(TokenType.RPAREN)
        else:
            returns = [self._parse_variable()]
        
        # Body
        body = []
        while not self._match(TokenType.END, TokenType.EOF):
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
        
        self._expect(TokenType.END)
        
        return Program(number, name, params, returns, body)
    
    def _parse_var_list(self) -> List[Variable]:
        """Parse comma-separated variable list."""
        vars = []
        if not self._match(TokenType.RPAREN):
            vars.append(self._parse_variable())
            while self._match(TokenType.COMMA):
                self._advance()
                vars.append(self._parse_variable())
        return vars
    
    def _parse_variable(self) -> Variable:
        """Parse a variable reference."""
        kind_map = {
            TokenType.VAR_V: 'V',
            TokenType.VAR_Z: 'Z',
            TokenType.VAR_R: 'R'
        }
        
        if self._current().type not in kind_map:
            raise SyntaxError(f"Expected variable, got {self._current().type.name}")
        
        token = self._advance()
        kind = kind_map[token.type]
        index = token.value
        
        # Optional type annotation
        type_ann = None
        if self._match(TokenType.TYPE_ANNOTATION):
            type_ann = TypeAnnotation.parse(self._advance().value)
        
        # Optional array index
        array_idx = None
        if self._match(TokenType.LBRACKET):
            self._advance()
            array_idx = self._parse_expression()
            self._expect(TokenType.RBRACKET)
        
        return Variable(kind, index, type_ann, array_idx)
    
    def _parse_statement(self) -> Optional[Statement]:
        """Parse a statement."""
        # Conditional: (expr) => stmt
        if self._match(TokenType.LPAREN):
            return self._parse_conditional()
        
        # While/For loop: W [ ... ]
        if self._match(TokenType.W):
            return self._parse_loop()
        
        # Counted loop: W1(n) => counter { body }
        if self._match(TokenType.W1):
            return self._parse_counted_loop()
        
        # Assignment: expr => var
        expr = self._parse_expression()
        if self._match(TokenType.ARROW):
            self._advance()
            target = self._parse_variable()
            return Assignment(expr, target)
        
        return None
    
    def _parse_conditional(self) -> Conditional:
        """Parse conditional: (condition) => statement."""
        self._expect(TokenType.LPAREN)
        condition = self._parse_expression()
        self._expect(TokenType.RPAREN)
        self._expect(TokenType.ARROW)
        body = self._parse_statement()
        return Conditional(condition, body)
    
    def _parse_loop(self) -> Union[WhileLoop, ForLoop]:
        """Parse while or for loop."""
        self._expect(TokenType.W)
        self._expect(TokenType.LBRACKET)
        
        body = []
        while not self._match(TokenType.RBRACKET):
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
        
        self._expect(TokenType.RBRACKET)
        self._expect(TokenType.LPAREN)
        
        # Check if it's a for loop (i: 0...n) or while (condition)
        condition = self._parse_expression()
        self._expect(TokenType.RPAREN)
        
        return WhileLoop(condition, body)
    
    def _parse_counted_loop(self) -> CountedLoop:
        """Parse counted loop: W1(n) => counter { body }.
        
        This is the advanced Plankalkul loop syntax used in the original
        documents. It iterates from 0 to n-1, with the counter variable
        being updated each iteration.
        
        Example: W1(V0[:i]) => R1[:i] { R0[:i] * (R1[:i]+1) => R0[:i] }
        """
        self._expect(TokenType.W1)
        self._expect(TokenType.LPAREN)
        
        # Parse the count expression (e.g., V0[:i], m-1)
        count_expr = self._parse_expression()
        
        self._expect(TokenType.RPAREN)
        self._expect(TokenType.ARROW)
        
        # Parse the counter variable (e.g., R1[:i])
        counter_var = self._parse_variable()
        
        # Parse body in curly braces
        self._expect(TokenType.LBRACE)
        
        body = []
        while not self._match(TokenType.RBRACE):
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
        
        self._expect(TokenType.RBRACE)
        
        return CountedLoop(count_expr, counter_var, body)
    
    def _parse_expression(self) -> Expression:
        """Parse an expression."""
        return self._parse_comparison()
    
    def _parse_comparison(self) -> Expression:
        """Parse comparison expression."""
        left = self._parse_additive()
        
        while self._match(TokenType.EQ, TokenType.NEQ, TokenType.LT, 
                          TokenType.GT, TokenType.LEQ, TokenType.GEQ):
            op = self._advance().value
            right = self._parse_additive()
            left = BinaryOp(left, op, right)
        
        return left
    
    def _parse_additive(self) -> Expression:
        """Parse additive expression (+, -)."""
        left = self._parse_multiplicative()
        
        while self._match(TokenType.PLUS, TokenType.MINUS):
            op = self._advance().value
            right = self._parse_multiplicative()
            left = BinaryOp(left, op, right)
        
        return left
    
    def _parse_multiplicative(self) -> Expression:
        """Parse multiplicative expression (*, /)."""
        left = self._parse_unary()
        
        while self._match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.COLON):
            op = self._advance().value
            if op == ':':
                op = '/'  # Plankalkül uses : for division
            right = self._parse_unary()
            left = BinaryOp(left, op, right)
        
        return left
    
    def _parse_unary(self) -> Expression:
        """Parse unary expression (!, -)."""
        if self._match(TokenType.NOT, TokenType.MINUS):
            op = self._advance().value
            operand = self._parse_unary()
            return UnaryOp(op, operand)
        
        return self._parse_primary()
    
    def _parse_primary(self) -> Expression:
        """Parse primary expression (literals, variables, parenthesized)."""
        # Parenthesized expression
        if self._match(TokenType.LPAREN):
            self._advance()
            expr = self._parse_expression()
            self._expect(TokenType.RPAREN)
            return expr
        
        # Integer literal
        if self._match(TokenType.INTEGER):
            return Literal(self._advance().value)
        
        # Float literal
        if self._match(TokenType.FLOAT):
            return Literal(self._advance().value)
        
        # Boolean literal
        if self._match(TokenType.BOOLEAN):
            return Literal(self._advance().value)
        
        # Variable
        if self._match(TokenType.VAR_V, TokenType.VAR_Z, TokenType.VAR_R):
            return self._parse_variable()
        
        raise SyntaxError(f"Unexpected token {self._current().type.name}")

# ============================================================================
# INTERPRETER
# ============================================================================

class Interpreter:
    """Interpreter for Plankalkül programs."""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.variables: Dict[str, Any] = {}
        self.programs: Dict[str, Program] = {}
    
    def _var_key(self, var: Variable) -> str:
        """Get dictionary key for a variable."""
        return f"{var.kind}{var.index}"
    
    def _get_var(self, var: Variable) -> Any:
        """Get variable value."""
        key = self._var_key(var)
        if key not in self.variables:
            return 0  # Default to 0
        value = self.variables[key]
        
        # Handle array indexing
        if var.array_index is not None:
            idx = self._eval_expr(var.array_index)
            if isinstance(value, list):
                return value[idx]
        
        return value
    
    def _set_var(self, var: Variable, value: Any):
        """Set variable value."""
        key = self._var_key(var)
        
        # Handle array indexing
        if var.array_index is not None:
            idx = self._eval_expr(var.array_index)
            if key not in self.variables:
                self.variables[key] = []
            while len(self.variables[key]) <= idx:
                self.variables[key].append(0)
            self.variables[key][idx] = value
        else:
            self.variables[key] = value
        
        if self.debug:
            print(f"  {key} = {value}")
    
    def _eval_expr(self, expr: Expression) -> Any:
        """Evaluate an expression."""
        if isinstance(expr, Literal):
            return expr.value
        
        if isinstance(expr, Variable):
            return self._get_var(expr)
        
        if isinstance(expr, UnaryOp):
            operand = self._eval_expr(expr.operand)
            if expr.operator == '!':
                return not operand
            if expr.operator == '-':
                return -operand
        
        if isinstance(expr, BinaryOp):
            left = self._eval_expr(expr.left)
            right = self._eval_expr(expr.right)
            
            ops = {
                '+': lambda a, b: a + b,
                '-': lambda a, b: a - b,
                '*': lambda a, b: a * b,
                '/': lambda a, b: a // b if isinstance(a, int) and isinstance(b, int) else a / b,
                '=': lambda a, b: a == b,
                '!=': lambda a, b: a != b,
                '<': lambda a, b: a < b,
                '>': lambda a, b: a > b,
                '<=': lambda a, b: a <= b,
                '>=': lambda a, b: a >= b,
                '&': lambda a, b: a and b,
                '|': lambda a, b: a or b,
            }
            
            if expr.operator in ops:
                return ops[expr.operator](left, right)
        
        if isinstance(expr, ArrayAccess):
            # Get the array and index
            array = self._get_var(expr.array_var)
            index = int(self._eval_expr(expr.index))
            if isinstance(array, (list, tuple)):
                return array[index]
            raise RuntimeError(f"Cannot index non-array: {expr.array_var}")
        
        raise RuntimeError(f"Cannot evaluate expression: {expr}")
    
    def _exec_stmt(self, stmt: Statement):
        """Execute a statement."""
        if isinstance(stmt, Assignment):
            value = self._eval_expr(stmt.expression)
            self._set_var(stmt.target, value)
        
        elif isinstance(stmt, Conditional):
            if self._eval_expr(stmt.condition):
                self._exec_stmt(stmt.body)
        
        elif isinstance(stmt, WhileLoop):
            while self._eval_expr(stmt.condition):
                for s in stmt.body:
                    self._exec_stmt(s)
        
        elif isinstance(stmt, ForLoop):
            start = stmt.start
            end = self._eval_expr(stmt.end)
            for i in range(start, end + 1):
                self.variables[stmt.variable] = i
                for s in stmt.body:
                    self._exec_stmt(s)
        
        elif isinstance(stmt, CountedLoop):
            # W1(n) => counter { body }
            # Iterates from 0 to n-1, setting counter each iteration
            count = self._eval_expr(stmt.count)
            for i in range(int(count)):
                self._set_var(stmt.counter_var, i)
                for s in stmt.body:
                    self._exec_stmt(s)
    
    def run(self, program: Program, *args) -> Dict[str, Any]:
        """Run a program with given arguments."""
        self.variables = {}
        
        # Set input parameters
        for i, (param, arg) in enumerate(zip(program.parameters, args)):
            self._set_var(param, arg)
        
        if self.debug:
            print(f"Running P{program.number} {program.name}")
            print(f"  Inputs: {list(zip([self._var_key(p) for p in program.parameters], args))}")
        
        # Execute body
        for stmt in program.body:
            self._exec_stmt(stmt)
        
        # Collect results
        results = {}
        for ret in program.returns:
            key = self._var_key(ret)
            results[key] = self.variables.get(key, 0)
        
        if self.debug:
            print(f"  Results: {results}")
        
        return results

# ============================================================================
# MAIN INTERFACE
# ============================================================================

def parse(source: str) -> Program:
    """Parse Plankalkül source code into AST."""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse_program()

def run(source: str, *args, debug: bool = False) -> Dict[str, Any]:
    """Parse and run Plankalkül source code."""
    program = parse(source)
    interpreter = Interpreter(debug=debug)
    return interpreter.run(program, *args)

def main():
    """Main entry point with demo programs."""
    print("=" * 70)
    print("  PLANKALKÜL INTERPRETER")
    print("  The First High-Level Programming Language (1945)")
    print("  Completing Konrad Zuse's Vision - 80 Years Later")
    print("=" * 70)
    print()
    
    # Demo: Maximum of two numbers
    max_program = """
    P1 max (V0[:8.0], V1[:8.0]) => R0[:8.0]
        V0[:8.0] => R0[:8.0]
        (R0[:8.0] < V1[:8.0]) => V1[:8.0] => R0[:8.0]
    END
    """
    
    print("1. Maximum of two numbers")
    print("-" * 40)
    result = run(max_program, 5, 8)
    print(f"   max(5, 8) = {result['R0']}")
    print()
    
    # Demo: Factorial
    fact_program = """
    P2 factorial (V0[:8.0]) => R0[:8.0]
        1 => R0[:8.0]
        1 => Z0[:8.0]
        W [ Z0[:8.0] * R0[:8.0] => R0[:8.0]
            Z0[:8.0] + 1 => Z0[:8.0] ] (Z0[:8.0] <= V0[:8.0])
    END
    """
    
    print("2. Factorial")
    print("-" * 40)
    result = run(fact_program, 5)
    print(f"   factorial(5) = {result['R0']}")
    print()
    
    # PRACTICAL: Loan Calculator
    loan_program = """
    P20 loan (V0[:32.0], V1[:32.0], V2[:32.0]) => R0[:32.0]
        ; Calculate simple interest loan payment
        ; V0 = principal, V1 = rate%, V2 = years
        V0[:32.0] * V1[:32.0] => Z0[:32.0]
        Z0[:32.0] * V2[:32.0] => Z1[:32.0]
        Z1[:32.0] / 100 => Z2[:32.0]
        V0[:32.0] + Z2[:32.0] => Z3[:32.0]
        V2[:32.0] * 12 => Z4[:32.0]
        Z3[:32.0] / Z4[:32.0] => R0[:32.0]
    END
    """
    
    print("3. PRACTICAL: Loan Payment Calculator")
    print("-" * 40)
    print("   Loan: $10,000 at 5% for 3 years")
    result = run(loan_program, 10000, 5, 3)
    print(f"   Monthly payment: ${result['R0']}")
    print(f"   (Total interest: $1500, Total: $11500)")
    print()
    
    # PRACTICAL: Temperature Converter
    temp_program = """
    P22 c_to_f (V0[:16.0]) => R0[:16.0]
        V0[:16.0] * 9 => Z0[:16.0]
        Z0[:16.0] / 5 => Z1[:16.0]
        Z1[:16.0] + 32 => R0[:16.0]
    END
    """
    
    print("4. PRACTICAL: Temperature Converter")
    print("-" * 40)
    result = run(temp_program, 100)
    print(f"   100°C = {result['R0']}°F (boiling point)")
    result = run(temp_program, 0)
    print(f"   0°C = {result['R0']}°F (freezing point)")
    result = run(temp_program, 37)
    print(f"   37°C = {result['R0']}°F (body temperature)")
    print()
    
    # PRACTICAL: Percentage Calculator
    percent_program = """
    P27 percent_of (V0[:32.0], V1[:32.0]) => R0[:32.0]
        V1[:32.0] * V0[:32.0] => Z0[:32.0]
        Z0[:32.0] / 100 => R0[:32.0]
    END
    """
    
    print("5. PRACTICAL: Percentage Calculator")
    print("-" * 40)
    result = run(percent_program, 15, 200)
    print(f"   15% of 200 = {result['R0']}")
    result = run(percent_program, 20, 500)
    print(f"   20% of 500 = {result['R0']} (tip calculator!)")
    print()
    
    # PRACTICAL: Distance/Speed/Time
    dst_program = """
    P24 distance (V0[:32.0], V1[:32.0]) => R0[:32.0]
        V0[:32.0] * V1[:32.0] => R0[:32.0]
    END
    """
    
    print("6. PRACTICAL: Distance Calculator")
    print("-" * 40)
    result = run(dst_program, 60, 3)
    print(f"   At 60 mph for 3 hours = {result['R0']} miles")
    result = run(dst_program, 100, 5)
    print(f"   At 100 km/h for 5 hours = {result['R0']} km")
    print()
    
    print("=" * 70)
    print("  ZUSE'S VISION LIVES ON")
    print("  These practical programs could have run in 1945!")
    print("=" * 70)

if __name__ == '__main__':
    main()

