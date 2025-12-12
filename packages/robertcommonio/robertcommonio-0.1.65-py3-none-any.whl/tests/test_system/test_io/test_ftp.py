import os
import time

from robertcommonio.system.io.ftp import FtpConfig, FtpAccessor
from robertcommonbasic.basic.cls.utils import daemon_thread
from typing import Callable


def test_client():
    access = FtpAccessor(FtpConfig(HOST='127.0.0.1', PORT=5001, USER='admin', PSW='123456'))
    client = access.get_client()
    assert access.download_file(client, 'test.ini', 'testv1.ini') == True


def test_client1():
    access = FtpAccessor(FtpConfig(HOST='cn1dc2.smartbeop.com', PORT=9506, USER='clpes', PSW='8e4oJrGu6QmGN'))
    client = access.get_client()
    assert access.download_file(client, 'test.ini', 'testv1.ini') == True


@daemon_thread
def test_server():
    #admin,123456,elramwM,;

    access = FtpAccessor(FtpConfig(HOST='0.0.0.0', PORT=5001, USERS=[{'name': 'admin', 'psw': '123456', 'folder': os.getcwd(), 'role': 'elramwM'}]))
    access.start_server()


@daemon_thread
def test_thread_server(func: str):
    access = FtpAccessor(FtpConfig(HOST='0.0.0.0', PORT=5001, USERS=[{'name': 'admin', 'psw': '123456', 'folder': os.getcwd(), 'role': 'elramwM'}]))
    access.__getattribute__(func)()


test_client1()
