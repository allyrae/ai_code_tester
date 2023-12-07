import sys
import os
import json
import configparser
import argparse
from openai import OpenAI

# Function to parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='AI Tester Script')
    parser.add_argument('-detailed', action='store_true', help='Enable detailed output')
    parser.add_argument('path', nargs='?', default=os.getcwd(), help='Specify a path or file for testing (default: current directory)')
    return parser.parse_args()

# Function to read configuration from the configuration file
def read_configuration():
    config = configparser.ConfigParser()
    config.read('ai_tester.cfg')
    return (
        config.get('ai_tester_config', 'openai_api_key'),
        [ext.strip() for ext in config.get('ai_tester_config', 'valid_extensions').split(',')],
        config.getint('ai_tester_config', 'max_tokens'),
        config.get('ai_tester_config', 'engine', fallback='text-davinci-002')
    )

# Function to read test instructions from the instruction file
def read_instruction_file(path):
    instruction_file = os.path.join(path, 'ai_test_instructions.ai_test')
    with open(instruction_file, 'r') as file:
        return file.read()

# Function to read content from a file
def read_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to run tests using OpenAI GPT-3
def run_tests(test_instructions, test_file, code_file, engine, max_tokens, openai_api_key):
    test = read_file_content(test_file)
    code = read_file_content(code_file)

    client = OpenAI(api_key=openai_api_key)

    # Creating a prompt for GPT-3 based on test instructions and code
    completion = client.completions.create(
        model=model,
        prompt=f"{test_instructions}\n\n{test}\n\n## CODE:\n\n{code}",
        max_tokens=max_tokens,
    )

    # Extracting and parsing GPT-3 output
    chatgpt_output = completion.choices[0].text
    return parse_output(chatgpt_output)

# Function to parse and extract information from GPT-3 output
def parse_output(chatgpt_output):
    try:
        output_data = json.loads(chatgpt_output)
        result = output_data.get('result', 'Unknown')
        test_passed = result.lower() == 'pass'
        return test_passed, result
    except json.JSONDecodeError as e:
        print(f"Error decoding ChatGPT output: {e}")
        return False, 'Error'

# Function to find matching code files in a directory
def find_matching_code_files(directory, test_file, valid_extensions):
    base_name, _ = os.path.splitext(test_file)
    return [
        file for file in os.listdir(directory)
        if file.startswith(base_name) and file.endswith(tuple(valid_extensions)) and file != test_file
    ]

# Main function
def main():
    args = parse_arguments()
    openai_api_key, valid_extensions, max_tokens, engine = read_configuration()
    test_instructions = read_instruction_file(args.path)

    # Determine if testing a single file or all files in a directory
    if os.path.isfile(args.path):  # Testing a specific file
        test_files = [args.path]
    else:  # Testing files in a directory
        test_files = [file for file in os.listdir(args.path) if file.endswith(".ai_test")]

    # Iterate through test files
    for test_file in test_files:
        matching_code_files = find_matching_code_files(args.path, test_file, valid_extensions)

        # Check if there are matching code files
        if not matching_code_files:
            print(f"No matching code file found for {test_file}")
            continue

        matching_code_file = os.path.join(args.path, matching_code_files[0])

        # Run tests and get results
        test_passed, chatgpt_output = run_tests(
            test_instructions,
            os.path.join(args.path, test_file),
            matching_code_file,
            model,
            max_tokens,
            openai_api_key
        )

        # Print test results
        print(f"Test for {matching_code_file} {'Passed' if test_passed else 'Failed'}")
        if test_passed or args.detailed:
            print(f"ChatGPT Output: {chatgpt_output}")
        print()

if __name__ == "__main__":
    main()
