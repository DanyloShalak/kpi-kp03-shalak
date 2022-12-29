from fs import FSItem, LogFile, BinaryFile, BufferFile


def get_item_type(item) -> str:
    if item.isDir():
        return 'Directory'

    if type(item) is LogFile:
        return 'LogFile'

    if type(item) is BinaryFile:
        return 'BinaryFile'

    if type(item) is BufferFile:
        return 'BufferFile'

    return 'Unknown'


def get_file_content(file_type: str, file: FSItem):
    if file_type == 'BinaryFile' or file_type == 'LogFile':
        return file.read()

    if file_type == 'BufferFile':
        return file.get_elements()

    return ""


def get_item_info(item: FSItem):
    return {'name': item.getName(), 'isDir': item.isDir(), 'itemType': get_item_type(item)}


def get_items(items: list):
    result = []
    for item in items:
        result.append(get_item_info(item))

    return result


def get_file_data(file):
    file_data = get_item_info(file)
    file_content = get_file_content(file_data['itemType'], file)
    file_data['file_content'] = file_content
    return file_data
