#!/bin/bash

docker run --name tfc-profile -p 8083:8083 -e DB_HOST=mongo --link mongo "$@" tfc/tfc-profile