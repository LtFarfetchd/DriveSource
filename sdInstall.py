import os, sys, platform, shutil, errno, argparse, urllib.request, json, typing
from subprocess import Popen, PIPE
from operator import itemgetter
from typing import Any, Dict, List

def getGitHubScriptContents(fileList: List[Dict[str, Any]], scriptName: str) -> str:
  script = next(script for script in fileList if script['name'] == scriptName)
  req = urllib.request.urlopen(script['download_url'])
  return req.read()

def getBooleanResponse(prompt: str) -> bool:
  responded = False
  while not responded:
    validatedResponse = input(prompt).lower()
    if validatedResponse in ['y', 'n']:
      return validatedResponse == 'y'

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
  parser.add_argument(
    'installDir', 
    nargs='?', 
    help='The local directory where you would like SourceDrive installed'
  )
  parser.add_argument(
    'clientSecrets',
    nargs='?',
    help='A path to a `client_secrets.json` file in your local filesystem. \
      The file should contain the json-encoded credentials of a Google Cloud \
      Platform OAuth web-application client you have created, \
      with the necessary Drive API permissions.'
  )
  args = parser.parse_args()
  verbose = args.verbose
  callingDir = os.path.dirname(os.path.realpath(__file__))

  # validate install location and client_secrets arguments
  if args.clientSecrets is None:
    print('Warning: Path to a client secrets file has not been provided.\n\
      You can add your credentials manually later, but SourceDrive will not \
      be authorised to access your Drive folders until you do.')
    shouldProceed = getBooleanResponse('Proceed with installation anyway [y/n]? ')
    if not shouldProceed:
      print('Exiting installer.')
      sys.exit()

  if args.installDir is None:
    print('Warning: Path to an install directory was not provided.\n'
      f'The installer will default to the calling directory ({callingDir}).')
    shouldProceed = getBooleanResponse('Proceed with installation to the calling directory [y/n]? ')
    if not shouldProceed:
      print('Exiting installer.')
      sys.exit()

  # fetch constants
  req = urllib.request.urlopen('https://raw.githubusercontent.com/LtFarfetchd/DriveSource/master/installConstants.json')
  VERSION, REPO_URL = itemgetter('VERSION', 'REPO_URL')(json.loads(req.read()))

  # --------- START INSTALLATION
  print(f'Installing SourceDrive v{VERSION}')

  # {1}: validate python version
  if verbose:
    print('Verifying python version...')
  major, minor, patch = list(map(float, platform.python_version_tuple()))
  if major < 3:
    print('SourceDrive was built in Python 3.7. At this time, it is not backwards compatible with Python 2.x.\nExiting installer.')
    sys.exit()
  elif major == 3 and minor < 7:
    print('SourceDrive was built in Python 3.7. Although it should work in any 3.x, not all expected behaviour is guaranteed.')

  # {2}: prepare to fetch install scripts
  if verbose:  
    print('Fetching endpoints for additional installer files...')
  req = urllib.request.urlopen('https://api.github.com/repos/ltfarfetchd/DriveSource/contents/installScripts')
  installFileList = json.loads(req.read())

  # {3}: determine platform to branch between sh and ps1 install scripts
  if verbose:
    print('Establishing os and appropriate shell...')
  userOS = platform.system()
  installExecution = None
  makeAliasExecution = None
  shell = None

  # {4}: prepare relevant installer and makeAlias scripts
  if userOS == 'Windows':
    installScriptContents = getGitHubScriptContents(installFileList, 'install.ps1')
    makeAliasScriptContents = getGitHubScriptContents(installFileList, 'makeAlias.ps1')
    shell = 'Powershell'
    installExecution = [
      'powershell.exe', 
      '-ExecutionPolicy',
      'Unrestricted',
    ]
  else: # assume posix-compliant, if not - well, bad luck
    installScriptContents = getGitHubScriptContents(installFileList, 'install.sh')
    makeAliasScriptContents = getGitHubScriptContents(installFileList, 'makeAlias.sh')
    shell = 'a POSIX-compliant shell such as bash or zsh'
    execution = ['sh']

  # {5}: execute relevant installer script (pulling down git repo)
  if verbose:
    print('Attempting to add SourceDrive as an alias on your machine and refresh your shell...')
  try:
    p = Popen(execution, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate(input=installScriptContents)
    if verbose:
      print(f'Output from your shell:\n{out}')
  except PermissionError as e:
    print('Permissions to the necessary installer scripts are restricted such that the installer cannot run them.\nExiting installer.')
    sys.exit()
  except OSError as e:
    if e.errno == errno.ENOENT:
      print(f'This installer requires an appropriate shell to run - i.e. {shell}. It seems like you don\'t have any such shell installed.\nExiting installer.')
    else:
      print(f'Your shell terminated with the following error:\n{err}.\nExiting installer.')
    sys.exit()

    # {6}: execute relevant makeAlias script
  

  print(f'SourceDrive has been successfully installed!\nRun `sd -h` for usage, or check out the readme at {REPO_URL}.')
