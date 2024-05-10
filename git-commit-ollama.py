#!/usr/bin/env python3
import subprocess
import json
import config
import re
import ollama

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
            {"role": "system", "content": "You are a git comment generator."},
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

    error, commit_message = generate_commit_message(git_status, git_diff)
    if not error:
        print("Error in generating commit message.")
        return
    print("Suggested commit message:\n")
    print(commit_message)
    confirmation = input("\nDo you want to proceed with this commit message? (Y/n): ")

    if confirmation.lower() in ['y', 'yes', '']:
        subprocess.run(["git", "commit", "-am", commit_message])
        print("Commit successful.")
        subprocess.run(["git", "push"])
        print("Push successful.")
    else:
        print("Commit aborted.")

if __name__ == "__main__":
    main()

