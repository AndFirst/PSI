#!/bin/bash
docker run -it --init --rm --network-alias z35_c_server_2_2 --hostname z35_c_server_2_2 --network z35_network --name z35_c_server_2_2 z35_c_server_2_2 "$@"

