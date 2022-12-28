from flask import Flask, jsonify, request, redirect, url_for
from fs import FileSystem, Directory, BinaryFile, BufferFile, LogFile
from service import get_items, get_file_data

app = Flask(__name__)
client = app.test_client()
fs = FileSystem()


@app.get("/version")
def get_version():
    return '1.0'


@app.get("/directory/<path:directory_path>")
def get_directory(directory_path):
    directory = fs.findDir(directory_path)

    if directory is None:
        return {'error_message': 'Directory not found'}, 400

    items = directory.items()
    return get_items(items)


@app.get("/bufferfile/<path:file_path>")
def get_buffer_file(file_path):
    buffer_file = fs.findFile(file_path)

    if buffer_file is None or type(buffer_file) is not BufferFile:
        return {'error_message': 'File not found'}, 400

    return jsonify(get_file_data(buffer_file))


@app.get("/logfile/<path:file_path>")
def get_log_file(file_path):
    log_file = fs.findFile(file_path)

    if log_file is None or type(log_file) is not LogFile:
        return {'error_message': 'File not found'}, 400

    return jsonify(get_file_data(log_file))


@app.get("/binaryfile/<path:file_path>")
def get_binary_file(file_path):
    binary_file = fs.findFile(file_path)

    if binary_file is None or type(binary_file) is not BinaryFile:
        return {'error_message': 'File not found'}, 400

    return jsonify(get_file_data(binary_file))


@app.delete("/directory/<path:directory_path>")
def delete_directory(directory_path):
    directory = fs.findDir(directory_path)

    if directory is None or type(directory) is not Directory:
        return {'error_message': 'Directory not found'}, 400

    is_removed = fs.removeItem(directory_path)

    if is_removed:
        return {'success': True}
    else:
        return {'error_message': 'Directory could not be removed'}, 400


@app.delete("/binaryfile/<path:file_path>")
def delete_binaryfile(file_path):
    bin_file = fs.findFile(file_path)

    if bin_file is None or type(bin_file) is not BinaryFile:
        return {'error_message': 'BinaryFile not found'}, 400

    fs.removeItem(file_path)
    return {'success': True}


@app.delete("/logfile/<path:file_path>")
def delete_logfile(file_path):
    log_file = fs.findFile(file_path)

    if log_file is None or type(log_file) is not LogFile:
        return {'error_message': 'LogFile not found'}, 400

    fs.removeItem(file_path)
    return {'success': True}


@app.delete("/bufferfile/<path:file_path>")
def delete_bufferfile(file_path):
    buffer_file = fs.findFile(file_path)

    if buffer_file is None or type(buffer_file) is not BufferFile:
        return {'error_message': 'BufferFile not found'}, 400

    fs.removeItem(file_path)
    return {'success': True}


@app.post("/directory/")
def create_directory():
    json = request.get_json()
    directory_path = json.get('directory_path')
    directory_name = json.get('directory_name')
    new_directory = Directory(directory_name)
    is_created = fs.addItem(new_directory, directory_path)

    if is_created:
        return {'success': True}
    else:
        return {'error_message': 'Directory creation failed'}, 400


@app.post("/bufferfile/")
def create_bufferfile():
    json = request.get_json()
    directory_path = json.get('directory_path')
    buffer_file_name = json.get('file_name')
    new_file = BufferFile(buffer_file_name)
    is_created = fs.addItem(new_file, directory_path)

    if is_created:
        return {'success': True}
    else:
        return {'error_message': 'File creation failed'}, 400


@app.post("/logfile/")
def create_logfile():
    json = request.get_json()
    directory_path = json.get('directory_path')
    binary_file_name = json.get('file_name')
    new_file = LogFile(binary_file_name, "")
    is_created = fs.addItem(new_file, directory_path)

    if is_created:
        return {'success': True}
    else:
        return {'error_message': 'File creation failed'}, 400


@app.post("/binaryfile/")
def create_binaryfile():
    json = request.get_json()
    directory_path = json.get('directory_path')
    binary_file_name = json.get('file_name')
    file_content = json.get('content')
    new_file = BinaryFile(binary_file_name, file_content)
    is_created = fs.addItem(new_file, directory_path)

    if is_created:
        return {'success': True}
    else:
        return {'error_message': 'File creation failed'}, 400


