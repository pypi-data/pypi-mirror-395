from typing import NamedTuple, Optional

from ftplib import FTP, FTP_TLS
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, ThrottledDTPHandler
from pyftpdlib.servers import FTPServer

from robertcommonbasic.basic.os.file import get_file_folder, get_file_name, check_file_exist, scan_files, check_is_file
from robertcommonbasic.basic.os.path import create_dir_if_not_exist

'''
server
pip installl pyftpdlib

Read permissions:
"e" = change directory (CWD, CDUP commands)
"l" = list files (LIST, NLST, STAT, MLSD, MLST, SIZE commands)
"r" = retrieve file from the server (RETR command)
Write permissions:

"a" = append data to an existing file (APPE command)
"d" = delete file or directory (DELE, RMD commands)
"f" = rename file or directory (RNFR, RNTO commands)
"m" = create directory (MKD command)
"w" = store a file to the server (STOR, STOU commands)
"M" = change file mode / permission (SITE CHMOD command) New in 0.7.0
"T" = change file modification time (SITE MFMT command) New in 1.5.3

注意Linux模式下 FTP需要使用主动模式连接 一般FTP为被动连接

'''

'''
client
tp.set_debuglevel(2)       #打开调试级别2，显示详细信息
ftp.set_pasv(0)           #0主动模式 1 #被动模式
print ftp.getwelcome()      #打印出欢迎信息
ftp.cmd("xxx/xxx")         #更改远程目录
ftp.set_debuglevel(0)       #关闭调试模式
ftp.quit()              #退出ftp
ftp.dir()               #显示目录下文件信息
ftp.mkd(pathname)          #新建远程目录
ftp.pwd()               #返回当前所在位置
ftp.rmd(dirname)          #删除远程目录
ftp.delete(filename)        #删除远程文件
ftp.rename(fromname, toname)   #将fromname修改名称为toname。
'''


class FTPEventHandler(FTPHandler):

    def on_connect(self):
        pass

    def on_disconnect(self):
        # do something when client disconnects
        pass

    def on_login(self, username):
        # do something when user login
        pass

    def on_logout(self, username):
        # do something when user logs out
        pass

    def on_file_sent(self, file):
        # do something when a file has been sent
        pass

    def on_file_received(self, file):
        # do something when a file has been received
        pass

    def on_incomplete_file_sent(self, file):
        # do something when a file is partially sent
        pass

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        pass


class FtpConfig(NamedTuple):
    HOST: str
    PORT: int
    USER: str = ''
    PSW: str = ''
    USERS: list = []        # 用户列表
    IS_CLIENT: bool = True  # 是否客户端模式
    IS_SSL: bool = False    # ssl模式
    ANONY_MOUS: str = ''    # 匿名路径
    UPLOAD_SPEED: int = 300*1024        # 上传速度
    DOWN_SPEED: int = 300*1024        # 下载速度
    CONNECT_LIMIT: int = 150        # 最大连接数
    PER_IP_LIMIT: int = 10          # 单个ip最大连接数
    PASSIVE_PORTS: tuple = (2000, 2200)        # 被动端口范围
    ENABLE_LOG: int = 0
    WELCOME: str = 'Welcome to my ftp'    # 欢迎信息
    DEBUG_LEVEL: int = 0
    BUFFER_SIZE: int = 8192
    TIMEOUT: float = 60  # 超时设置


