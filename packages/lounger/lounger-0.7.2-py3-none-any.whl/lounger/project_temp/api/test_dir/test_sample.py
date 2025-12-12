"""
requests test sample

run test：
> pytest -vs test_api.py
"""
from pytest_req.assertions import expect

from lounger.commons.load_config import base_url


def test_getting_resource(get):
    """
    Getting a resource
    """
    s = get(f"{base_url()}/posts/1")
    expect(s).to_be_ok()
    expect(s).to_have_path_value("userId", 1)


def test_creating_resource(post):
    """
    Creating a resource
    """
    data = {"title": "foo", "body": "bar", "userId": 1}
    s = post(f'{base_url()}/posts', json=data)
    expect(s).to_have_status_code(201)
    json_str = {
        "title": "foo",
        "body": "bar",
        "userId": 1,
        "id": 101
    }
    expect(s).to_have_json_matching(json_str)
