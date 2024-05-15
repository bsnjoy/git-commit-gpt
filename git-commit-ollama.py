#!/usr/bin/env python3
import subprocess
import json
import config
import re
import ollama

prefix = "Here's the one liner comment for the changes:"

def get_git_status():
    result = subprocess.run(["git", "status"], stdout=subprocess.PIPE)
    return result.stdout.decode()

def get_git_diff():
    result = subprocess.run(["git", "diff"], stdout=subprocess.PIPE)
    return result.stdout.decode()

def clean_string(input_string):
    # This regular expression matches any non-letter and non-number characters
    # at the beginning (^) or end ($) of the string.
    pattern = r'^[^A-Za-z0-9]+|[^A-Za-z0-9]+$'

    # The re.sub() function replaces the matched patterns with an empty string,
    # effectively removing them.
    return re.sub(pattern, '', input_string)

def generate_commit_message(git_status, git_diff):
    client = ollama.Client(config.OLLAMA_HOST)
    response = client.chat(
        model=config.OLLAMA_MODEL,
        messages = [ # Change the prompt parameter to the messages parameter
            {"role": "system", "content": config.SYSTEM_MESSAGE},
            {'role': 'user', 'content': config.EXAMPLE_USER_1},
            {'role': 'assistant', 'content': config.EXAMPLE_ASSYSTANT_1},
            # {'role': 'user', 'content': config.EXAMPLE_USER_2},
            # {'role': 'assistant', 'content': config.EXAMPLE_ASSYSTANT_2},
            {'role': 'user', 'content': config.PROMPT.format(git_status, git_diff)}
        ],
        options = {"temperature": 0, "top_p": 0, "top_k": 1},
        # temperature=0
    )
    
    try:
        return True, clean_string(response['message']['content'])
    except KeyError:
        print("Error: 'choices' key not found in response.")
        print("Response content:", response)
        return False, "Error in generating commit message"

    except json.JSONDecodeError:
        print("Error: Unable to decode JSON response.")
        print("Response content:", response)
        return False, "Error in generating commit message"

def main():
    git_status = get_git_status()
    git_diff = get_git_diff()
    if not git_status and not git_diff :
        print("No changes detected.")
        return

    error, command = generate_commit_message(git_status, git_diff)
    if not error:
        print("Error in generating commit message.")
        return

    command = command.split('\n')[0].strip()
    # ensure the command ends with a double quote "
    if command[-1] != '"':
        command += '"'
    print(command)
    confirmation = input("\nDo you want to proceed with this command? (Y/n): ")

    if confirmation.lower() in ['y', 'yes', '']:
#        subprocess.run(["git", "commit", "-am", commit_message])
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
# Check the result
        if result.returncode == 0:
            print("Commit successful.")
            print("Output:", result.stdout)
        else:
            print("Commit failed.")
            print("Error:", result.stderr)

        subprocess.run(["git", "push"])
        print("Push successful.")
    else:
        print("Commit aborted.")

if __name__ == "__main__":
    main()

