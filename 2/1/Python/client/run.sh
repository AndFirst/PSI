#!/bin/bash
docker run -it --init --rm --network-alias z35_python_client_2_1 --hostname z35_python_client_2_1 --network z35_network --name z35_python_client_2_1 z35_python_client_2_1 "$@"

