import json

import pytest
import handler

def test_get_all_orders():
    response=handler.get_all_orders(event=None,context=None)
    assert response['statusCode']==200

def test_create_service():
    event={"body":"{\"name\":  \"test_service\",\"price\":  12.5}"}
    response=handler.create_service(event,context=None)
    assert response['statusCode']==200

def test_create_order():
    event={"body":"{\"services\":  [2,7],\"description\":  \"test order\"}"}
    response=handler.create_order(event,context=None)
    assert response['statusCode']==200

def test_get_order_details():
    event={"pathParameters":{"id":4}}
    response=handler.get_order_details(event,context=None)
    assert response['statusCode']==200

def test_update_order():
    event={"pathParameters":{"id":4},"body":"{\"services\": [2,7]}"}
    response=handler.update_order(event,context=None)
    assert response['statusCode']==200

def test_delete_order():
    event = {"body": "{\"services\":  [2,7],\"description\":  \"test order\"}"}
    response=handler.create_order(event,context=None)
    order_id=json.loads(response['body'])['order_id']
    event={"pathParameters":{"id":order_id}}
    response=handler.delete_order(event,context=None)
    assert response['statusCode']==200