@app.post("/logfile/log")
def log_line_to_file():
    json = request.get_json()
    log_file_path = json.get('log_file_path')
    log_line = json.get('log_line')

    if log_line is None or log_file_path is None:
        return {'error_message': 'Invalid data'}, 400

    log_file = fs.findFile(log_file_path)

    if log_file is None:
        return {'error_message': 'File not found'}, 400

    if type(log_file) is not LogFile:
        return {'error_message': 'File do not supports logging'}, 400

    log_file.append(log_line)
    return {'success': True}


@app.post("/bufferfile/push")
def push_element_to_buffer_file():
    json = request.get_json()
    buffer_file_path = json.get('buffer_file_path')
    element = json.get('push_element')

    if buffer_file_path is None or element is None:
        return {'error_message': 'Invalid data'}, 400

    buffer_file = fs.findFile(buffer_file_path)

    if buffer_file is None:
        return {'error_message': 'File not found'}, 400

    if type(buffer_file) is not BufferFile:
        return {'error_message': 'This operation can not be done with this file'}, 400

    is_pushed = buffer_file.push(element)

    if is_pushed:
        return {'success': True}
    else:
        return {'error_message': 'Element can not be pushed'}, 400


@app.get("/bufferfile/pop/<path:buffer_file_path>")
def pop_element_from_buffer_file(buffer_file_path):
    buffer_file = fs.findFile(buffer_file_path)

    if buffer_file is None:
        return {'error_message': 'File not found'}, 400

    if type(buffer_file) is not BufferFile:
        return {'error_message': 'This operation can not be done with this file'}, 400

    pop_element = buffer_file.pop()

    if pop_element is not None:
        return {'pop_element': pop_element}
    else:
        return {'error_message': 'Buffer file is empty'}, 400


@app.post("/bufferfile/move")
def move_bufferfile():
    json = request.get_json()
    buffer_file_path = json.get('buffer_file_path')
    destination_path = json.get('destination_path')

    buffer_file = fs.findFile(buffer_file_path)

    if buffer_file is None or type(buffer_file) is not BufferFile:
        return {'error_message': 'File not found'}, 400

    is_moved = fs.moveItem(buffer_file_path, destination_path)

    if is_moved:
        return {'success': True}
    else:
        return {'error_message': f'File can not be moved to {destination_path}'}, 400


@app.post("/directory/move")
def move_directory():
    json = request.get_json()
    directory_path = json.get('directory_path')
    destination_path = json.get('destination_path')

    directory = fs.findDir(directory_path)

    if directory is None or type(directory) is not Directory:
        return {'error_message': 'Directory not found'}, 400

    is_moved = fs.moveItem(directory_path, destination_path)

    if is_moved:
        return {'success': True}
    else:
        return {'error_message': f'Directory can not be moved to {destination_path}'}, 400


@app.post("/logfile/move")
def move_logfile():
    json = request.get_json()
    log_file_path = json.get('log_file_path')
    destination_path = json.get('destination_path')

    log_file = fs.findFile(log_file_path)

    if log_file is None or type(log_file) is not LogFile:
        return {'error_message': 'File not found'}, 400

    is_moved = fs.moveItem(log_file_path, destination_path)

    if is_moved:
        return {'success': True}
    else:
        return {'error_message': f'File can not be moved to {destination_path}'}, 400


@app.post("/binaryfile/move")
def move_binaryfile():
    json = request.get_json()
    binary_file_path = json.get('binary_file_path')
    destination_path = json.get('destination_path')

    binary_file = fs.findFile(binary_file_path)

    if binary_file is None or type(binary_file) is not BinaryFile:
        return {'error_message': 'File not found'}, 400

    is_moved = fs.moveItem(binary_file_path, destination_path)

    if is_moved:
        return {'success': True}
    else:
        return {'error_message': f'File can not be moved to {destination_path}'}, 400


if __name__ == '__main__':
    app.run(host='0.0.0.0')
