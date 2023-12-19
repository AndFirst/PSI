#!/bin/bash
docker run -it --init --rm --network-alias z35_c_client_2_2 --hostname z35_c_client_2_2 --network z35_networkv6 --name z35_c_client_2_2 z35_c_client_2_2 "$@"

