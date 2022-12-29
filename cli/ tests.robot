*** Settings ***
Library  Process
Library  JSONLibrary

*** Test Case ***
Create Directory
    ${result}=     RUN PROCESS  python3    app.py  dir-create  root/   dir76
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Create Binary File
    ${result}=     RUN PROCESS  python3    app.py  bin-create  root/   bin1     content
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Create Log File
    ${result}=     RUN PROCESS  python3    app.py  log-create  root/   log1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Create Buffer File
    ${result}=     RUN PROCESS  python3    app.py  buff-create  root/   buff1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Create Directory With Same Name
    ${result}=     RUN PROCESS  python3    app.py  dir-create  root/   dir76
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json["error_message"]}    Directory creation failed

Create File With Same Name
    ${result}=     RUN PROCESS  python3    app.py  log-create  root/   log1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json["error_message"]}    File creation failed


Create Directory With With Wrong Path
    ${result}=     RUN PROCESS  python3    app.py  dir-create  root/asdfsd/asdasd   dir76
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json["error_message"]}    Directory creation failed

Delete Directory
    ${result}=     RUN PROCESS  python3    app.py  dir-delete  root/dir76
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Delete Binary File
    ${result}=     RUN PROCESS  python3    app.py  bin-delete  root/bin1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Delete Log File
    ${result}=     RUN PROCESS  python3    app.py  log-delete   root/log1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Delete Buffer File
    ${result}=     RUN PROCESS  python3    app.py  buff-delete  root/buff1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Delete Not Existing File
    ${result}=     RUN PROCESS  python3    app.py  log-delete  root/sdfsdf/sdfsdf
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json['error_message']}   LogFile not found

Delete Not Existing Directory
    ${result}=     RUN PROCESS  python3    app.py  dir-delete  root/sdfsdf/sdfsdf
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json['error_message']}   Directory not found

Delete Wrong File Type
    RUN PROCESS  python3    app.py  log-create  root/   log1
    ${result}=     RUN PROCESS  python3    app.py  buff-delete  root/log1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json['error_message']}   BufferFile not found

Log Line To LogFile
    ${result}=  RUN PROCESS  python3    app.py  log-log  root/log1  line
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Log Line To Not LogFile
    RUN PROCESS  python3    app.py  buff-create  root/   buff1
    ${result}=  RUN PROCESS  python3    app.py  log-log  root/buff1  line
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json['error_message']}    File do not supports logging

Push Element To BufferFile
    ${result}=  RUN PROCESS  python3    app.py  buff-push  root/buff1  element1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Push Element To Not BufferFile
    ${result}=  RUN PROCESS  python3    app.py  buff-push  root/log1    element
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json['error_message']}    This operation can not be done with this file

Pop Element From BufferFile
    ${result}=  RUN PROCESS  python3    app.py  buff-pop  root/buff1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json['pop_element']}  element1

Pop Element To Not BufferFile
    ${result}=  RUN PROCESS  python3    app.py  buff-pop  root/log1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json['error_message']}    This operation can not be done with this file

Move Directory
    RUN PROCESS  python3    app.py  dir-create  root/   dir1
    RUN PROCESS  python3    app.py  dir-create  root/   dir2
    ${result}=  RUN PROCESS  python3    app.py  dir-move    root/dir2  root/dir1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Move Directory To Not Existing Directory
    ${result}=  RUN PROCESS  python3    app.py  dir-move    root/dir1/dir2  dsfsdfsdfasdf/asdfsdaf
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json['error_message']}    Directory can not be moved to dsfsdfsdfasdf/asdfsdaf

Move Not Existing Directory
    ${result}=  RUN PROCESS  python3    app.py  dir-move    dsfsdfsdfasdf/asdfsdaf    root/dir1/dir2
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json['error_message']}    Directory not found

Move File
    ${result}=  RUN PROCESS  python3    app.py  log-move    root/log1   root/dir1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Move Wrong Type File
    ${result}=  RUN PROCESS  python3    app.py  log-move    root/buff1   root/dir1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json['error_message']}  File not found

Move Not Existing File
    ${result}=  RUN PROCESS  python3    app.py  log-move    root/buff1sdf/asd   root/dir1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json['error_message']}  File not found

Move File To Not Existing Directory
    ${result}=  RUN PROCESS  python3    app.py  buff-move    root/buff1   root/dir1/asdas
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json['error_message']}    File can not be moved to root/dir1/asdas

Get Directory Content
    ${result}=  RUN PROCESS  python3    app.py  dir-get    root/
    ${json}=   Convert String to JSON  ${result.stdout}
    ${count}=   Get length  ${json}
    should be equal as integers  ${count}   2

Get Directory Content Not From Directory
    ${result}=  RUN PROCESS  python3    app.py  dir-get    root/buff1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json['error_message']}    Directory not found

Get Binary File Content
    RUN PROCESS  python3    app.py  bin-create  root/   bin1     some content
    ${result}=     RUN PROCESS  python3    app.py  bin-get  root/bin1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json['file_content']}    some content

Get Binary File Content Not From File Content
    ${result}=     RUN PROCESS  python3    app.py  bin-get  root/bin1/sdfsd/sdf
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json['error_message']}    File not found

Get Binary File Content From File Type
    ${result}=     RUN PROCESS  python3    app.py  bin-get  root/buff1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json['error_message']}    File not found