import argparse

from gitify.config import get_api_key, get_model
from gitify.llm import generate_commit_message
from gitify.utils import get_git_diff, run_git_commit


def main():
  parser = argparse.ArgumentParser(
      prog='gitify', description='Generate commit messages using LLMs.')
  parser.add_argument('command', choices=['commit'])
  args = parser.parse_args()

  if args.command == 'commit':
    api_key = get_api_key()
    model = get_model()
    diff = get_git_diff()

    if not diff.strip():
      print(
          "No changes to commit. Please stage changes before running gitify.")
      return

    commit_message = generate_commit_message(diff, api_key, model)
    # TODO: Here I want it to be more like normal github where you actually view and can edit the message before confirming it then it gets commited.
    print(f"\nGenerated commit message:\n> {commit_message}")
    run_git_commit(commit_message)
