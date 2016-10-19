echo 'starting installation process' >> /var/log/sga-npcomplete-forecast-decision-install.log
cd '/home/ec2-user/ForecastDecision'

echo 'Activating virtualenv for ForecastDecision Microservice' >> /var/log/sga-npcomplete-forecast-decision-install.log
pip install virtualenv >> /var/log/sga-npcomplete-forecast-decision-install.log
virtualenv venv >> /var/log/sga-npcomplete-forecast-decision-install.log
. venv/bin/activate >> /var/log/sga-npcomplete-forecast-decision-install.log
pip install requests
pip install Flask >> /var/log/sga-npcomplete-forecast-decision-install.log
#echo 'Running Flask Server' >> /var/log/sga-npcomplete-flask-install.log
export FLASK_APP=forecast_decision.py
flask run --host=0.0.0.0 --port=65000 >> /var/log/sga-npcomplete-forecast-decision-server.log 2>&1 &
