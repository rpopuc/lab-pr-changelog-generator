import os
import git
import sys
import openai
import difflib

# Authenticate with OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]

# Clone the repository to a local directory
# repo_dir = sys.argv[1]
# repo = git.Repo(repo_dir)
repo_url = "git@github.com:rpopuc/lab-pr-changelog-generator.git"
repo_dir = "/tmp/repo"
repo = git.Repo.clone_from(repo_url, repo_dir)

# Fetch the PR diff from GitHub API
diff_lines = repo.git.diff('origin/pull/1')

# Initialize variables for added, deleted, and modified lines
added_lines = []
deleted_lines = []
modified_lines = []

# Loop through the diff lines and classify them as added, deleted, or modified
for line in diff_lines.splitlines(True):
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
# print(added_lines)
added_code = "".join(added_lines)
deleted_code = "".join(deleted_lines)
modified_code = "".join(modified_lines)

response = openai.Completion.create(
  model="text-davinci-003",
  prompt=f"Based only on this diffs:\nAdded code:\n{added_code}\nDeleted code:\n{deleted_code}\nModified code:\n{modified_code}.\n\nExplain the main changes, one per line, made on the code in terms of added, changed or removed funcionality.",
  temperature=0.7,
  max_tokens=400,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)

# Extract the summary from the result
summary = response.choices[0].text.strip()
print(summary)