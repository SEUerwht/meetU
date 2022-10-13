import os
import uuid
import config
from util.response import response

def file_legal(filename):
    return filename in config.FILE_LEGAL


def upload_file(file):
    if not file:
        return response(msg="没有上传头像", status=401)
    file_suffix = file.filename.split('.')[1].lower()
    if file_legal(file_suffix) == False:
        return response(msg="该文件不合法", status=401)
    name_ = uuid.uuid4().hex
    save_name = f"{name_}.{file_suffix}"
    file.save(config.SAVE_FILE_PATH + save_name)
    file_url = config.BASE_URL + save_name
    return file_url


def delete(file_url):
    if not file_url:
        return
    file_name = file_url.rsplit('/',1)[1]
    file_path = config.SAVE_FILE_PATH + file_name
    if(os.path.exists(file_path)):
        os.remove(file_path)