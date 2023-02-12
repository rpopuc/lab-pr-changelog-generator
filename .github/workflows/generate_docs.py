import os
import git
import sys
import openai
import difflib

# Authenticate with OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]

# Load GPT-3 model
# model_engine = "text-davinci-003"
# model = openai.Model.load(model_engine)

# Clone the repository to a local directory
repo_dir = sys.argv[2]
repo = git.Repo(repo_dir)
# repo_url = "https://github.com/rpopuc/lab-pr-changelog-generator"
# repo_dir = "/tmp/repo"
# repo = git.Repo.clone_from(repo_url, repo_dir)

# Fetch the PR diff from GitHub API
# pr_number = sys.argv[1]
diff_lines = repo.git.diff(f"origin/main")

# newFiles = set()
# changedFiles = set()
# for line in diff_lines.splitlines(True):
#     if line.startswith("+++"):
#         file_path = line[4:]
#         if file_path.startswith("b/"):
#             newFiles.add(file_path[2:].rstrip())
#         else:
#             changedFiles.add(file_path)

# original_code = []
# for file in newFiles:
#     original_code.append(file + ':')
#     # original_code.append(repo.git.show(f"origin/main:{file}"))
#     with open(repo_dir + '/' + file) as f:
#         original_code.append("".join(f.readlines()))
#         f.close()
#     original_code.append('')

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
  prompt=f"Based only on this diffs:\nAdded code:\n{added_code}\nDeleted code:\n{deleted_code}\nModified code:\n{modified_code}.\n\nExplain the main changes made on the code in terms of added, changed or removed funcionality.",
  temperature=0.7,
  max_tokens=400,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)

# Extract the summary from the result
summary = response.choices[0].text.strip()
print(summary)