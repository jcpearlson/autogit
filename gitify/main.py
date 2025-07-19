import argparse

from gitify.__init__ import DEFAULT_MODEL, MODEL_INPUT_COST
from gitify.config import get_api_key, get_model, set_config
from gitify.llm import (generate_commit_message, get_tokens_cost,
                        get_tokens_length)
from gitify.utils import (confirm_operation, get_git_diff,
                          open_editor_with_content, run_git_commit)


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
  commit_parser.add_argument('--no_confirm',
                             action='store_true',
                             help='Bypass all confirmation prompts')

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
    # TODO: this method needs much more error handling around the input of args.api_key and args.model int terms of them being valid
    set_config(args.api_key, args.model)
    print("✅ Configuration saved.")
    return

  elif args.command == 'commit':
    api_key = get_api_key()
    model = get_model()
    git_diff_text = get_git_diff()

    if not api_key.strip():
      print(
          " Please configure an API key before use using gitify config --api_key"
      )

    if not git_diff_text.strip():
      print(
          "⚠️  No staged changes found. Please stage files using `git add` before running gitify."
      )
      return

    if args.no_confirm:
      commit_message = generate_commit_message(git_diff_text, api_key, model)
      run_git_commit(commit_message.strip())
      print("✅ Commit created.\n")
      return

    #  Generate a cost estimation for the operation
    if model in MODEL_INPUT_COST:
      total_cost = get_tokens_cost(git_diff_text, model)
      float_total_cost = float(total_cost)

      if total_cost < 0.01:
        total_cost = '~ < $0.01'
      else:
        total_cost = '~ $' + str(total_cost)

      print("Estimated cost: " + total_cost + "\n")

      if float_total_cost >= 0.1:  # NOTE: confirm if 10 cents or greater in cost
        if not confirm_operation(message="Generate commit message?"):
          print("Aborting operation.")
          return
    else:
      # Model is not in MODEL_INPUT_COST
      total_token_length = get_tokens_length(git_diff_text, model)

      print("Estimated tokens: ~ " + str(total_token_length) + "\n")

      if total_token_length > 50_000:  # NOTE: confirm if 50k tokens or greater
        if not confirm_operation(message="Generate commit message?"):
          print("Aborting operation.")
          return

    commit_message = generate_commit_message(git_diff_text, api_key, model)

    # NOTE: view and make changes to message
    commit_message = open_editor_with_content(commit_message)

    # NOTE: final confirm before commit
    CONFIRM_COMMIT_MESSAGE = "Do you want to commit with this message?"
    if confirm_operation(CONFIRM_COMMIT_MESSAGE):
      run_git_commit(commit_message)
      print("✅ Commit created.")
    else:
      print("❌ Commit cancelled.")
