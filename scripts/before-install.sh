#!/bin/bash

sudo yum install -y docker-io
sudo service docker start

dangling_images="$(sudo docker images -f "dangling=true" -q)"


if [ "$dangling_images" == "" ] ; then
        echo "no images"
else
		sudo docker rmi -f $(sudo docker images -f "dangling=true" -q)
    echo "images present"
fi