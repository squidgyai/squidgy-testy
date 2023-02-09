from pydantic import BaseModel
from pydantic_yaml import YamlModel, YamlModelMixin
from typing import Optional, Union, Literal

class SimilarToAssertionData(BaseModel):
    value: str
    threshold: float

class Assertion(BaseModel):
    pass

class StartsWithAssertion(YamlModelMixin, Assertion):
    startsWith: str

class EqualToAssertion(YamlModelMixin, Assertion):
    equalTo: str

class SimilarToAssertion(YamlModelMixin, Assertion):
    similarTo: SimilarToAssertionData

class Test(YamlModelMixin, BaseModel):
    prompt_file: str
    prompt_append: Optional[str]
    params: Optional[dict[str, str]]
    stop: Optional[list[str]]
    assertions: list[Union[EqualToAssertion, SimilarToAssertion, StartsWithAssertion]]

class TestSuite(YamlModel):
    stop: Optional[list[str]]
    tests: dict[str, Test]
