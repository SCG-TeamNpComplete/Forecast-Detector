echo 'starting installation process' >> /var/log/sga-npcomplete-forecast-decision-install.log
cd '/home/ec2-user/docker'
sudo docker login -e="kedar.gn20@gmail.com" -u="kedargn" -p="npcomplete"   #TODO : hide password
sudo docker pull kedargn/forecastdetector
sudo docker run -d -p 65000:65000 --name forecastdetector $(sudo docker images | grep kedargn/forecastdetector | awk '{print $3}') >> ./log.txt
