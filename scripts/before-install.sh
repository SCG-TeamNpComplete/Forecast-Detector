sudo docker ps -a | grep 'forecastdetector' | awk '{print $1}' | xargs --no-run-if-empty docker stop
sudo docker ps -a | grep 'forecastdetector' | awk '{print $1}' | xargs --no-run-if-empty docker rm