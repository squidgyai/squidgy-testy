from squidgy_testy.model import SimilarToAssertionData
from squidgy_testy.assertions import similarTo
from squidgy_testy.gpt3 import Gpt3PromptService

def test_similar_to():
    similar_to = SimilarToAssertionData(value="hello", threshold=0.85)
    service = Gpt3PromptService()

    similar, score = similarTo(service, "hello", similar_to)
    assert similar

    similar, score = similarTo(service, "dog", similar_to)
    assert not similar
    assert score < 0.85

    similar, score = similarTo(service, "bonjour", similar_to)
    assert similar
    assert score > 0.85