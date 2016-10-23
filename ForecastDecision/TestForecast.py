import unittest
from forecast_decision import app
import json
import ast
 
class TestForecast(unittest.TestCase):
	def test_forecast(self):
		self.test_app = app.test_client()
		data = {'userId': 'user_name', 'reqId': 'ForecastDecision'}
		response = self.test_app.post('/forecast_decision/json', data="{'userId': 'user_name', 'reqId': 'ForecastDecision'}")
		self.assertEquals(response.status, "200 OK")

	def test_forecast_wronginput(self):
		self.test_app = app.test_client()
		data = {'userId': 'user_name', 'reqId': 'ForecastDecision'}
		response = self.test_app.post('/forecast_decision', data="{ 'reqId': 'ForecastDecision'}")
		self.assertNotEquals(response.status, "200 OK")

