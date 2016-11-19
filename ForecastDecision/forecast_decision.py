from flask import Flask, jsonify, request
import httplib
import requests
import ast, random
import json
from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.exceptions import KazooException
import logging
import uuid
import calendar, datetime, time
from datetime import datetime

app = Flask(__name__)
ec2Ip = requests.get("http://checkip.amazonaws.com/").text.split("\n")[0]
#ec2Ip = "127.0.0.1"
@app.route('/forecast_decision/json', methods=['POST'])
def forecast_decision():
  service_id = 5
  response_json = {}
  random_no = int(random.uniform(0, 100))
  result = ast.literal_eval(request.data)
  result["serviceId"] = "ForecastDecision"
  headers = {'Content-Type': 'application/json'}

  forecastUrl = requests.get("http://ec2-35-160-137-157.us-west-2.compute.amazonaws.com:11000/servicegateway/forecast")

  if(random_no%2==0):
    parsed_json = {'result':'yes'}
    connection = requests.post(forecastUrl+"/forecast/json", data=json.dumps(result));
    print connection
    response_json = ast.literal_eval(connection.text)
    result["text"] = "Forecast Initiated"   
    r = requests.post("http://ec2-35-160-137-157.us-west-2.compute.amazonaws.com:8080/SG_MICROSERVICE_REGISTRY/gateway/message/saveData", data=json.dumps(result), headers=headers)
    print r.status_code
    return jsonify(response_json)
  else:
    result["text"] = "Forecast Not Initiated"
    r = requests.post("http://ec2-35-160-137-157.us-west-2.compute.amazonaws.com:8080/SG_MICROSERVICE_REGISTRY/gateway/message/saveData", data=json.dumps(result), headers=headers)
    return jsonify({'result':'no'})


def createConnection():
  global ec2Ip
  id = str(uuid.uuid4())
  hostIp = ec2Ip+":2181"
  zk = KazooClient(hosts=hostIp)
  zk.start()
  zk.add_listener(my_listener)
  path = "http://"+ec2Ip+":65000/forecast_decision/json"
  print "tryin to create node"
  #zk.create("/load-balancing-example/forecast",hostIp,ephemeral=True,makepath=True)
  zk.create("/load-balancing-example/forecastDetector/"+id, json.dumps({'name': 'forecastDetector', 'id': id, 'address': ec2Ip, 'port': 65000,'sslPort': None, 'payload': None,'registrationTimeUTC': (datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds(),'serviceType': 'DYNAMIC',"uriSpec": {"parts": [{"value": path, "variable": False}]}}, ensure_ascii=True).encode(),ephemeral=True,makepath=True)

def tearDown():
  zk.stop()

def my_listener(state):
  global ec2Ip
  if state == KazooState.LOST:
    # Register somewhere that the session was lost
    hostIp = ec2Ip+":2181"
    zk = KazooClient(hosts=hostIp)
    zk.start()

  elif state == KazooState.SUSPENDED:
    # Handle being disconnected from Zookeeper
    print "connection suspended"
  else:
    # Handle being connected/reconnected to Zookeeper
    print "connection error"

#@app.before_first_request
def connect():
  try:
    createConnection()
  except KazooException as e:
    print e.__doc__
    print "error "+e.message
  logging.basicConfig()

connect()

