import queue
import constants


class FSItem:
  def __init__(self, itemName : str) -> None:
    self.__itemName = itemName
    self._isDir = False

  def getName(self) -> str:
    return self.__itemName

  def isDir(self) -> bool:
    return self._isDir


class BinaryFile(FSItem):
  def __init__(self, fileName : str, fileContent : str) -> None:
    self._content = fileContent
    super().__init__(fileName)

  def read(self) -> str:
    return self._content


class LogFile(BinaryFile):
  def __init__(self, fileName : str, fileContent : str) -> None:
    super().__init__(fileName, fileContent)

  def append(self, line) -> None:
    self._content += f"\n{line}"


class BufferFile(FSItem):
  def __init__(self, fileName : str) -> None:
    self.__buffer = queue.Queue()
    self.__usedStorage = 0;
    super().__init__(fileName)

  def push(self, element :str) -> bool:
    if (self.__usedStorage + len(element)) < constants.MAX_BUF_FILE_SIZE:
      self.__buffer.put(element)
      self.__usedStorage += len(element)
      return True
    else:
      return False

  def pop(self) -> str:
    if self.__buffer.empty():
      return None
    else:
      element = self.__buffer.get()
      self.__usedStorage -= len(element)
      return element


class Directory(FSItem):
  def __init__(self, itemName: str) -> None:
    super().__init__(itemName)
    self.__items = []
    self.__parent = None
    self.__itemsCount = 0
    self._isDir = True

  def addItem(self, item: FSItem) -> bool:
    
    if self.getItemByName(item.getName()) != None or item == None:
      return False

    if self.__itemsCount < constants.DIR_MAX_ELEMS:
      self.__itemsCount += 1
      self.__items.append(item)
      
      if item.isDir():
        item.setParent(self)

      return True
    
    return False

  def popItem(self, itemName) -> FSItem:
    item = self.getItemByName(itemName)
    self.__items.remove(item)
    return item

  def getItemByName(self, name : str) -> FSItem:
    for item in self.__items:
      if item.getName() == name:
        return  item

    return None
  
  def items(self) -> list:
    return self.__items.copy()

  def setParent(self, newParent):
    self.__parent = newParent
  
  def getParent(self):
    return self.__parent

  
class FileSystem:
  def __init__(self) -> None:
    self.__root = Directory("root")

  def getRoot(self) -> Directory:
    return self.__root

  def addItem(self, item, path : str) -> bool:
    itemDir = self.findDir(path)
    if itemDir == None or item == None:
      return False
    
    return itemDir.addItem(item)

  def removeItem(self, itemPath: str) -> bool:
    if len(itemPath.split('/')) == 1:
      return False

    item = self.__getItemFromDir(itemPath)
    if item == None:
      return False

    return True


  def moveItem(self, itemPath : str, path : str) -> bool:
    itemDir = self.findDir(path)

    if itemDir == None or len(itemPath.split('/')) == 1:
      return False
    
    item = self.__getItemFromDir(itemPath)

    if item == None :
      return False

    return itemDir.addItem(item)
    
  def __getItemFromDir(self, itemPath : str) -> FSItem:
    pathList = itemPath.split('/')
    itemName = pathList.pop()
    itemDirPath = '/'.join(pathList)
    itemDir = self.findDir(itemDirPath)
    item = itemDir.popItem(itemName)
    return item

  def findDir(self, path: str) -> Directory:
    folders = path.split('/')
    rootName = folders.pop(0)

    if self.__root.getName() != rootName:
      return None

    searchedDir = self.__root
    for folder in folders:
      subDir = searchedDir.getItemByName(folder)
      
      if subDir == None or not subDir.isDir():
        return None
      searchedDir = subDir
    
    return searchedDir