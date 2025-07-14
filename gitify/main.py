import argparse

from gitify.__init__ import DEFAULT_MODEL, MODEL_INPUT_COST
from gitify.config import get_api_key, get_model, set_config
from gitify.llm import generate_commit_message, get_tokens_cost
from gitify.utils import get_git_diff, run_git_commit


def main():
  parser = argparse.ArgumentParser(
      prog='gitify',
      description='Generate Git commit messages using LLMs.',
  )

  subparsers = parser.add_subparsers(dest='command',
                                     required=True,
                                     help='Subcommands')
  commit_parser = subparsers.add_parser(
      'commit',
      help='Generate and run a commit with an AI-generated message.',
      description=
      'Use this command after staging your changes to auto-generate a commit message using GPT.'
  )

  config_parser = subparsers.add_parser(
      'config',
      help='Save your OpenAI API key and model to local config.',
      description=
      'Configure Gitify with your OpenAI API key and preferred model (e.g., gpt-4).'
  )
  config_parser.add_argument('--api_key',
                             required=True,
                             help='Your OpenAI API key.')
  config_parser.add_argument('--model',
                             default=DEFAULT_MODEL,
                             help='LLM model to use (default: gpt-4).')
  args = parser.parse_args()

  if args.command == 'config':
    set_config(args.api_key, args.model)
    print("✅ Configuration saved.")
    return

  elif args.command == 'commit':
    api_key = get_api_key()
    model = get_model()
    diff = get_git_diff()

    if not api_key.strip():
      print(
          " Please configure an API key before use using gitify config --api_key"
      )

    if not diff.strip():
      print(
          "⚠️  No staged changes found. Please stage files using `git add` before running gitify."
      )
      return

    commit_message = generate_commit_message(diff, api_key, model)
    # TODO: Here I want it to be more like normal github where you actually view and can edit the message before confirming it then it gets commited.
    print(f"\nGenerated commit message:\n{commit_message}\n")

    if model in MODEL_INPUT_COST:
      # TODO: should not really display this cost unless it is greater than a cent!
      total_cost = get_tokens_cost(diff, model)
      if total_cost < 0.01:
        total_cost = '~ < $0.01'
      else:
        total_cost = '~ $' + str(total_cost)

      print("Estimated Cost: " + total_cost + "\n")

    while True:
      confirm = input(
          "Do you want to commit with this message? [y/n]: ").strip().lower()
      if confirm == 'y':
        run_git_commit(commit_message)
        print("✅ Commit created.")
        break
      elif confirm == 'n':
        print("❌ Commit cancelled.")
        break
      else:
        print("Please type 'y' or 'n'.")
