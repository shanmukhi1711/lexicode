import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from bs4 import BeautifulSoup

def clean_text(text, ignore_quotes=False, ignore_bibliography=False):
    if not text:
        return ""
    
    # Optional bibliography filtering
    if ignore_bibliography:
        text = re.split(r'\n(?i:references|bibliography)\b', text, maxsplit=1)[0]
    
    # Optional quote filtering
    if ignore_quotes:
        text = re.sub(r'["\'].*?["\']', '', text)
        
    # Strip HTML if any
    text = BeautifulSoup(text, "html.parser").get_text()
    
    # Lowercase and normalize whitespace
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_text(text):
    """Returns a list of preprocessed sentences and a list of all tokens."""
    try:
        sentences = sent_tokenize(text)
    except LookupError:
        # Fallback if punkt is missing
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
    try:
        stop_words = set(stopwords.words('english'))
    except LookupError:
        stop_words = {'the', 'is', 'in', 'and', 'to', 'a', 'of', 'for', 'on', 'with', 'as'}
        
    stemmer = PorterStemmer()
    
    processed_sentences = []
    all_tokens = []
    
    for sentence in sentences:
        words = re.findall(r'\b\w+\b', sentence)
        tokens = [stemmer.stem(w) for w in words if w not in stop_words]
        processed_sentences.append(" ".join(tokens))
        all_tokens.extend(tokens)
        
    return processed_sentences, all_tokens

def generate_ngrams(tokens, n):
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]
