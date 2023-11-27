import subprocess
import threading
import os
import re
import time
import difflib
import glob
import sys

from langchain.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate

from dataclasses import dataclass

@dataclass
class Args:
    debug: bool = "False"
    model: str = "llama2"

def reader_thread(pipe, func):
    "Read lines from a pipe and call a function for each line. Part of a multi-threaded subprocess reader."
    while True:
        line = pipe.readline()
        if line:
            func(line.decode('utf-8').strip())
        else:
            break

class Terraform():
    def __init__(self, args) -> None:
        self.debugVar = args.debug
        self.llm = ChatOllama(
            model=args.model
        )
    
    def debug(self, msg):
        "Print a debug message if the global debug flag is set."
        if self.debugVar:
            print('DEBUG:', msg)

    def error(self, msg):
        "Print an error message and exit."
        print('ERROR:', msg)
        sys.exit(1)

    def terraform_init(self):
        command = "terraform init"
        exit_code = self.run_command(command)
        return exit_code
    
    def run_command(self, command: str):
        "Run a shell command and return the exit code."
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Define a function to handle output
        def print_output(line):
            if self.debug:
                print("Subprocess Output:", line)
        
        # Define a function to handle errors
        def print_error(line):
            print("Subprocess Error:", line)
        
        # Create threads for reading stdout and stderr
        out_thread = threading.Thread(target=reader_thread, args=[process.stdout, print_output])
        err_thread = threading.Thread(target=reader_thread, args=[process.stderr, print_error])
        
        # Start threads
        out_thread.start()
        err_thread.start()
        
        # Wait for both threads to finish
        out_thread.join()
        err_thread.join()
        
        # Wait for the process to finish and get the exit code
        process.communicate()
        return process.returncode
    
    def terraform_validate(self):
        "Run terraform validate in the current directory. Return exit code."

        command = "terraform validate"
        exit_code = self.run_command(command) 
        return exit_code
    
    def get_completion_langchain(self, operation: str):
        # Curly braces in example TF code must be escaped by doubling them
        # so Langchain doesn't interpret them as placeholders.
        template_string = """
    You are a Terraform developer working on a Terraform project with multiple HCL files ending in ".tf".
    Your task is to perform the following operations on those files:
    {operation} 

    Do not make any other changes.
    Each input filename is delimited with BEGIN and END lines like this:
    ---BEGIN filename.tf---
    File contents
    ---END filename.tf---

    Output all project files after your changes, using the same format as the input files.

    Do not output anything other than the delimited files themselves.

    Example file list format:
    ---BEGIN filename1.tf---
    resource "random_pet" "pet1" {{
    length = 2
    }}
    ---END filename1.tf---

    ---BEGIN filename2.tf---
    resource "random_id" "server" {{
    byte_length = 8
    }}
    ---END filename2.tf---

    Input file list to process:
    {tf_files_str}
    """
        
        prompt_template = ChatPromptTemplate.from_template(template_string)
        # debug(prompt_template.messages[0].prompt)

        tf_files_str = self.encode_tf_files_to_delim_str()

        messages = prompt_template.format_messages(operation=operation, tf_files_str=tf_files_str)

        self.debug('Submitting prompt to OpenAI API')
        response = self.llm(messages)
        content = response.content

        trimmed_resp = content[content.find("---BEGIN"):] if "---BEGIN" in content else content

        self.debug('BEGIN get_completion_langchain() trimmed_resp:')
        self.debug(trimmed_resp)
        self.debug('END get_completion_langchain() trimmed_resp')

        return trimmed_resp

    def encode_tf_files_to_delim_str(self):
        "Encode all .tf files in the current directory into a single delimited string. Return string."
        tf_files = glob.glob('*.tf')
        output_string = ''
        
        for tf_file in tf_files:
            self.debug(f"Encoding {tf_file}")
            with open(tf_file, 'r') as file:
                content = file.read()
                output_string += f'---BEGIN {tf_file}---\n{content}\n---END {tf_file}---\n\n'
        
        return output_string
    
    def recreate_tf_files_from_delim_str(self, delimited_str):
        "Recreate all .tf files in a temp directory from a single delimited string. Returns output dir path."

        tmpdir = self.make_timestamp_tmp_dir()

        # Split the string into segments based on the custom delimiter
        segments = re.split(r'---BEGIN (.+?)---|---END .+?---', delimited_str)
        # debug('Segments before removing empties')
        # if g_debug:
        #     for segment in segments:
        #         debug(f"ORIG SEGMENT: {segment}")
        #         debug('END ORIG SEGMENT')
        
        # Remove None and empty string elements from the list
        # segments = [segment for segment in segments if segment]
        # filtered_segments = [item for item in segments if item not in [None, '', '\n', '\n\n']]
        filtered_segments = [item for item in segments if item not in [None, '', '\n', '\n\n']]
        # debug('Segments after removing empties')
        # if g_debug:
        #     for segment in filtered_segments:
        #         debug(f"FILTERED SEGMENT: {segment}")
        #         debug('END FILTERED SEGMENT')

        
        # Create files from the segments
        for i in range(0, len(filtered_segments), 2):
            try:
                filename = filtered_segments[i].strip()
                # debug('Filename: ' + filename)
                content = filtered_segments[i + 1]
                # debug('content: ' + content)
            except IndexError:
                self.debug('IndexError, skipping')
                continue
            except AttributeError:
                self.debug('AttributeError, skipping')
                continue

            if not filename:
                self.debug("Skipping empty filename.")
                continue

            # Create the full path of the new file in the temporary directory
            full_path = os.path.join(tmpdir, filename)

            # Write the content to the new file
            self.debug(f"Writing {full_path}")
            with open(full_path, 'w') as f:
                f.write(content)
                f.write('\n')

            # debug(f"File {filename} recreated in {tmpdir}")
        return tmpdir
    
    def make_timestamp_tmp_dir(self):
        "Create a timestamped subdirectory. Return the full path."
        current_time = time.strftime('%Y%m%d_%H.%M.%S')
        prefix = 'tfai_output_'
        path = os.path.join(os.getcwd(), prefix + current_time)
        self.debug(f"Creating directory {path}")
        try:
            os.mkdir(path)
        except FileExistsError:
            print(f"ERROR: A directory with the name {current_time} already exists.")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR: {e}")

    # get_file_content() and compare_directories() are used for printing before/after diffs
    def get_file_content(self, file_path):
        "Return the contents of a file."
        with open(file_path, 'r') as f:
            return f.readlines()

    def compare_directories(self, dir1, dir2):
        "Compare .tf files between two directories and print differences."
        files1 = [f for f in os.listdir(dir1) if f.endswith('.tf')]
        files2 = [f for f in os.listdir(dir2) if f.endswith('.tf')]

        common_files = set(files1) & set(files2)
        only_in_dir1 = set(files1) - set(files2)
        only_in_dir2 = set(files2) - set(files1)

        if only_in_dir1:
            print(f"Files only in {dir1}: {', '.join(only_in_dir1)}")
        if only_in_dir2:
            print(f"Files only in {dir2}: {', '.join(only_in_dir2)}")

        for common_file in common_files:
            file1_content = self.get_file_content(os.path.join(dir1, common_file))
            file2_content = self.get_file_content(os.path.join(dir2, common_file))

            diff = difflib.unified_diff(file1_content, file2_content, fromfile=common_file, tofile=common_file)

            diff_output = list(diff)
            if diff_output:
                print(f"Differences in {common_file}:")
                print(''.join(diff_output))

    def run(self, operation: str):
        self.debug("Checking for terraform files in current directory")
        exit_code = self.terraform_init()
        # debug(f"terraform init exit code: {exit_code}")
        if exit_code != 0:
            self.error(f"terraform init failed with exit code {exit_code} before any operations.")
            sys.exit(1)

        exit_code = self.terraform_validate()
        # debug(f"terraform validate exit code: {exit_code}")
        if exit_code != 0:
            self.error(f"terraform validate failed with exit code {exit_code} before any operations.")
            sys.exit(1)
            
        new_tf_encoded = self.get_completion_langchain()
        output_dir = self.recreate_tf_files_from_delim_str(new_tf_encoded)

        os.chdir(output_dir)

        self.terraform_init(after=True)
        self.terraform_validate(after=True)

        os.chdir('..')
        self.compare_directories('.', output_dir)

        print("\nSUCCESS! New Terraform files generated in %s\n" % output_dir)