#!/bin/bash
docker run -it --init --rm --network-alias z35_c_server_2_3 --hostname z35_c_server_2_3 --network z35_networkv6 --name z35_c_server_2_3 z35_c_server_2_3 "$@"

