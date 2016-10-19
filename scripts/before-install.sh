echo 'killing existing flask process if any' >> /var/log/flask-before.log
ps -ef | grep ForecastDecision | grep -v grep | awk '{print $2}' | xargs kill >> /var/log/flask-before.log
sleep 5
