from typing import List
from ..lexer.base import Token

class Normalizer:
    @staticmethod
    def normalize(tokens: List[Token]) -> List[str]:
        # Filter out comments and whitespaces, extract normalized strings
        return [
            t.normalized for t in tokens 
            if t.type not in ('COMMENT', 'WHITESPACE')
        ]
