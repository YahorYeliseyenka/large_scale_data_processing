#!/usr/bin/env bash

path=$1
name=test

if [ ! -z "$path" ]
then
    timestamp="$(date +"%s")"

	docker build -t numguy/$name $path
    docker tag $name numguy/$name:$timestamp
	docker push numguy/$name
fi

# docker run -d -p 5000:5000 temp
# curl http://localhost:5000

# docker ps -a
# docker rm @@@
# docker rmi @@@ --force