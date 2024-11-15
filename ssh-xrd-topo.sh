#!/bin/bash

# Configuration
readonly USERNAME="cisco"
readonly PASSWORD="cisco123"
readonly DOCKER_IMAGE="ios-xr/xrd-control-plane:24.2.2"
readonly SSH_OPTS="-o StrictHostKeyChecking=no -o ConnectTimeout=10"

# Error handling
set -euo pipefail
trap 'echo "Error: Script failed on line $LINENO"' ERR

# Functions
get_containers() {
    docker ps --format '{{.ID}} {{.Names}} {{.Image}}' | grep "$DOCKER_IMAGE" || {
        echo "No running XRd containers found."
        exit 1
    }
}

sort_containers() {
    local unsorted_file="$1"

    {
        # Sort LF containers by numeric suffix
        grep "LF" "$unsorted_file" | sort -t '-' -k4.3,4n
        # Sort SP containers by numeric suffix
        grep "SP" "$unsorted_file" | sort -t '-' -k4.3,4n
        # Sort SS containers by numeric suffix
        grep "SS" "$unsorted_file" | sort -t '-' -k4.3,4n
    } || {
        echo "Error sorting containers. Ensure container names follow expected conventions."
        exit 1
    }
}

display_containers() {
    local -n containers=$1
    echo -e "\nCisco XRd Containers (sorted LF -> SP -> SS):"
    echo "----------------------------------------"

    for i in "${!containers[@]}"; do
        local name image
        name=$(echo "${containers[i]}" | awk '{print $2}')
        image=$(echo "${containers[i]}" | awk '{print $3}')
        printf "%2d. %-30s [%s]\n" "$((i+1))" "$name" "$image"
    done
    echo "----------------------------------------"
}

get_container_ip() {
    local container_id=$1
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$container_id" || {
        echo "Failed to get IP address for container $container_id"
        return 1
    }
}

ssh_to_container() {
    local container_ip=$1
    echo "Connecting to $container_ip..."

    sshpass -p "$PASSWORD" ssh $SSH_OPTS "$USERNAME@$container_ip"
    return 0  # Always return success to continue script
}

# Main script
main() {
    while true; do
        # Create temporary files for sorting
        local unsorted_file=$(mktemp)

        # Get containers and store in temporary file
        get_containers > "$unsorted_file"

        # Sort containers in the correct order (LF -> SP -> SS)
        mapfile -t container_array < <(sort_containers "$unsorted_file")

        # Clean up
        rm "$unsorted_file"

        # Display containers
        display_containers container_array

        # Get user input
        echo -e "\nEnter the number of the container to SSH into (0 to exit):"
        read -r choice

        # Validate input
        if [[ ! "$choice" =~ ^[0-9]+$ ]]; then
            echo "Please enter a valid number"
            continue
        fi

        # Handle exit
        if [ "$choice" -eq 0 ]; then
            echo "Exiting..."
            exit 0
        fi

        # Validate selection
        if (( choice >= 1 && choice <= ${#container_array[@]} )); then
            local container_id container_name container_ip
            container_id=$(echo "${container_array[choice-1]}" | awk '{print $1}')
            container_name=$(echo "${container_array[choice-1]}" | awk '{print $2}')

            echo "Selected container: $container_name"

            # Get container IP and establish SSH connection
            if container_ip=$(get_container_ip "$container_id"); then
                ssh_to_container "$container_ip"
                echo -e "\nDisconnected from $container_name"
            fi
        else
            echo "Invalid selection. Please choose a number between 1 and ${#container_array[@]}"
        fi
    done
}

# Execute main function
main


