#!/bin/bash
docker kill cappit_splaidbirch 2>/dev/null
docker rm cappit_splaidbirch 2>/dev/null
docker rmi splaidbirch 2>/dev/null