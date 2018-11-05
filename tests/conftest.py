# -*- coding: utf-8 -*-
import pytest
import requests_mock


@pytest.fixture(scope='function')
def m():
    mocker = requests_mock.mock()
    mocker.head('http://mock.com/favicon.ico', text='404', status_code=404)

    mocker.start()
    yield mocker
    mocker.stop()
