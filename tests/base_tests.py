import pytest
from pytest_mock import MockerFixture

@pytest.fixture()
def mocker():
    mocker = MockerFixture({})
    yield mocker
    mocker.stopall()
    mocker.resetall()