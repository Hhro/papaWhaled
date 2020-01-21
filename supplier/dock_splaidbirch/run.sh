#!/bin/bash
docker kill cappit_splaidbirch 2>/dev/null
docker rm cappit_splaidbirch 2>/dev/null
docker run --privileged -p 31000:31000 -dit --name cappit_splaidbirch splaidbirch