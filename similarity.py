from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def compute_cosine(text1, text2):
    if not text1 or not text2:
        return 0.0
    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(sim)
    except ValueError:
        return 0.0

def compute_jaccard(tokens1, tokens2, n=3):
    from processing import generate_ngrams
    set1 = set(generate_ngrams(tokens1, n))
    set2 = set(generate_ngrams(tokens2, n))
    if not set1 or not set2:
        return 0.0
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return float(len(intersection)) / len(union)

def compute_sentence_match(sentences1, sentences2, threshold=0.75):
    if not sentences1 or not sentences2:
        return 0.0, []
        
    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform(sentences1 + sentences2)
        s1_vectors = tfidf_matrix[:len(sentences1)]
        s2_vectors = tfidf_matrix[len(sentences1):]
        
        sim_matrix = cosine_similarity(s1_vectors, s2_vectors)
        max_sims = np.max(sim_matrix, axis=1)
        
        matched_count = np.sum(max_sims >= threshold)
        ratio = float(matched_count) / len(sentences1)
        return ratio, max_sims.tolist()
    except ValueError:
        return 0.0, []

def compute_overall_score(cosine, jaccard, sentence_ratio):
    score = 0.4 * cosine + 0.3 * jaccard + 0.3 * sentence_ratio
    return score * 100

def get_verdict(score):
    if score <= 20: return "Original"
    if score <= 40: return "Low"
    if score <= 60: return "Moderate"
    if score <= 80: return "High"
    return "Very High"
