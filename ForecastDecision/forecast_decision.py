from flask import Flask, jsonify, request
import httplib
import requests
import ast, random
import json

app = Flask(__name__)

@app.route('/forecast_decision/json', methods=['POST'])
def forecast_decision():
  service_id = 5

  response_json = {}
  random_no = int(random.uniform(0, 100))

  result = ast.literal_eval(request.data)
  result["serviceId"] = "ForecastDecision"

  headers = {'Content-Type': 'application/json'}

  
  if(random_no%2==0):
    parsed_json = {'result':'yes'}
    connection = requests.post("http://ec2-54-69-92-137.us-west-2.compute.amazonaws.com:64000/forecast/json", data=json.dumps(result));
    print connection
    response_json = ast.literal_eval(connection.text)
    result["text"] = "Forecast Initiated"	  
    r = requests.post("http://ec2-54-69-92-137.us-west-2.compute.amazonaws.com:8080/SG_MICROSERVICE_REGISTRY/gateway/message/saveData", data=json.dumps(result), headers=headers)
    print r.status_code
    return jsonify(response_json)
  else:
    result["text"] = "Forecast Not Initiated"
    r = requests.post("http://ec2-54-69-92-137.us-west-2.compute.amazonaws.com:8080/SG_MICROSERVICE_REGISTRY/gateway/message/saveData", data=json.dumps(result), headers=headers)
    return jsonify({'result':'no'})
