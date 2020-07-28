from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from shadowHierarchy import ShadowDir, ShadowNonDir, ShadowHierarchy
import types
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
    'This is a python program built on top of PyDrive for synchronising a local directory with a directory in Google Drive.\n\n'
    'Accepted input:\n'
    '[shortcut] command |argument(s)| -> explanation\n\n'
    f'{formatCommands(jsonEncodedCommands)}'
  )

def generateShadows(shadowDir, fileList):
  return map(
    lambda driveFile: 
      ShadowDir(driveFile['id'], driveFile['title'], shadowDir, driveFile) if driveFile['mimeType'] == types.FOLDER_MIMETYPE 
      else ShadowNonDir(driveFile['id'], driveFile['title'], shadowDir, driveFile), 
    fileList
  )

def deformatResponse(response):
  return response.split()[0].lower()

def getArguments(validatedResponse):
  return list(map(lambda arg: arg.lower(), validatedResponse.split()[1:]))

def getAction(permittedCommands):
  responded = False
  while not responded:
    response = input('SD >| ')
    if deformatResponse(response) in permittedCommands:
      return response

def getPath(shadowDir):
  if shadowDir.getParent() is None:
    return '/'
  return f'{getPath(shadowDir.getParent())}/{shadowDir.getName()}'

def isolateSubDirs(shadowDir):
  return list(filter(lambda subFile : isinstance(subFile, ShadowDir), shadowDir.getChildren()))

def isolateSubNonDirs(shadowDir):
  return list(filter(lambda subFile : not isinstance(subFile, ShadowDir), shadowDir.getChildren()))

def listFiles(shadowDir):
  newLine = '\n'
  return (
    f'/{newLine.join(isolateSubDirs(shadowDir))}'
    f'{newLine.join(isolateSubNonDirs(shadowDir))}'
  )

def performAction(validatedResponse, shadowDir, commandKeys):
  command = deformatResponse(response)
  if command in ['help', 'h']:
    print(getHelp(commandKeys))
  elif command in ['up', 'u']:
    if shadowDir.getParent() is not None:
      return shadowDir.getParent()
    else:
      print('Cannot navigate up: you are at the root') 
  elif command in ['down', 'd']:
    argDir = getArguments(validatedResponse)[0]
    try:
      nextDir = shadowDir.getChildren()[argDir]
      return nextDir
    except KeyError:
      print('Cannot navigate down: the specified directory does not exist')
  elif command in ['list', 'l']:
    print(f'{getPath(shadowDir)}\n')
    print(f'{listFiles(shadowDir)}\n')
  elif command in ['target', 't']:
    print('TODO')
  return shadowDir

            
jsonEncodedCommands = None
with open('commands.json') as commands:
  jsonEncodedCommands = json.loads(commands.read())

commandKeys = list(jsonEncodedCommands.keys())
commandKeys.extend(list(map(lambda key : jsonEncodedCommands[key]['shortcut'], commandKeys)))

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
shadowHierarchy = ShadowHierarchy(ShadowDir('root', '', None, None))

targetedDir = None
currentDir = shadowHierarchy.getRoot().getId()
while targetedDir is None:
  query = f"'{currentDir}' in parents and trashed=false"
  fileList = drive.ListFile({'q': query}).GetList()

  shadowFiles = generateShadows(currentDir, fileList)
  for shadowFile in shadowFiles:
    currentDir.addChild(shadowFile)

  response = getAction(commandKeys)
  currentDir = performAction(response, currentDir, commandKeys)

        
        
    
        