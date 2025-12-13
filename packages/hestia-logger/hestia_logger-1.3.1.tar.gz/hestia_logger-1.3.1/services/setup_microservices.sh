#!/bin/bash
set -e  # Exit script if any command fails

NETWORK_NAME="elastic-net"
SUBNET="172.18.0.0/16"
GATEWAY="172.18.0.1"

check_overlap() {
    local subnet1=$1
    local subnet2=$2
    python - <<EOF
from ipaddress import ip_network
net1 = ip_network("$subnet1")
net2 = ip_network("$subnet2")
print(net1.overlaps(net2))
EOF
}

network_exists=$(docker network ls -q -f name="$NETWORK_NAME")
if [ -n "$network_exists" ]; then
    echo "🔍 Checking if '$NETWORK_NAME' has attached resources..."
    attached_containers=$(docker network inspect "$NETWORK_NAME" --format '{{range .Containers}}{{.Name}} {{end}}')
    if [ -z "$attached_containers" ]; then
        echo "🗑️ No containers attached to '$NETWORK_NAME'. Removing it..."
        docker network rm "$NETWORK_NAME"
        echo "✅ Network '$NETWORK_NAME' removed."
    else
        echo "⚠️ Network '$NETWORK_NAME' has attached containers: $attached_containers. Skipping removal."
    fi
fi

conflict_found=0
declare -A conflicts

if [ -z "$(docker network ls -q -f name="$NETWORK_NAME")" ]; then
    echo "🔍 Scanning existing Docker networks for subnet conflicts with $SUBNET..."
    existing_networks=$(docker network ls -q)
    for net in $existing_networks; do
        net_name=$(docker network inspect "$net" --format '{{.Name}}')
        subnets=$(docker network inspect "$net" --format '{{range .IPAM.Config}}{{.Subnet}} {{end}}')
        for existing_subnet in $subnets; do
            if [ -n "$existing_subnet" ]; then
                overlap=$(check_overlap "$SUBNET" "$existing_subnet")
                if [ "$overlap" == "True" ]; then
                    echo "⚠️ Conflict detected: Desired subnet $SUBNET overlaps with network '$net_name' (subnet: $existing_subnet)"
                    conflict_found=1
                    attached_containers=$(docker network inspect "$net" --format '{{range .Containers}}{{.Name}} (ID: {{.Name}}) {{end}}')
                    if [ -z "$attached_containers" ]; then
                        attached_containers="No containers attached."
                    fi
                    conflicts["$net_name"]="$existing_subnet | $attached_containers"
                fi
            fi
        done
    done

    if [ $conflict_found -eq 1 ]; then
        echo -e "\n❌ Failed to create network '$NETWORK_NAME' due to subnet overlaps."
        echo -e "\nConflicting network details:"
        for net in "${!conflicts[@]}"; do
            IFS='|' read -r conf_subnet conf_containers <<< "${conflicts[$net]}"
            echo "-------------------------------------------"
            echo "Network: $net"
            echo "Subnet: $conf_subnet"
            echo "Attached containers: $conf_containers"
            echo "-------------------------------------------"
        done
        echo -e "\nRecommendations:"
        echo "  • Choose a different address space (e.g., SUBNET=172.19.0.0/16) OR"
        echo "  • Remove conflicting networks if unused:"
        for net in "${!conflicts[@]}"; do
            echo "    docker network rm $net"
        done
        exit 1
    fi

    echo "🌐 Creating external network '$NETWORK_NAME' with subnet '$SUBNET' and gateway '$GATEWAY'..."
    docker network create --driver bridge --subnet "$SUBNET" --gateway "$GATEWAY" "$NETWORK_NAME"
    echo "✅ Network '$NETWORK_NAME' created successfully."
else
    echo "✅ Network '$NETWORK_NAME' already exists and will be reused."
fi

check_and_create_dir() {
    local DIR="$1"
    if [ ! -d "$DIR" ]; then
        echo "📁 Creating directory: $DIR"
        mkdir -p "$DIR"
        chmod -R 777 "$DIR"  # Ensure writability for testing
    else
        echo "✅ Directory exists: $DIR"
    fi
}

check_and_create_dir "./host_volumes/hestia-logs"
check_and_create_dir "./host_volumes/esdata01"
check_and_create_dir "./host_volumes/esdata02"
check_and_create_dir "./host_volumes/grafana-data"

echo "🎉 Directory setup complete for testing!"
echo "  - Hestia Logs: ./host_volumes/hestia-logs"
echo "  - Elasticsearch Data (es01): ./host_volumes/esdata01"
echo "  - Elasticsearch Data (es02): ./host_volumes/esdata02"
echo "  - Grafana Data: ./host_volumes/grafana-data"

if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found in current directory!"
    exit 1
fi

if [ ! -f "fluentbit/fluent-bit.conf" ]; then
    echo "❌ fluent-bit.conf not found in services/fluentbit/!"
    exit 1
fi

if [ ! -f "log-generator/Dockerfile" ]; then
    echo "❌ Dockerfile not found in services/log-generator/!"
    exit 1
fi

if [ ! -f "fluentbit/Dockerfile" ]; then
    echo "❌ Dockerfile not found in services/fluentbit/!"
    exit 1
fi

if [ ! -f "log-generator/generate_logs.py" ]; then
    echo "❌ generate_logs.py not found in services/log-generator/!"
    exit 1
fi

if [ ! -f "grafana/provisioning/datasources/elasticsearch.yml" ]; then
    echo "❌ Grafana datasource config not found in services/grafana/provisioning/datasources/!"
    exit 1
fi

echo "🚀 Starting Docker Compose..."
if ! docker compose up --build -d; then
    echo "❌ Failed to start Docker Compose!"
    exit 1
fi

echo "🏁 To stop the microservices, run:"
echo "   docker compose down"