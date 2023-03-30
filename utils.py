import schemas

def test_request(request: schemas.Request):
    import requests
    import json
    passed = True

    headers_object = {}
    params_object = {}
    for header in request.body['headers']:
        headers_object[header['key']] = header['value']
    for param in request.body['params']:
        params_object[param['key']] = param['value']

    if request.body['method'] == 'GET':
        test = requests.get(request.url, params=params_object, headers=headers_object)
    elif request.body['method'] == 'POST':
        test = requests.post(request.url, data=request.body['body'], params=params_object, headers=headers_object)
    elif request.body['method'] == 'PUT':
        test = requests.put(request.url, data=request.body['body'], params=params_object, headers=headers_object)
    elif request.body['method'] == 'PATCH':
        test = requests.patch(request.url, data=request.body['body'], params=params_object, headers=headers_object)
    elif request.body['method'] == 'DELETE':
        test = requests.delete(request.url, data=request.body['body'], params=params_object, headers=headers_object)

    response_data = test.text
    response_headers = test.headers
    status = test.status_code
    try:
        response_data_json = json.loads(test.content)
    except:
        response_data_json = {}

    for search_param in json.loads(request.search_params):

        if search_param['key'] == "status" and search_param['relation'] == "igual":
            if not int(search_param['value']) == status:
                passed = False

        elif search_param['key'] == "body" and search_param['relation'] == "igual":
            if not search_param['value'] == response_data:
                passed = False
        elif search_param['key'] == "body" and search_param['relation'] == "contiene":
            if not search_param['value'] in response_data:
                passed = False

        elif search_param['key'] == "headers" and search_param['relation'] == "igual":
            if not search_param['value'] == response_headers:
                passed = False
        elif search_param['key'] == "headers" and search_param['relation'] == "contiene":
            if not search_param['value'] in response_headers:
                passed = False

    return passed, response_data_json