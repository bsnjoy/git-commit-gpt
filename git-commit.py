#!/usr/bin/env python3
import subprocess
import json
import config
import openai

openai.api_key = config.OPENAI_API_KEY

def get_git_diff():
    result = subprocess.run(["git", "diff"], stdout=subprocess.PIPE)
    return result.stdout.decode()

def generate_commit_message(diff):
    prompt = f'''Write a comment, which I will put in git commit command for changes below git diff.
 Include description of what was changed so that user, who is not familiar with the programming will understand what has been updated. 
 Don't write which files were changed. 
 1. output with no introduction, no explaintation, only comment.
 2. DONT MAKE ANY MISTAKES, check if you did any
 3. only return comment, and nothing else.
 4. no DOCUMENATION IN THE OUTPUT

git diff:\n{diff}'''

    completion = openai.ChatCompletion.create( # Change the function Completion to ChatCompletion
  model = config.OPENAI_API_MODEL,
  messages = [ # Change the prompt parameter to the messages parameter
    {"role": "system", "content": "You are a helpful assistant."},
    {'role': 'user', 'content': prompt}
  ],
  temperature = 0  
)
    
    try:
        return True, completion.choices[0].message.content
    except KeyError:
        print("Error: 'choices' key not found in response.")
        print("Response content:", completion.text)
        return False, "Error in generating commit message"

    except json.JSONDecodeError:
        print("Error: Unable to decode JSON response.")
        print("Response content:", completion.text)
        return False, "Error in generating commit message"

def main():
    diff = get_git_diff()
    if not diff:
        print("No changes detected.")
        return

    error, commit_message = generate_commit_message(diff)
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

