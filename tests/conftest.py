import pytest
import requests_mock


@pytest.fixture
def m():
    mocker = requests_mock.mock()
    mocker.start()
    yield mocker
    mocker.stop()
