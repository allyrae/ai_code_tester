


# AI Code Tester
Overview
The AI Tester is a script designed to test code against specified test cases using OpenAI's GPT-3 language model. This tool facilitates automated testing by generating prompts based on test instructions and code, then evaluating the output provided by the GPT-3 model.

# Requirements
Before using the AI Tester, ensure you have the following prerequisites installed:

Python 3.x
OpenAI Python library (openai)
An OpenAI GPT-3 API key
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/your-repo.git
Install dependencies:

bash
Copy code
pip install openai
Configure the AI Tester by creating a configuration file named ai_tester.cfg with the following structure:

ini
Copy code
[ai_tester_config]
openai_api_key = YOUR_OPENAI_API_KEY
valid_extensions = py, js  # Add valid file extensions separated by commas
max_tokens = 100  # Set the maximum number of tokens for GPT-3 output
engine = text-davinci-002  # Specify the GPT-3 engine to use
Usage
Run the AI Tester script by executing the following command:

bash
Copy code
python AI_Tester.py [-detailed] [path]
Use the -detailed flag to enable detailed output.
Optionally, specify a path or file for testing (default: current directory).
Test Instructions
Create a test instruction file named ai_test_instructions.ai_test within the test directory. The content of this file should include the instructions for the GPT-3 model.

#Test Files
Place your test files in the test directory with the extension .ai_test. Each test file corresponds to a set of code and test instructions.

#Output
The script will display the results of the tests, indicating whether each test passed or failed. Detailed output includes the GPT-3-generated response.

#Example
bash
Copy code
python AI_Tester.py -detailed /path/to/tests
#Notes
Ensure your OpenAI API key is kept confidential and not shared publicly.
Customize the valid file extensions in the ai_tester.cfg file based on the programming languages you are testing.
Feel free to explore and enhance the AI Tester according to your specific testing requirements. If you encounter any issues or have suggestions for improvement, please create an issue on the GitHub repository.
