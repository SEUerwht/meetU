IS_LOCOLHOST = True
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/meetu?charset=utf8mb4"
NOT_CHECK_URL = [
    "/user/login",
    '/',
    '/user/register'
]
SECURITY_KEY = "dhAfi656grs126Ud7afFYEFH8aesfwa9ahH"
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
EXPIRE_TIME = 7 * 24 * 60 * 60
SAVE_FILE_PATH = "/" if IS_LOCOLHOST else "/MeetU/savefiles/"
FILE_LEGAL = ['png', 'jpg']
BASE_URL = "http://aitmaker.cn:6555/"
HELP_PATH = "/files/help.docx"