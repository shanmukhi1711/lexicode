import re
from typing import List
from .base import Token, LexerResult, BaseLexer

class GenericLexer(BaseLexer):
    def __init__(self, language: str):
        self.language = language

    def analyze(self, source_code: str) -> LexerResult:
        tokens = []
        errors = []
        
        # Simple lexer regex patterns to fulfill base requirements
        patterns = [
            (r'//[^\n]*|/\*.*?\*/|\#[^\n]*', 'COMMENT'),
            (r'".*?"|\'.*?\'', 'STRING'),
            (r'\b(if|else|while|for|return|def|class|int|float|void)\b', 'KEYWORD'),
            (r'\b[a-zA-Z_]\w*\b', 'IDENTIFIER'),
            (r'\d+\.\d+|\d+', 'NUMBER'),
            (r'[+\-*/=<>!&|%]+', 'OPERATOR'),
            (r'[{}()\[\].,;:]', 'PUNCTUATION'),
            (r'\s+', 'WHITESPACE'),
            (r'.', 'UNKNOWN')
        ]
        
        combined_pat = '|'.join(f'(?P<{name}>{pat})' for pat, name in patterns)
        regex = re.compile(combined_pat, re.DOTALL)
        
        lines = source_code.split('\n')
        line_num = 1
        col_num = 1
        
        for match in regex.finditer(source_code):
            token_type = match.lastgroup
            token_val = match.group()
            
            if token_type == 'WHITESPACE':
                newlines = token_val.count('\n')
                if newlines > 0:
                    line_num += newlines
                    col_num = len(token_val) - token_val.rfind('\n')
                else:
                    col_num += len(token_val)
                continue
                
            normalized = token_val
            if token_type == 'IDENTIFIER':
                normalized = 'ID'
            elif token_type == 'NUMBER':
                normalized = 'NUM'
            elif token_type == 'STRING':
                normalized = 'STR'
            elif token_type == 'COMMENT':
                continue # Skip comments entirely
                
            if token_type == 'UNKNOWN':
                errors.append({"line": line_num, "column": col_num, "error_type": "LEXICAL", "message": f"Unknown token '{token_val}'"})
            else:
                tokens.append(Token(value=token_val, type=token_type, line=line_num, column=col_num, normalized=normalized))
            
            col_num += len(token_val)
            
        return LexerResult(tokens=tokens, errors=errors, total_tokens=len(tokens))

class CLexer(GenericLexer):
    def __init__(self): super().__init__("c")

class CppLexer(GenericLexer):
    def __init__(self): super().__init__("cpp")

class JavaLexer(GenericLexer):
    def __init__(self): super().__init__("java")

class PythonLexer(GenericLexer):
    def __init__(self): super().__init__("python")
