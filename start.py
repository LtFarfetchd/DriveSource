from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from shadowHierarchy import ShadowDir, ShadowNonDir, ShadowHierarchy
from constantTypes import *
import shlex
import json

def formatCommands(jsonEncodedCommands):
  commandNames = list(jsonEncodedCommands.keys())
  return '\n'.join(
    list(map(
      lambda key : (
        f'[{jsonEncodedCommands[key]["shortcut"]}] '
        f'{key} '
        f'{("|" + ", ".join(jsonEncodedCommands[key]["arguments"]) + "|") if "arguments" in jsonEncodedCommands[key] else ""} '
        '-> '
        f'{jsonEncodedCommands[key]["description"]}'),
      commandNames
    ))
  )

def getHelp(jsonEncodedCommands):
  return (
    'Welcome to SourceDrive, friends.\n'
    'This is a python program built on top of PyDrive for synchronising a local directory with a directory in Google Drive.\n\n'
    'Accepted input:\n'
    '[shortcut] command |argument(s)| -> explanation\n\n'
    f'{formatCommands(jsonEncodedCommands)}'
  )

def generateShadows(shadowDir, fileList):
  return map(
    lambda driveFile: 
      ShadowDir(driveFile['id'], driveFile['title'], shadowDir, driveFile) if driveFile['mimeType'] == FOLDER_MIMETYPE 
      else ShadowNonDir(driveFile['id'], driveFile['title'], shadowDir, driveFile), 
    fileList
  )

def getCommand(response):
  return response.split()[0].lower()

def getArguments(validatedResponse):
  return list(map(lambda arg: arg.lower(), shlex.split(validatedResponse)[1:]))

def getInputResponse(permittedCommands):
  responded = False
  while not responded:
    response = input(f'{CLI_PROMPT} ')
    if getCommand(response) in permittedCommands:
      return response

def getBooleanResponse(prompt):
  responded = False
  while not responded:
    validatedResponse = input(prompt).lower()
    if validatedResponse in ['y', 'n']:
      return validatedResponse == 'y'

def getPath(shadowDir):
  if shadowDir.parentDir is None:
    return '/'
  return f'{getPath(shadowDir.parentDir)}{shadowDir.displayName}/'

def isolateFilesByShadowType(shadowDir, shadowType):
  return list(map(
    str,
    filter(
      lambda shadowChild : isinstance(shadowChild, shadowType), 
      shadowDir.children.values()
    )
  ))

def listFiles(shadowDir):
  newline = '\n'
  dirSeparator = '\n/'
  dirs = isolateFilesByShadowType(shadowDir, ShadowDir)
  nonDirs = isolateFilesByShadowType(shadowDir, ShadowNonDir)
  return (
    f'{"/" + dirSeparator.join(dirs) + newline if len(dirs) > 0 else ""}'
    f'{newline.join(nonDirs)}'
  )

def performAction(validatedResponse, currentDir, shadowHierarchy, jsonEncodedCommands, commandKeys):
  command = getCommand(validatedResponse)
  if command in ['help', 'h']:
    print(getHelp(jsonEncodedCommands))

  elif command in ['up', 'u']:
    if currentDir.parentDir is not None:
      return currentDir.parentDir
    else:
      print('Cannot navigate up: you are at the root.') 

  elif command in ['down', 'd']:
    argDir = getArguments(validatedResponse)[0]
    try:
      nextDir = currentDir.children[argDir]
      return nextDir
    except KeyError:
      print('Cannot navigate down: the specified directory does not exist.')

  elif command in ['list', 'l']:
    print(f'{getPath(currentDir)}\n')
    print(f'{listFiles(currentDir)}\n')

  elif command in ['target', 't']:
    targetWillChange = True
    if shadowHierarchy.target is not None:
      targetWillChange = getBooleanResponse(
        f'Target has already been set to {getPath(shadowHierarchy.target)}.\n'
        f'Changing the target requires a full local re-sync. Change the target to {getPath(currentDir)} anyway [Y/n]?'
      )
    if targetWillChange:
      shadowHierarchy.target = currentDir
      print(f'{getPath(currentDir)} set as target.')
    else:
      print('Target was not changed.')

  return currentDir

jsonEncodedCommands = None
with open('commands.json') as commands:
  jsonEncodedCommands = json.loads(commands.read())

commandKeys = list(jsonEncodedCommands.keys())
commandKeys.extend(list(map(lambda key : jsonEncodedCommands[key]['shortcut'], commandKeys)))

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
shadowHierarchy = ShadowHierarchy(ShadowDir('root', '', None, None))
print(ASCII_ART_TITLE)
targetedDir = None
currentDir = shadowHierarchy.root
while targetedDir is None:
  if not currentDir.synced:
    query = f"'{currentDir.driveId}' in parents and trashed=false"
    fileList = drive.ListFile({'q': query}).GetList()
    for shadowFile in generateShadows(currentDir, fileList):
      currentDir.addChild(shadowFile)
    currentDir.synced = True

  response = getInputResponse(commandKeys)
  currentDir = performAction(response, currentDir, shadowHierarchy, jsonEncodedCommands, commandKeys)

        
        
    
        