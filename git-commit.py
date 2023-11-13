#!/usr/bin/env python3
import subprocess
import requests
import json

def get_git_diff():
    result = subprocess.run(["git", "diff"], stdout=subprocess.PIPE)
    return result.stdout.decode()

def generate_commit_message(diff):
    prompt = f"Generate a Git commit message based on these changes:\n\n{diff}"

    headers = {
        'Authorization': f'Bearer {config.OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        'model': 'gpt-4.0-turbo',
        'prompt': prompt,
        'max_tokens': 150
    }

    response = requests.post('https://api.openai.com/v1/engines/gpt-4.0-turbo/completions', headers=headers, json=data)
    return response.json()['choices'][0]['text'].strip()

def main():
    diff = get_git_diff()
    if not diff:
        print("No changes detected.")
        return

    commit_message = generate_commit_message(diff)
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

