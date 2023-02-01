from pydantic import BaseModel
from pydantic_yaml import YamlModel
from typing import Optional

class SimilarToAssertion(BaseModel):
    value: str
    threshold: float

class Assertions(BaseModel):
    startsWith: Optional[str]
    equalTo: Optional[str]
    similarTo: Optional[SimilarToAssertion]

class Test(BaseModel):
    prompt_file: str
    prompt_append: Optional[str]
    params: Optional[dict[str, str]]
    stop: Optional[list[str]]
    assertions: Assertions

class TestSuite(YamlModel):
    tests: dict[str, Test]
