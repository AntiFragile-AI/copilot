#!/bin/bash

# Function to handle HTTP requests
send_request() {
    # Placeholder for sending HTTP requests (e.g., using curl)
    # This function needs to be implemented based on your system's capabilities
    echo "Sending HTTP request to $1"
    # Example: curl -X POST -H "Content-Type: application/json" -d "$2" "$1"
}

# Function to handle error responses
handle_error() {
    echo "Error: $1"
    exit 1
}

# Function to execute tf plan and interact with Capy API
execute_tf_plan() {
    local endpoint="$1"
    local option="$2"
    local question="$3"

    # Execute terraform plan
    tf_plan_output=$(terraform plan)

    # Define request token
    request_token=$(date +%s%N)

    # Prepare common request body
    request_body_common='{
        "request_token": "'"$request_token"'",
        "command": "tf plan",
        "command_result": '"$tf_plan_output"',
        "repo_content": { … }
    }'

    # Handle different endpoint scenarios
    case "$endpoint" in
        "explain" | "cost")
            request_body="$request_body_common, \"option\": \"$option\"}"
            ;;
        "question")
            request_body="$request_body_common, \"option\": \"$option\", \"option_content\": \"$question\"}"
            ;;
        *)
            handle_error "Invalid endpoint: $endpoint"
            ;;
    esac

    # Send HTTP request
    response=$(send_request "https://capy/api" "$request_body")

    # Parse response
    change_json=$(echo "$response" | jq -r '.change_json')
    explain_json=$(echo "$response" | jq -r '.explain_json')

    # Check for errors
    if [ -z "$change_json" ] || [ -z "$explain_json" ]; then
        handle_error "Invalid response from Capy API"
    fi

    # Print results
    echo "Change JSON: $change_json"
    echo "Explain JSON: $explain_json"
}


# Parse command-line arguments
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <endpoint> [<option>] [<question>]"
    exit 1
fi

# Assign arguments to variables
endpoint="$1"
option="$2"
question="$3"

# Execute the appropriate function based on the provided endpoint
case "$endpoint" in
    "explain" | "cost" | "question")
        execute_tf_plan "$endpoint" "$option" "$question"
        ;;
    *)
        handle_error "Invalid endpoint: $endpoint"
        ;;
esac

exit 0