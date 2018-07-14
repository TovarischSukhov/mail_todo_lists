# encoding: utf-8

from fact_extraction.network_utils import STATUSES
from fact_extraction.views import app
from tests.test_utils import DEFAULT_FACTS, assert_have_json

APP = app.test_client()


def test_api_no_header():
    response = APP.get('/srv/v1/facts/realty/all')
    assert response.status_code == STATUSES['HTTP_403_forbidden']
    content = response.json
    assert content.get("data", {}).get("error") == 'x-service header with your service name is required'
    assert content.get("success") is not True


def test_api_no_message():
    response = APP.get('/srv/v1/facts/realty/all',
                       headers={'x-service': 'bot.realty.test'},
                       )
    assert response.status_code == STATUSES['HTTP_400_bad_request']
    content = response.json
    assert content.get("success") is not True


def test_api_no_facts_extracted():
    response = APP.get('/srv/v1/facts/realty/all?message="hi"',
                       headers={'x-service': 'bot.realty.test'},
                       )
    assert response.status_code == STATUSES['HTTP_200_ok']
    content = response.json
    assert content.get("success") is True
    assert_have_json(content.get('data', {}).get('facts'), DEFAULT_FACTS)


def test_api_all_correct():
    response = APP.get('/srv/v1/facts/realty/all?message="hi"',
                       headers={'x-service': 'bot.realty.test'},
                       )
    assert response.status_code == STATUSES['HTTP_200_ok']
    content = response.json
    assert content.get("success") is True


def test__():
    message = 'для себя, хочется, чтобы это была трешка с балконом, желательно с раздельным туалетом. до 20 млн было бы отлично. Желательно рядом с метро'
    response = APP.get('/srv/v1/facts/realty/all?message="{}"'.format(message),
                       headers={'x-service': 'bot.realty.test'},
                       )
    print(response)
