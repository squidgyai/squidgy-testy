from .model import SimilarToAssertion
from .service import PromptService
from numpy import dot
from numpy.linalg import norm

def cos_sim(a, b):
    return dot(a, b)/(norm(a)*norm(b))
    
def equalTo(result: str, expected: str):
    return result == expected

def similarTo(service: PromptService, result: str, similarTo: SimilarToAssertion) -> tuple[bool, float]:
    response = service.embed([similarTo.value, result])

    embeddings = [d['embedding'] for d in response['data']]
    
    score = cos_sim(embeddings[0], embeddings[1])

    return score > similarTo.threshold, score