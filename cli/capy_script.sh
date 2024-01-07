#!/bin/bash

# Function to display usage information
display_usage() {
    echo "Usage: $0 --command <command_value> --option <option_value>"
    exit 1
}

# Check for the correct number of arguments
if [ "$#" -ne 4 ]; then
    display_usage
fi

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
    case "$1" in
        --command)
            command_value="$2"
            shift 2
            ;;
        --option)
            option_value="$2"
            shift 2
            ;;
        *)
            display_usage
            ;;
    esac
done

# Validate if both command and option are provided
if [ -z "$command_value" ] || [ -z "$option_value" ]; then
    display_usage
fi

# Display the extracted values
echo "Command: $command_value"
echo "Option: $option_value"