from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import json

def formatCommands(jsonEncodedCommands):
  commandNames = list(jsonEncodedCommands.keys())
  return '\n'.join(
    list(map(
      lambda key : (
        f'[{jsonEncodedCommands[key]["shortcut"]}] '
        f'{key} '
        f'{"|" + ", ".join(jsonEncodedCommands[key]["arguments"]) + "|" if "arguments" in jsonEncodedCommands[key] else ""} '
        '-> '
        f'{jsonEncodedCommands[key]["description"]}'),
      commandNames
    ))
  )

def getHelp(jsonEncodedCommands):
  return (
    'Welcome to SourceDrive, friends.\n'
    'This is a python program built on top of PyDrive for syncronising a local directory with a directory in Google Drive.\n\n'
    'Accepted input:\n'
    '[shortcut] command |argument(s)| -> explanation\n\n'
    f'{formatCommands(jsonEncodedCommands)}'
  )

def getDirs(currentDirectory):
  dirs = []
  return list(filter(lambda file: file['mimetype'] == 'application/vnd.google-apps.folder', dirs))

def deformatResponse(response):
  return response.split()[0].lower()

def getAction(permittedCommands):
  responded = False
  while not responded:
    response = input('SD >| ')
    if deformatResponse(response) in permittedCommands:
      return response
            
jsonEncodedCommands = None
with open('commands.json') as commands:
  jsonEncodedCommands = json.loads(commands.read())

commandKeys = list(jsonEncodedCommands.keys())
permittedCommands = commandKeys.extend(list(map(lambda key : jsonEncodedCommands[key]['shortcut'], commandKeys)))

print(getHelp(jsonEncodedCommands))

# gauth = GoogleAuth()
# gauth.LocalWebserverAuth()
# drive = GoogleDrive(gauth)

# fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
# targetedDir = None
# currentDir = 'root'
# while targetedDir is None:
#     dirs = getDirs(currentDir)
#     response = awaitAction()

        
        
    
        