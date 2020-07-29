class ShadowHierarchy:
  def __init__(self, shadowRoot):
    self.shadowRoot = shadowRoot

  def getRoot(self):
    return self.shadowRoot

class ShadowFile:
  def __init__(self, driveId, displayName, parentDir, underlyingFile):
    self.driveId = driveId
    self.displayName = displayName
    self.parentDir = parentDir
    self.children = {}
    self.underlyingFile = underlyingFile

  def getId(self):
    return self.driveId

  def getName(self):
    return self.displayName

  def getParent(self):
    return self.parentDir

  def addChild(self, newChild):
    self.children[newChild.getName().lower()] = newChild

  def getChildren(self):
    return self.children

  def getUnderlying(self):
    return self.underlyingFile

class ShadowDir(ShadowFile):
  pass

class ShadowNonDir(ShadowFile):
  def __init__(self, driveId, displayName, parentDir, underlyingFile):
    ShadowFile.__init__(self, driveId, displayName, parentDir, underlyingFile)
    self.mimeType = underlyingFile['mimeType']

  def getMimeType(self):
    return self.getMimeType