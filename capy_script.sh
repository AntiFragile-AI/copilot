#!/bin/bash

# Instruction of usage: https://docs.google.com/document/d/1vPLq70UAm6jgnXZ8uLxbbpkLtUeupRpHTZFdjaOBrCI/edit
# example: ./capy --command "tf plan" --option explain | cost | question
# test option: ./capy --command "test" --option cost 

# Function to display usage information
display_usage() {
    echo "Usage: capy --command <command_value> --option <option_value>"
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
            command_to_execute="$2"
            shift 2
            ;;
        --option)
            capy_command="$2"
            shift 2
            ;;
        *)
            display_usage
            ;;
    esac
done

# Validate if both command and option are provided
if [ -z "$command_to_execute" ] || [ -z "$capy_command" ]; then
    display_usage
fi

# Default output file if not provided
if [ -z "$output_file" ]; then
    output_file="output.txt"
fi

# Display the extracted input values
echo "system command: $command_to_execute, capy command: $capy_command"

# Execute command and save it to output file
if [ "$command_to_execute" == "test" ]; then
    cat "test_input.txt" >"$output_file"
    command_to_execute="tf plan"
else
    eval "$command_to_execute" > "$output_file"
fi
echo "system command results saved to: $output_file"

# Get system command output
sys_command_output=$(cat "$output_file")
echo "system command output: $sys_command_output"

# Execute capy client
echo "Execute capy command: python capy_api.py $command_to_execute <sys_command_output> $capy_command"
python cli/capy_api.py "$command_to_execute" "$sys_command_output" "$capy_command"

# Delete the output file
rm "$output_file"
echo "Deleted $output_file"


