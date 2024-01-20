#!/bin/bash

# Specify coordinator host and port
coordinator_host="127.0.0.1"
coordinator_port=4999

# Specify server ports and ids
server_ports=(5000 5001)
server_ids=(1 2)

# Function to terminate processes using a specified port
terminate_process_by_port() {
    local port=$1
    local pid=$(lsof -t -i:$port)

    if [ -n "$pid" ]; then
        echo "Terminating process using port $port (PID: $pid)"
        kill $pid
        sleep 1  # Wait for the process to terminate
    fi
}

# Terminate processes using coordinator and server ports
terminate_process_by_port $coordinator_port
for port in "${server_ports[@]}"; do
    terminate_process_by_port $port
done

# Launch the coordinator
# python coordinator.py --host $coordinator_host --port 2137 &

# Wait for a short time to ensure the coordinator is running before launching servers
sleep 2
# Launch three server instances with different host and port combinations
cd hls-server &
for i in "${!server_ports[@]}"; do
    python hls-server/server.py --coordinator_host $coordinator_host --coordinator_port $coordinator_port --server_host "127.0.0.1" --server_port ${server_ports[i]} --server_id ${server_ids[i]} &
done
# Wait for all background processes to finish
wait
