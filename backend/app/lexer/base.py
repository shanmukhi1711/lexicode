from pydantic import BaseModel
from typing import List, Optional

class Token(BaseModel):
    value: str
    type: str
    line: int
    column: int
    normalized: str

class LexicalError(BaseModel):
    line: int
    column: int
    error_type: str
    message: str

class LexerResult(BaseModel):
    tokens: List[Token]
    errors: List[LexicalError]
    total_tokens: int

class BaseLexer:
    def analyze(self, source_code: str) -> LexerResult:
        raise NotImplementedError("analyze method must be implemented by subclasses")
