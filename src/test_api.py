from app import client
import json


mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}


def test_create_directory():
    data = {
        'directory_path': 'root/',
        'directory_name': 'subdir1'
    }
    response = client.post('/directory/', data=json.dumps(data), headers=headers)
    assert response.status_code == 200


def test_create_binary_file():
    data = {
        'directory_path': 'root/subdir1',
        'file_name': 'binfile',
        'content': 'text ' * 10
    }

    response = client.post('/binaryfile/', data=json.dumps(data), headers=headers)
    assert response.status_code == 200


def test_create_buffer_file():
    data = {
        'directory_path': 'root/subdir1',
        'file_name': 'bufffile'
    }
    response = client.post('/bufferfile/', data=json.dumps(data), headers=headers)
    assert response.status_code == 200


def test_create_log_file():
    data = {
        'directory_path': 'root/subdir1',
        'file_name': 'logfile'
    }
    response = client.post('/logfile/', data=json.dumps(data), headers=headers)
    assert response.status_code == 200


def test_add_file_with_same_name():
    data = {
        'directory_path': 'root/subdir1',
        'file_name': 'logfile'
    }
    response = client.post('/logfile/', data=json.dumps(data), headers=headers)
    assert response.status_code == 400


def test_add_dir_with_same_name():
    data = {
        'directory_path': 'root/',
        'directory_name': 'subdir1'
    }
    response = client.post('/directory/', data=json.dumps(data), headers=headers)
    assert response.status_code == 400


def test_add_file_to_non_existent_directory():
    data = {
        'directory_path': 'root123/zdsasd/asdfasd',
        'file_name': 'logfile'
    }
    response = client.post('/logfile/', data=json.dumps(data), headers=headers)
    assert response.status_code == 400


def test_add_file_with_wrong_name():
    data = {
        'directory_path': 'root123/subdir1',
        'file_name': 'logfile/sdfsd'
    }
    response = client.post('/logfile/', data=json.dumps(data), headers=headers)
    assert response.status_code == 400


def test_get_directory():
    response = client.get('/directory/root/subdir1')
    assert len(response.json) == 3
    assert response.status_code == 200


def test_get_binary_file():
    response = client.get('/binaryfile/root/subdir1/binfile')
    assert response.status_code == 200
    assert response.json['name'] == 'binfile'
    assert response.json['itemType'] == 'BinaryFile'
    assert response.json['isDir'] is False
    assert response.json['file_content'] == 'text ' * 10


def test_get_log_file():
    response = client.get('/logfile/root/subdir1/logfile')
    assert response.status_code == 200
    assert response.json['name'] == 'logfile'
    assert response.json['itemType'] == 'LogFile'
    assert response.json['isDir'] is False
    assert response.json['file_content'] == ''


def test_get_buffer_file():
    response = client.get('/bufferfile/root/subdir1/bufffile')
    assert response.status_code == 200
    assert response.json['name'] == 'bufffile'
    assert response.json['itemType'] == 'BufferFile'
    assert response.json['isDir'] is False
    assert len(response.json['file_content']) == 0


def test_append_line_to_log_file():
    data = {
        'log_file_path': 'root/subdir1/logfile',
        'log_line': 'logfile1'
    }

    response = client.post('/logfile/log', data=json.dumps(data), headers=headers)
    assert response.status_code == 200

    data['log_line'] = 'logfile2'

    response = client.post('/logfile/log', data=json.dumps(data), headers=headers)
    assert response.status_code == 200

    response = client.get('/logfile/root/subdir1/logfile')
    assert response.status_code == 200
    assert response.json['name'] == 'logfile'
    assert response.json['itemType'] == 'LogFile'
    assert response.json['isDir'] is False
    assert len(response.json['file_content'].split("\n")) == 2


def test_log_to_non_existing_file():
    data = {
        'log_file_path': 'root/subdir1/logfile/sdkfsdf',
        'log_line': 'logfile1'
    }

    response = client.post('/logfile/log', data=json.dumps(data), headers=headers)
    assert response.status_code == 400


def test_log_to_not_log_file():
    data = {
        'log_file_path': 'root/subdir1/bufffile',
        'log_line': 'logfile1'
    }

    response = client.post('/logfile/log', data=json.dumps(data), headers=headers)
    assert response.status_code == 400


def test_push_to_buffer_file():
    data = {
        'buffer_file_path': 'root/subdir1/bufffile',
        'push_element': 'element 1'
    }

    response = client.post('/bufferfile/push', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    data['push_element'] = 'element 2'
    response = client.post('/bufferfile/push', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    data['push_element'] = 'element 3'
    response = client.post('/bufferfile/push', data=json.dumps(data), headers=headers)
    assert response.status_code == 200

    response = client.get('/bufferfile/root/subdir1/bufffile')
    assert response.status_code == 200
    assert response.json['name'] == 'bufffile'
    assert response.json['itemType'] == 'BufferFile'
    assert response.json['isDir'] is False
    assert len(response.json['file_content']) == 3


def test_push_to_not_buffer_file():
    data = {
        'buffer_file_path': 'root/subdir1/logfile',
        'push_element': 'element 1'
    }

    response = client.post('/bufferfile/push', data=json.dumps(data), headers=headers)
    assert response.status_code == 400


def test_push_to_non_existing_file():
    data = {
        'buffer_file_path': 'root/subdir1/logfile/sdfsdf',
        'push_element': 'element 1'
    }

    response = client.post('/bufferfile/push', data=json.dumps(data), headers=headers)
    assert response.status_code == 400


def test_pop_from_buffer_file():
    response = client.get('/bufferfile/pop/root/subdir1/bufffile')
    assert response.status_code == 200
    assert response.json['pop_element'] == 'element 1'

    response = client.get('/bufferfile/pop/root/subdir1/bufffile')
    assert response.status_code == 200
    assert response.json['pop_element'] == 'element 2'

    response = client.get('/bufferfile/root/subdir1/bufffile')
    assert response.status_code == 200
    assert response.json['name'] == 'bufffile'
    assert response.json['itemType'] == 'BufferFile'
    assert response.json['isDir'] is False
    assert len(response.json['file_content']) == 1


def test_pop_from_not_buffer_file():
    response = client.get('/bufferfile/pop/root/subdir1/logfile')
    assert response.status_code == 400


def test_move_file():
    data = {
        'log_file_path': 'root/subdir1/logfile',
        'destination_path': 'root/'
    }
    response = client.post('/logfile/move', data=json.dumps(data), headers=headers)
    assert response.status_code == 200


def test_non_existent_move_file():
    data = {
        'log_file_path': 'root/subdir1/logfile/23432412',
        'destination_path': 'root/'
    }
    response = client.post('/logfile/move', data=json.dumps(data), headers=headers)
    assert response.status_code == 400


def test_move_wrong_type_file():
    data = {
        'log_file_path': 'root/subdir1/bufffile',
        'destination_path': 'root/'
    }
    response = client.post('/logfile/move', data=json.dumps(data), headers=headers)
    assert response.status_code == 400


def test_move_file_to_dir_with_same_name_item():
    data = {
        'directory_path': 'root/subdir1',
        'file_name': 'logfile'
    }
    response = client.post('/logfile/', data=json.dumps(data), headers=headers)
    assert response.status_code == 200

    data = {
        'log_file_path': 'root/subdir1/logfile',
        'destination_path': 'root/'
    }
    response = client.post('/logfile/move', data=json.dumps(data), headers=headers)
    assert response.status_code == 400