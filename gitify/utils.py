import subprocess


def get_git_diff():
  result = subprocess.run(['git', 'diff', '--cached'],
                          stdout=subprocess.PIPE,
                          text=True)
  return result.stdout


def run_git_commit(message):
  subprocess.run(['git', 'commit', '-m', message])
