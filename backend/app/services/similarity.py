from typing import List, Dict, Any
from .normalization import Normalizer
from ..lexer.implementations import GenericLexer

def get_ngrams(tokens: List[str], n: int = 3) -> List[tuple]:
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

class SimilarityEngine:
    @staticmethod
    def compare(tokens_a: List[str], tokens_b: List[str]) -> Dict[str, Any]:
        ngrams_a = set(get_ngrams(tokens_a))
        ngrams_b = set(get_ngrams(tokens_b))
        
        if not ngrams_a or not ngrams_b:
            sim = 0.0
        else:
            intersection = ngrams_a.intersection(ngrams_b)
            union = ngrams_a.union(ngrams_b)
            sim = (len(intersection) / len(union)) * 100
            
        return {
            "similarity": round(sim, 2),
            "token_count_a": len(tokens_a),
            "token_count_b": len(tokens_b),
            "matching_tokens": len(intersection) * 3, # rough estimate based on 3-grams
            "matched_regions": []
        }
