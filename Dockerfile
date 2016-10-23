FROM ubuntu:12.04

RUN apt-get update
RUN apt-get install -y python-dev python-pip
 
ADD ./ForecastDecision/ ./
RUN pip install virtualenv
RUN virtualenv venv
RUN . venv/bin/activate
RUN pip install requests
RUN pip install flask
RUN pip install nose 
ENV FLASK_APP=forecast_decision.py
EXPOSE 65000
CMD flask run --host=0.0.0.0 --port=65000