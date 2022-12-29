import fs
import pytest

def test_fsItem():
  item = fs.FSItem("item1")
  assert item.getName() == "item1"

def test_directory_check():
  directory = fs.Directory("dir1")
  assert directory.isDir() == True

def test_log_file():
  logFile = fs.LogFile("log1", "first line")
  logFile.append("second line")
  logFile.append("third line")
  logText = "first line" + "\n" + "second line" + "\n" + "third line"
  assert logFile.read() == logText
  assert logFile.isDir() == False

def test_Buffer_file():
  buffFile = fs.BufferFile("buff1")
  buffFile.push("item1")
  buffFile.push(2)
  buffFile.push('c')
  assert (buffFile.pop() == None) == False
  assert buffFile.pop() == 2
  assert buffFile.pop() == 'c'
  assert buffFile.pop() == None
  assert buffFile.isDir() == False

def test_binary_file():
  binFile = fs.BinaryFile("bin1", "content" * 10)
  assert (binFile.read() == "content" * 11) == False
  assert binFile.isDir() == False

def test_directory_items():
  directrory = fs.Directory("dir1")
  logFile = fs.LogFile("logFile", "first line")
  buffFile = fs.BufferFile("buff1")
  binFile = fs.BinaryFile("bin1", "content" * 3)
  logFileWithSameName = fs.LogFile("logFile", "first line")
  assert directrory.addItem(logFile) == True
  assert directrory.addItem(binFile) == True
  assert directrory.addItem(buffFile) == True
  assert directrory.addItem(logFileWithSameName) == False
  assert len(directrory.items()) == 3
  with pytest.raises(ValueError):
    directrory.popItem("non-existent")

def test_directories_parents():
  Dir = fs.Directory("main")
  subDir = fs.Directory("subDir")
  subsubDir = fs.Directory("subsubDir")
  Dir.addItem(subDir)
  subDir.addItem(subsubDir)
  assert subsubDir.getParent().getName() == "subDir"
  assert subDir.getParent().getName() == "main"
  assert Dir.getParent() == None

def test_directory_max_item_size():
  d = fs.Directory("dir1")
  for i in range (1,101):
    assert d.addItem(fs.BinaryFile(str(i), "content")) == True
  
  assert d.addItem(fs.BinaryFile("101", "content")) == False


def test_fs():
  f = fs.FileSystem()
  f.addItem(fs.Directory("dir1"), "root")
  f.addItem(fs.Directory("dir2"), "root")

  assert f.findDir("root/dir1").getName() == "dir1"
  assert f.findDir("root/dir2").getName() == "dir2"
  assert len(f.getRoot().items()) == 2

  f.addItem(fs.Directory("subdir1"), "root/dir1")
  f.addItem(fs.Directory("subdir2"), "root/dir2")

  assert f.findDir("root/dir1/subdir1").getName() == "subdir1"
  assert f.findDir("root/dir2/subdir2").getName() == "subdir2"
  assert f.addItem(fs.BinaryFile("bin1", "content"), "root/dir1/subdir1") == True

  f.moveItem("root/dir1/subdir1/bin1", "root/dir2/subdir2")
  assert f.findDir("root/dir1/subdir1").getItemByName("bin1") == None
  assert f.findDir("root/dir2/subdir2").getItemByName("bin1") != None

  f.removeItem("root/dir2/subdir2/bin1")
  assert f.findDir("root/dir2/subdir2").getItemByName("bin1") == None

  f.addItem(fs.LogFile("log1", "content"), "root/dir2/subdir2")
  f.addItem(fs.BufferFile("buff1"), "root/dir2/subdir2")
  assert len(f.findDir("root/dir2/subdir2").items()) == 2

  f.moveItem("root/dir2/subdir2", "root")
  assert len(f.getRoot().items()) == 3
  assert f.findDir("root/subdir2").getName() == "subdir2"
  assert f.findDir("root/dir2/subdir2") == None
  assert f.findDir("root/subdir2").getParent() == f.getRoot()