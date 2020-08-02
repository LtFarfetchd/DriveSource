import argparse
from shell.shell import start as startShell
import json

if __name__ == "__main__":
  jsonEncodedCommands = None
  with open('commands.json') as commands:
      jsonEncodedCommands = json.loads(commands.read())

  parser = argparse.ArgumentParser(
      prog='sd',
      description='Mark directories on your computer as SourceDrive repositories, link them to Google Drive folders and sync your files from Drive.',
      epilog='Please raise an issue on GitHub if you find bugs or want to request a feature - PRs also welcome.'
    )
  parser.add_argument('-v', '--version', help='')
  subparsers = parser.add_subparsers(dest='command')
  for command in jsonEncodedCommands:
    subparser = subparsers.add_parser(command)
    options = jsonEncodedCommands[command]['options']
    arguments = jsonEncodedCommands[command]['arguments']
    for option in options:
      subparser.add_argument(f'-{options[option]["shortcut"]}', f'--{option}', help=options[option]['description'], action='store_true')
    for argument in arguments:
      subparser.add_argument(argument, help=arguments[argument]['description'], nargs=arguments[argument]['nargs'])
  args = parser.parse_args()

  if args.command == None:
    startShell()