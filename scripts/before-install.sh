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

install_dir="/usr/local"
dir="/usr/local/zookeeper-3.4.8"
if [ ! -d "$dir" ] ; then
	cd "$install_dir"
	wget http://www-us.apache.org/dist/zookeeper/zookeeper-3.4.8/zookeeper-3.4.8.tar.gz
	tar xzf zookeeper-3.4.8.tar.gz
	rm zookeeper-3.4.8.tar.gz
	cd "$dir/conf"
	touch zoo.cfg
	echo "tickTime=2000" > zoo.cfg
	echo "dataDir=/var/lib/zookeeper" >> zoo.cfg
	echo "clientPort=2181" >> zoo.cfg
fi

cd "$dir/bin"
./zkServer.sh stop
./zkServer.sh start
