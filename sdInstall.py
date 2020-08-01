import subprocess
import os, sys, platform, shutil, errno, argparse
from constants import VERSION, REPO_URL

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument(
    '-v', 
    '--verbose', 
    required=False, 
    action='store_true', 
    help='Runs the installer in verbose mode. \
      Errors and output produced by your shell will be forwarded up to you. \
      The installer will keep you informed as it progresses through each step.'
  )
  args = parser.parse_args()

  print(f'Installing SourceDrive v{VERSION}')

  if args.v:
    print('Verifying python version...')
  major, minor, patch = platform.python_version_tuple()
  if major < 3:
    print('SourceDrive was built in Python 3.7. At this time, it is not backwards compatible with Python 2.x.\nExiting installer.')
    sys.exit()
  elif major == 3 and minor < 7:
    print('SourceDrive was built in Python 3.7. Although it should work in 3.x, not all expected behaviour is guaranteed.')

  if args.v:
    print('Establishing os and appropriate shell...')
  currentDir = os.path.dirname(os.path.realpath(__file__))
  userOS = platform.system()
  execution = None
  shell = None

  if userOS == 'Windows':
    shell = 'Powershell'
    execution = [
      "powershell.exe", 
      '-ExecutionPolicy',
      'Unrestricted',
      f'{currentDir}\\install\\install.ps1'
    ]
  else:
    # assume posix-compliant, if not - well, bad luck
    shell = 'a POSIX-compliant shell such as bash or zsh'
    execution = [
      f'{currentDir}/install/install.sh'
    ]

  if args.v:
    print('Attempting to add SourceDrive as an alias on your machine and refresh your shell...')
  try:
    out, err = subprocess.Popen(execution, stdout=sys.stdout).communicate()
    if args.v:
      print(f'Output from your shell:\n{out}')
  except OSError as e:
    if e.errno == errno.ENOENT:
      print(f'This installer requires an appropriate shell to run - i.e. {shell}. It seems like you don\'t have any such shell installed.\nExiting installer.')
    else:
      print(f'Your shell terminated with the following error:\n{err}.\nExiting installer.')

  print(f'SourceDrive has been successfully installed!\nRun `sd -h` for usage, or check out the readme at {REPO_URL}.')
