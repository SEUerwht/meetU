IS_LOCOLHOST = True
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/meetu?charset=utf8mb4"
NOT_CHECK_URL = [
    "/user/login",
    '/',
    '/user/register'
]
SECURITY_KEY = "wwanghaitaoqqxqzgrb"
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
EXPIRE_TIME = 7 * 24 * 60 * 60
SAVE_FILE_PATH = "/" if IS_LOCOLHOST else "/"
FILE_LEGAL = ['png','jpg']
BASE_URL = ""
HELP_PATH = "/files/help.docx"