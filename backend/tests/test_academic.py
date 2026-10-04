import pytest
from backend.app.services.normalization import Normalizer
from backend.app.services.similarity import SimilarityEngine
from backend.app.lexer.implementations import GenericLexer

def test_c_lexer_normalization():
    code1 = "int add(int a, int b) { return a + b; }"
    code2 = "int sum(int x, int y) { return x + y; }"
    
    lexer = GenericLexer("c")
    tok1 = lexer.analyze(code1).tokens
    tok2 = lexer.analyze(code2).tokens
    
    norm1 = Normalizer.normalize(tok1)
    norm2 = Normalizer.normalize(tok2)
    
    # Structural similarity should be 100% since identifiers are normalized to 'ID'
    sim = SimilarityEngine.compare(norm1, norm2)
    assert sim['similarity'] == 100.0

def test_different_code():
    code1 = "int add(int a, int b) { return a + b; }"
    code2 = "void print_hello() { printf('hello'); }"
    
    lexer = GenericLexer("c")
    tok1 = lexer.analyze(code1).tokens
    tok2 = lexer.analyze(code2).tokens
    
    norm1 = Normalizer.normalize(tok1)
    norm2 = Normalizer.normalize(tok2)
    
    sim = SimilarityEngine.compare(norm1, norm2)
    assert sim['similarity'] < 50.0

def test_comment_removal():
    code1 = "int add(int a, int b) { return a + b; }"
    code2 = "int add(int a, int b) { \n// this is a comment\nreturn a + b; }"
    
    lexer = GenericLexer("c")
    tok1 = lexer.analyze(code1).tokens
    tok2 = lexer.analyze(code2).tokens
    
    norm1 = Normalizer.normalize(tok1)
    norm2 = Normalizer.normalize(tok2)
    
    sim = SimilarityEngine.compare(norm1, norm2)
    assert sim['similarity'] == 100.0