class FtpAccessor:

    def __init__(self, config: FtpConfig):
        self.config = config
        self.client = None

    def __del__(self):
        self.exit()

    def exit(self):
        self.close()

    def close(self):
        try:
            if self.client is not None:
                if self.config.IS_CLIENT is True:
                    self.client.quit()
                else:
                    self.client.close_all()
        finally:
            del self.client
            self.client = None

    def start(self):
        if self.get_client() is not None and self.config.IS_CLIENT is False:
            self.client.serve_forever()

    def get_client(self):
        if self.config.IS_CLIENT is True:
            if self.client is None:
                client = FTP_TLS(timeout=self.config.TIMEOUT) if self.config.IS_SSL is True else FTP(timeout=self.config.TIMEOUT)
                client.set_debuglevel(self.config.DEBUG_LEVEL)
                client.connect(self.config.HOST, self.config.PORT)
                if self.config.IS_SSL is True:
                    client.auth()
                    client.prot_p()  # switch to secure data connection

                if len(self.config.USER) > 0:
                    client.login(self.config.USER, self.config.PSW)

                # 设置ftp为被动模式，解决有时候ftp会卡住问题
                client.set_pasv(1)
                self.client = client
        else:
            if self.client is None:
                authorizer = DummyAuthorizer()
                for user in self.config.USERS:
                    authorizer.add_user(user.get('name'), user.get('psw'), user.get('folder'), user.get('role'))
                if len(self.config.ANONY_MOUS) > 0:
                    authorizer.add_anonymous(self.config.ANONY_MOUS)

                throttled = ThrottledDTPHandler
                throttled.read_limit = self.config.DOWN_SPEED
                throttled.write_limit = self.config.DOWN_SPEED

                handler = FTPEventHandler
                handler.authorizer = authorizer
                handler.banner = self.config.WELCOME
                handler.passive_ports = range(self.config.PASSIVE_PORTS[0], self.config.PASSIVE_PORTS[1])
                self.client = FTPServer((self.config.HOST, self.config.PORT), handler)
                self.client.max_cons = self.config.CONNECT_LIMIT
                self.client.max_cons_per_ip = self.config.PER_IP_LIMIT
        return self.client

    def pwd(self) -> str:
        """显示当前目录"""
        if self.get_client():
            return self.client.pwd()

    def nlst(self, *args) -> list:
        """显示当前目录下的列表"""
        if self.get_client():
            return self.client.nlst(*args)

    def dir(self, *args):
        """显示当前目录下的目录"""
        if self.get_client():
            #return self.client.retrlines('LIST')
            return self.client.dir(*args)

    def cwd(self, dirname: str):
        """切换目录"""
        if len(dirname) > 0:
            if self.get_client():
                return self.client.cwd(dirname)

    def mkd(self, dirname: str):
        """创建目录"""
        if len(dirname) > 0:
            if self.get_client():
                folder = get_file_folder(dirname)
                if dirname not in self.nlst(folder):
                    self.client.mkd(dirname)

    def rmd(self, dirname: str):
        """删除目录"""
        if len(dirname) > 0:
            if self.get_client():
                folder = get_file_folder(dirname)
                if dirname in self.nlst(folder):
                    self.client.rmd(dirname)

    def rename(self, fromname: str, toname: str):
        """重命名"""
        if self.get_client():
            return self.client.rename(fromname, toname)

    def delete(self, filename: str):
        """删除文件"""
        if self.get_client():
            return self.client.delete(filename)

    def size(self, filename: str):
        """文件大小"""
        if self.get_client():
            return self.client.size(filename)

    def download_file(self, remote_path: str, local_path: str):
        """下载文件"""
        remote_folder = get_file_folder(remote_path)
        remote_name = get_file_name(remote_path)
        if isinstance(remote_folder, str) and len(remote_folder) > 0:
            self.cwd(remote_folder)
        if self.get_client():
            local_folder = get_file_folder(local_path)
            if isinstance(local_folder, str) and len(local_folder) > 0:
                create_dir_if_not_exist(local_folder)
            with open(local_path, 'wb') as f:
                result = self.client.retrbinary(f"RETR {remote_name}", f.write, self.config.BUFFER_SIZE)
                if result.startswith('226'):
                    return True
                raise Exception(f"download fail({result})")

    def download_folder(self, remote_folder: str, local_folder: str):
        """下载目录"""
        create_dir_if_not_exist(local_folder)

        files = self.nlst(remote_folder)
        for index, file in enumerate(files):
            if check_file_exist(file):
                self.download_file(file, f"{local_folder}/{get_file_name(file)}")
            else:
                self.download_folder(file, f"{local_folder}/{get_file_name(file)}")

    def upload_file(self, local_path: str, remote_path: Optional[str] = None):
        """上传文件"""
        if check_file_exist(local_path) is True:
            file_name = get_file_name(local_path)
            if isinstance(remote_path, str) and len(remote_path) > 0:
                file_folder = get_file_folder(remote_path)
                file_name = get_file_name(remote_path)
                if isinstance(file_folder, str) and len(file_folder) > 0:
                    self.cwd(file_folder)

            if self.get_client():
                with open(local_path, 'rb') as f:
                    result = self.client.storbinary(f"STOR {file_name}", f, self.config.BUFFER_SIZE)
                    if result.startswith('226'):
                        return True
                    raise Exception(f"upload fail({result})")

    def upload_folder(self, local_folder: str, remote_folder: Optional[str] = None):
        """上传目录"""
        if check_file_exist(local_folder) is True:
            files = scan_files(local_folder)
            if len(files) > 0:
                if isinstance(remote_folder, str) and len(remote_folder) > 0:
                    self.mkd(remote_folder)

                for index, file in enumerate(files):
                    if check_is_file(file):
                        self.upload_file(file)
                    else:
                        self.upload_folder(file, f"{remote_folder}/{get_file_folder(file)}" if isinstance(remote_folder, str) and len(remote_folder) > 0 else f"{get_file_folder(file)}")

    # 获取用户列表
    def get_users(self):
        return self.config.USERS

    # 更新用户
    def update_users(self, users: list):
        if self.get_client():
            for user in self.config.USERS:
                if self.client.handler.authorizer.has_user(user.get('name')) is True:
                    self.client.handler.authorizer.remove_user(user.get('name'))

            self.config = self.config._replace(USERS=users)

            for user in self.config.USERS:
                self.client.handler.authorizer.add_user(user.get('name'), user.get('psw'), user.get('folder'), user.get('role'))
