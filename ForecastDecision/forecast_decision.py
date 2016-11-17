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

  forecastUrl = requests.get("http://ec2-35-160-137-157.us-west-2.compute.amazonaws.com:9999/TeamNpComplete/Forecast")

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
  zk = KazooClient(hosts='127.0.0.1:2181')
  zk.start()
  zk.add_listener(my_listener)
  print "tryin to create node"
  if zk.exists("/load-balancing-example"):
    print "----> node already exists"
  else:
    #Change this to refect dynamic ip and path
    zk.create("/my/favorite/node3",b"http://12.22.33.22:1209",ephemeral=True,makepath=True)

def tearDown():
  zk.stop()

def my_listener(state):
  if state == KazooState.LOST:
    # Register somewhere that the session was lost
    zk = KazooClient(hosts='127.0.0.1:2181')
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
