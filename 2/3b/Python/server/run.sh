#!/bin/bash
docker run -it --init --rm --network-alias z35_python_server_2_3 --hostname z35_python_server_2_3 --network z35_network --name z35_python_server_2_3 z35_python_server_2_3 "$@"

