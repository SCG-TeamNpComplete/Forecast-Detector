echo 'starting installation process' >> /var/log/sga-npcomplete-forecast-decision-install.log
cd '/home/ec2-user/docker'
sudo docker login -e="kedar.gn20@gmail.com" -u="kedargn" -p="npcomplete"   #TODO : hide password
sudo docker pull kedargn/forecastdetector

sudo docker ps -a | grep 'forecastdetector1' | awk '{print $1}' | xargs --no-run-if-empty docker stop
sudo docker ps -a | grep 'forecastdetector1' | awk '{print $1}' | xargs --no-run-if-empty docker rm
sudo docker run -d -p 65000:65000 --name forecastdetector1 $(sudo docker images | grep kedargn/forecastdetector | awk '{print $3}') >> ./log.txt


sleep 2


sudo docker ps -a | grep 'forecastdetector2' | awk '{print $1}' | xargs --no-run-if-empty docker stop
sudo docker ps -a | grep 'forecastdetector2' | awk '{print $1}' | xargs --no-run-if-empty docker rm
sudo docker run -d -p 65001:65001 --name forecastdetector2 $(sudo docker images | grep kedargn/forecastdetector | awk '{print $3}') >> ./log.txt
