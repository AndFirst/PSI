#!/bin/bash
docker run -it --init --rm --network-alias z35_python_client_1_1 --hostname z35_python_client_1_1 --network z35_network --name z35_python_client_1_1 z35_python_client_1_1 "$@"