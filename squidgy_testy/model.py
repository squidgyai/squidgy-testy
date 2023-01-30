from pydantic import BaseModel
from pydantic_yaml import YamlModel

class SimilarToAssertion(BaseModel):
    value: str
    threshold: float

class Assertions(BaseModel):
    startsWith: str | None
    equalTo: str | None
    similarTo: SimilarToAssertion | None

class Test(BaseModel):
    prompt_file: str
    prompt_append: str | None
    params: dict[str, str] | None
    stop: list[str] | None
    assertions: Assertions

class TestSuite(YamlModel):
    tests: dict[str, Test]
