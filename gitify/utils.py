import os
import shutil
import subprocess
import tempfile


def get_git_diff() -> str:
  result = subprocess.run(['git', 'diff', '--cached'],
                          stdout=subprocess.PIPE,
                          text=True)
  return result.stdout


def run_git_commit(message):
  subprocess.run(['git', 'commit', '-m', message])


def open_editor_with_content(initial_content="") -> str:
  editor = os.environ.get("VISUAL") or os.environ.get("EDITOR") or "vi"

  # Ensure the editor exists in PATH
  if not shutil.which(editor):
    raise FileNotFoundError(
        f"Editor '{editor}' not found. Please set the VISUAL or EDITOR environment variable to a valid editor."
    )

  with tempfile.NamedTemporaryFile(suffix=".tmp",
                                   delete=False,
                                   mode="w+",
                                   encoding="utf-8") as tf:
    HEADER = "# Generated commit message is below. Make any changes then save the file. \n# Any lines starting with '#' will not be included in the commit message.\n\n"

    total_content = HEADER + initial_content.strip()
    tf.write(total_content)
    tf.flush()
    temp_path = tf.name

  try:
    subprocess.run([editor, temp_path], check=True)
  except subprocess.CalledProcessError as e:  # If editor fails to open
    raise RuntimeError(f"Editor exited with an error: {e}")
  except FileNotFoundError:
    raise FileNotFoundError(f"Editor '{editor}' could not be launched.")

  with open(temp_path, "r", encoding="utf-8") as tf:
    edited_content = "".join(line for line in tf
                             if not line.lstrip().startswith('#'))

  edited_content = edited_content.strip()
  if edited_content == "":
    raise ValueError("Can not have a commit message that is empty.")

  os.remove(temp_path)

  return edited_content


def confirm_operation(message) -> bool:
  while True:
    confirm = input(message + " [y/n]: ").strip().lower()
    if confirm == "y":
      return True
    elif confirm == "n":
      return False
    else:
      print("Please type 'y or 'n'.")
