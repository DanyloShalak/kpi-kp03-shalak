import json
import typer
import httpx


app = typer.Typer()
headers = {'Content-Type': 'application/json'}
base_url = 'http://0.0.0.0:5000/'

directory_catalog = 'directory/'
logfile_catalog = 'logfile/'
binaryfile_catalog = 'binaryfile/'
bufferfile_catalog = 'bufferfile/'
version_catalog = 'version'
move_subcatalog = 'move'


@app.command()
def version():
    try:
        res = httpx.get(base_url + version_catalog)
        print(res.json())
    except Exception:
        print('Error occurred')


@app.command()
def dir_get(path: str):
    try:
        res = httpx.get(base_url + directory_catalog + path)
        print(json.dumps(res.json()))
    except Exception:
        print('Error occurred')


@app.command()
def dir_create(path: str, name: str):
    try:
        data = {'directory_path': path, 'directory_name': name}
        res = httpx.post(base_url + directory_catalog, json=data, headers=headers)
        print(json.dumps(res.json()))
    except Exception:
        print('Error occurred')


@app.command()
def dir_delete(directory_path: str):
    try:
        res = httpx.delete(base_url + directory_catalog + directory_path)
        print(json.dumps(res.json()))
    except Exception:
        print('Error occurred')


@app.command()
def dir_move(directory_path: str, destination_path: str):
    try:
        data = {'directory_path': directory_path, 'destination_path': destination_path}
        res = httpx.post(base_url + directory_catalog + move_subcatalog, json=data, headers=headers)
        print(json.dumps(res.json()))
    except Exception:
        print('Error occurred')


@app.command()
def log_create(path: str, file_name: str):
    try:
        data = {'directory_path': path, 'file_name': file_name}
        res = httpx.post(base_url + logfile_catalog, json=data, headers=headers)
        print(json.dumps(res.json()))
    except Exception:
        print('Error occurred')


@app.command()
def log_log(file_path: str, log_line: str):
    try:
        data = {'log_file_path': file_path, 'log_line': log_line}
        res = httpx.post(base_url + logfile_catalog + 'log', json=data, headers=headers)
        print(json.dumps(res.json()))
    except Exception:
        print('Error occurred')


@app.command()
def log_get(file_path: str):
    try:
        res = httpx.get(base_url + logfile_catalog + file_path)
        print(json.dumps(res.json()))
    except Exception:
        print('Error occurred')


@app.command()
def log_move(file_path: str, destination_path: str):
    try:
        data = {'log_file_path': file_path, 'destination_path': destination_path}
        res = httpx.post(base_url + logfile_catalog + move_subcatalog, json=data, headers=headers)
        print(json.dumps(res.json()))
    except Exception:
        print('Error occurred')


@app.command()
def log_delete(file_path: str):
    try:
        res = httpx.delete(base_url + logfile_catalog + file_path)
        print(json.dumps(res.json()))
    except Exception:
        print('Error occurred')


@app.command()
def bin_create(path: str, file_name: str, content: str):
    try:
        data = {'directory_path': path, 'file_name': file_name, 'content': content}
        res = httpx.post(base_url + binaryfile_catalog, json=data, headers=headers)
        print(json.dumps(res.json()))
    except Exception:
        print('Error occurred')


@app.command()
def bin_get(file_path: str):
    try:
        res = httpx.get(base_url + binaryfile_catalog + file_path)
        print(json.dumps(res.json()))
    except Exception:
        print('Error occurred')


@app.command()
def bin_delete(file_path: str):
    try:
        res = httpx.delete(base_url + binaryfile_catalog + file_path)
        print(json.dumps(res.json()))
    except Exception:
        print('Error occurred')


@app.command()
def bin_move(file_path: str, destination_path: str):
    try:
        data = {'binary_file_path': file_path, 'destination_path': destination_path}
        res = httpx.post(base_url + binaryfile_catalog + move_subcatalog, json=data, headers=headers)
        print(json.dumps(res.json()))
    except Exception:
        print('Error occurred')


@app.command()
def buff_create(path: str, file_name: str):
    try:
        data = {'directory_path': path, 'file_name': file_name}
        res = httpx.post(base_url + bufferfile_catalog, json=data, headers=headers)
        print(json.dumps(res.json()))
    except Exception:
        print('Error occurred')


@app.command()
def buff_delete(file_path: str):
    try:
        res = httpx.delete(base_url + bufferfile_catalog + file_path)
        print(json.dumps(res.json()))
    except Exception:
        print('Error occurred')


@app.command()
def buff_get(file_path: str):
    try:
        res = httpx.get(base_url + bufferfile_catalog + file_path)
        print(json.dumps(res.json()))
    except Exception:
        print('Error occurred')



@app.command()
def buff_move(file_path: str, destination_path: str):
    try:
        data = {'buffer_file_path': file_path, 'destination_path': destination_path}
        res = httpx.post(base_url + bufferfile_catalog + move_subcatalog, json=data, headers=headers)
        print(json.dumps(res.json()))
    except Exception:
        print('Error occurred')


@app.command()
def buff_push(file_path: str, push_element: str):
    try:
        data = {'buffer_file_path': file_path, 'push_element': push_element}
        res = httpx.post(base_url + bufferfile_catalog + 'push', json=data, headers=headers)
        print(json.dumps(res.json()))
    except Exception:
        print('Error occurred')


@app.command()
def buff_pop(file_path: str):
    try:
        res = httpx.get(base_url + bufferfile_catalog + 'pop/' + file_path)
        print(json.dumps(res.json()))
    except Exception:
        print('Error occurred')




if __name__ == "__main__":
    app()
