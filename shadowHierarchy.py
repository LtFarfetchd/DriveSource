from constantTypes import *
from typing import Dict, Any

class ShadowHierarchy:
  def __init__(self, shadowRoot):
    self.root = shadowRoot
    self.target = None

class ShadowFile:
  def __init__(self, driveId: str, displayName: str, parentDir: ShadowFile, underlyingFile: DriveFile):
    self.driveId = driveId
    self.displayName = displayName
    self.parentDir = parentDir
    self.children = {}
    self.underlyingFile = underlyingFile

  def __str__(self):
    return self.displayName

class ShadowDir(ShadowFile):
  def __init__(self, driveId: str, displayName: str, parentDir: ShadowDir, underlyingFile: dict):
    ShadowFile.__init__(self, driveId, displayName, parentDir, underlyingFile)
    self.synced = False

  def addChild(self, shadowFile):
    self.children[shadowFile.displayName.lower()] = shadowFile

class ShadowNonDir(ShadowFile):
  def __init__(self, driveId: str, displayName: str, parentDir: ShadowDir, underlyingFile: dict):
    ShadowFile.__init__(self, driveId, displayName, parentDir, underlyingFile)
    try:
      self.extension = DRIVE_MIMETYPE_EXTENSIONS[underlyingFile['mimeType']]
    except KeyError:
      self.extension = ''

  def __str__(self):
    return f'{ShadowFile.__str__(self)}.{self.extension}'