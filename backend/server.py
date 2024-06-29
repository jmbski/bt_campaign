import json

from flask import Flask, request, Response, g
from flask_cors import CORS

from modules.data_utils import clean_params
from packages.sql import QueryObject, entities, ENTITY_MAP

from warskald import utils, req_utils, AttrDict, EnvironmentProps

APP_NAME = 'bt_campaign_mgr'
ENV_PROPS = EnvironmentProps()
APP_PROPS = ENV_PROPS.get(APP_NAME)

app = Flask(__name__)

CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.route('/api/v1/status', methods=['GET'])
def get_status():
    return Response('{"status": "ok"}', status=200, mimetype='application/json')

@app.route('/api/v1/get_mul', methods=['GET', 'POST'])
def get_mul():
    query = QueryObject(entities.MulData)
    
    params = req_utils.parse_request_data()
    
    loose = params.pop('loose', False)
    
    response = query.get_multiple(loose=loose, **params)
    
    response = [item.to_json() for item in response] if response else []
    
    query.close_session()
    
    return Response(json.dumps(response), status=200, mimetype='application/json')

@app.route('/api/v1/get_mtf', methods=['GET', 'POST'])
def get_mtf():
    query = QueryObject(entities.MtfData)
    
    params = req_utils.parse_request_data()
    
    response = query.get_multiple(**params)
    
    response = [item.to_json() for item in response] if response else []
    
    query.close_session()
    
    return Response(json.dumps(response), status=200, mimetype='application/json')

@app.route('/api/v1/data', methods=['POST'])
def perform_data_query():
    params = AttrDict(request.get_json())
    
    if(not params):
        return Response('{"error": "No data provided"}', status=400, mimetype='application/json')
    
    if(not params.entity):
        return Response('{"error": "No entity provided"}', status=400, mimetype='application/json')
    
    entity = ENTITY_MAP.get(params.entity)
    
    if(not entity):
        return Response(f'{{"error": "Invalid entity \'{entity}\' provided"}}', status=400, mimetype='application/json')
    
    action = params.action
    
    if(not action):
        return Response('{"error": "No action provided"}', status=400, mimetype='application/json')
    
    if(action not in ['get', 'get_multiple', 'save', 'delete']):
        return Response(f'{{"error": "Invalid action \'{action}\' provided"}}', status=400, mimetype='application/json')
    
    query = QueryObject(entity)
    
    funct = getattr(query, action)
    
    query_data = params.get('data', {})
    
    if(action == 'get_multiple'):
        loose = query_data.pop('loose', False)
        response = funct(loose=loose, **query_data)
    else:
        response = funct(**query_data)
        
    if(isinstance(response, list)):
        response = [item.to_json() for item in response]
    elif(isinstance(response, entities.Base)):
        response = response.to_json()
    
    response_content = {
        'status': 'ok',
        'data': response
    }
    
    return Response(json.dumps(response_content), status=200, mimetype='application/json')
        
    
    
    