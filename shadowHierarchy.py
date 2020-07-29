from constantTypes import *

def formatKey(key):
  return key.lower()

class ShadowHierarchy:
  def __init__(self, shadowRoot):
    self.root = shadowRoot

class ShadowFile:
  def __init__(self, driveId, displayName, parentDir, underlyingFile):
    self.driveId = driveId
    self.displayName = displayName
    self.parentDir = parentDir
    self.children = {}
    self.underlyingFile = underlyingFile

  def __str__(self):
    return self.displayName

class ShadowDir(ShadowFile):
  def __init__(self, driveId, displayName, parentDir, underlyingFile):
    ShadowFile.__init__(self, driveId, displayName, parentDir, underlyingFile)
    self.isTarget = False

  def addChild(self, shadowFile):
    self.children[formatKey(shadowFile.displayName)] = shadowFile

  def makeTarget(self):
    self.isTarget = True

class ShadowNonDir(ShadowFile):
  def __init__(self, driveId, displayName, parentDir, underlyingFile):
    ShadowFile.__init__(self, driveId, displayName, parentDir, underlyingFile)
    try:
      self.extension = DRIVE_MIMETYPE_EXTENSIONS[underlyingFile['mimeType']]
    except KeyError:
      self.extension = ''

  def __str__(self):
    return f'{ShadowFile.__str__(self)}.{self.extension}'