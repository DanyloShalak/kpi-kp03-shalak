Task 1.
Create in-memory File System (FS). The file system consists of 4 types of nodes: 

Directory - can contain other directories and files. Directory can be empty or can have some elements. Number of elements in the directory should be <= DIR_MAX_ELEMS 
Allowed operations:
Create directory
Delete directory
List files and subdirectories
Move file or subdirectory to another location

Binary file - just an immutable file that contains some information.  
Allowed operations:
Create file
Delete file
Move file
Readfile (returns file content)

Log text file - a text file that can be modified by appending lines to the end of the file.
Allowed operations:
Create file
Delete file
Move file
Readfile (returns file content)
Append a line to the end of the file

Buffer file - this is a special type of file that works like a queue. Some threads push elements to the file the other pop elements from the file. The number of element in the file is <= MAX_BUF_FILE_SIZE
Allowed operations:
Create file
Delete file
Move file
Push element
Consume element


Task 2.

Using the API defined above create some file system topology that contains at least 2 nested folders and several instances of all types of the FS nodes
