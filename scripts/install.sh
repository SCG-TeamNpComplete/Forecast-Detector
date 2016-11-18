#!/bin/bash

echo 'starting installation process' >> /var/log/sga-npcomplete-forecast-decision-install.log
cd '/home/ec2-user/docker'
sudo docker login -u="kedargn" -p="npcomplete"   #TODO : hide password
sudo docker pull kedargn/forecastdetector

no_of_instances=1     #change this to set the number of instances
current_instance=1
port=65000
while [ $current_instance -le $no_of_instances ]
do
	#echo "$(sudo docker ps -a | grep "forecastdetector$current_instance" | awk '{print $1}')"
	if [ "$(sudo docker ps -a | grep "forecastdetector$current_instance" | awk '{print $1}')" != "" ]; then
		sudo docker ps -a | grep "forecastdetector$current_instance" | awk '{print $1}' | xargs --no-run-if-empty sudo docker stop
		sudo docker ps -a | grep "forecastdetector$current_instance" | awk '{print $1}' | xargs --no-run-if-empty sudo docker rm
	fi
	#echo "$port:$port"
	sudo docker run -d -p "$port:$port" --name "forecastdetector$current_instance" $(sudo docker images | grep kedargn/forecastdetector | awk '{print $3}')
	echo "forecastdetector$current_instance instance"
	current_instance=$((current_instance+1))
	port=$((port+1))
	sleep 1
done
