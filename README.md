If you are tired of making ideas of writing git commit comments?  
Let AI do it for you.  
Just write: gg  
and AI will create commit message for you and push it in repository  

## Install
```
git clone https://github.com/bsnjoy/git-commit-gpt.git
cd git-commit-gpt
pip install -r requirements.txt --break-system-packages --upgrade
cp config.py.sample config.py
# Edit config.py and put your OPENAI_API_KEY

# Execute below command and put result command in .profile .bashrc and/or .zshrc or other file whie is loaded when new shell executed. To make gg work in current shell, run it here also.
echo "alias gg=`pwd`/git-commit-ollama.py"

# Execute like so:
gg
```
