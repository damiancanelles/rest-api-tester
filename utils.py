import schemas

def test_request(request: schemas.Request):
    import requests
    import json
    passed = False

    """
        Here we create the params and header objects from the list of key values that the client provide.
    """

    headers_object = {}
    params_object = {}
    for header in request.body['headers']:
        headers_object[header['key']] = header['value']
    for param in request.body['params']:
        params_object[param['key']] = param['value']

    """
        Here we identify wich method is define in the request and execute the correct function
    """

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

    """
        Here extract the data from the response object (for now we only save json responses).
    """

    response_data = test.content
    status = test.status_code
    try:
        response_data_json = json.loads(response_data)
    except:
        response_data_json = {}

    """
        Here perform the seach in the response of the search params.
    """

    for search_param in request.seach_params:
        if search_param['key'] == "status":
            if int(search_param['value']) == status:
                passed = True
            else:
                passed = False
        elif search_param['key'] == "all":
            if not search_param['value'] in response_data:
                passed = True
            else:
                passed = False
        elif search_param['key'] == "prop":
            if not search_param['key'] in response_data_json:
                if response_data_json[search_param['key']] == search_param['value']:
                    passed = True
                else:
                    passed = False
            else:
                passed = False

        return passed, response_data_json