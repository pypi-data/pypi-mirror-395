import os
import time

from robertcommonio.system.io.ftps import FtpConfig, FtpAccessor
from robertcommonbasic.basic.cls.utils import daemon_thread
from robertcommonbasic.basic.os.file import check_is_file, get_file_name
from typing import Callable


def test_client():
    access = FtpAccessor(FtpConfig(HOST='cn1dc2.smartbeop.com', PORT=9506, USER='clpes', PSW='8e4oJrGu6QmGN', IS_SSL=True))
    #access = FtpAccessor(FtpConfig(HOST='ftp.panpwrws.com', PORT=21, USER='clpes', PSW='8e4oJrGu6QmGN', IS_SSL=True))
    access.start()
    access.cwd('Pan42Measurements')
    files = access.nlst()
    for file in files:
        if file.endswith('.csv'):
            access.download_file(file, get_file_name(file))
            access.delete(file)
    print(files)


def test_client1():
    access = FtpAccessor(FtpConfig(HOST='ftp.panpwrws.com', PORT=21, USER='clpes', PSW='8e4oJrGu6QmGN', IS_SSL=True))
    #access = FtpAccessor(FtpConfig(HOST='ftp.panpwrws.com', PORT=21, USER='clpes', PSW='8e4oJrGu6QmGN', IS_SSL=True))
    access.start()
    access.cwd('Pan42Measurements')
    files = access.nlst()
    for file in files:
        if file.endswith('.csv'):
            access.download_file(file, get_file_name(file))
            access.delete(file)
    print(files)


test_client1()
