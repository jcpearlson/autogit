import argparse

from gitify.__init__ import DEFAULT_MODEL, MODEL_INPUT_COST
from gitify.config import get_api_key, get_model, set_config
from gitify.llm import generate_commit_message, get_tokens_cost
from gitify.utils import get_git_diff, open_editor_with_content, run_git_commit


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
    #TODO: add a flag to commit where the user can choose to skip all prompts and just auto commit whatever message it generates
    #TODO: add a flag that bypasses confirms but still allows the user to view and edit the message before commit
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

    #  Generate a cost estimation for the operation
    if model in MODEL_INPUT_COST:
      total_cost = get_tokens_cost(diff, model)
      float_total_cost = float(total_cost)

      if total_cost < 0.01:
        total_cost = '~ < $0.01'
      else:
        total_cost = '~ $' + str(total_cost)

      print("Estimated cost: " + total_cost + "\n")

      # NOTE: if total cost is greater than 10 cents we will reprompt the user for cost
      if float_total_cost >= 0.1:
        while True:
          confirm = input("Generate commit message? [y/n]: ").strip().lower()
          if confirm == 'y':
            break
          elif confirm == 'n':
            print('Aborting operation.')
            return
          else:
            print("Please type 'y' or 'n'.")
    else:
      print('No cost estimation could be found for this model type.')
      # TODO: This operation will take x tokens please confirm ext or figure out how to handle this case

    commit_message = generate_commit_message(diff, api_key, model)

    # NOTE: Allows user to view commit message and make any changes before saving
    commit_message = open_editor_with_content(commit_message)

    print(f"Final commit message:\n\n{commit_message}\n")

    while True:
      confirm = input(
          "Do you want to commit with this message? [y/n]: ").strip().lower()
      if confirm == 'y':
        run_git_commit(commit_message)
        print("✅ Commit created.\n")
        break
      elif confirm == 'n':
        print("❌ Commit cancelled.")
        return
      else:
        print("Please type 'y' or 'n'.")
