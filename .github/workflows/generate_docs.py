import os
import git
import sys
import openai
import difflib

# Authenticate with OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]

# Load GPT-3 model
model_engine = "text-davinci-003"
model = openai.Model.load(model_engine)

# Clone the repository to a local directory
# repo_dir = sys.argv[2]
# repo = git.Repo(repo_dir)
repo_url = "https://github.com/rpopuc/lab-pr-changelog-generator"
repo_dir = "local/repo/dir"
repo = git.Repo.clone_from(repo_url, repo_dir)

# Fetch the PR diff from GitHub API
pr_number = sys.argv[1]
diff_lines = repo.git.diff(f"origin/pull/{pr_number}")

files = set()
for line in diff_lines:
    if line.startswith("+++"):
        file_path = line[4:]
        if file_path.startswith("b/"):
            file_path = file_path[2:]
        files.add(file_path)

original_code = []
for file in files:
    original_code.append(file + ':')
    original_code.append(repo.git.show(f"origin/main:{file}"))
    original_code.append('')

# Initialize variables for added, deleted, and modified lines
added_lines = []
deleted_lines = []
modified_lines = []

# Loop through the diff lines and classify them as added, deleted, or modified
for line in diff_lines:
    if line.startswith("+"):
        added_lines.append(line)
    elif line.startswith("-"):
        deleted_lines.append(line)
    elif line.startswith(" "):
        pass
    else:
        modified_lines.append(line)

# Use the difflib library to find the longest common subsequence between the added and deleted lines
matcher = difflib.SequenceMatcher(None, added_lines, deleted_lines)
lcs = matcher.find_longest_match(0, len(added_lines), 0, len(deleted_lines))

# Extract the added, deleted, and modified code blocks
added_code = "\n".join(added_lines[lcs.a:lcs.a + lcs.size])
deleted_code = "\n".join(deleted_lines[lcs.b:lcs.b + lcs.size])
modified_code = "\n".join(modified_lines)
original_code = "\n".join(original_code)

# Concatenate the original and modified code blocks into a single prompt string
prompt = f"Here are the main changes in the PR:\n\nOriginal code:\n{original_code}\nAdded code:\n{added_code}\nDeleted code:\n{deleted_code}\nModified code:\n{modified_code}. Summarize the main changes: "

# Use the prompt to generate a document summarizing the main changes
result = model.generate(prompt=prompt, max_tokens=512)

# Extract the summary from the result
summary = result.choices[0].text.strip()
