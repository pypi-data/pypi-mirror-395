import time

from robertcommonbasic.basic.data.conversion import format_bytes
from robertcommonio.system.io.transport import IOTTransportSocket, IOTTransportSerial


def call_back(data):
    print(data)


def extra_on_connect(transport):
    """连接上服务器后需要进行的初始化操作"""
    print(f"{transport} connect")


def extra_on_close(transport):
    """连接上服务器后需要进行的初始化操作"""
    print(f"{transport} close")


def extra_on_receive(transport, datas: bytes):
    print(f"{transport} receive {format_bytes(datas)}")


def test_tcp_client():
    client = IOTTransportSocket(**{'host': '127.0.0.1', 'port': 4001})
    client.extra_on_connect = extra_on_connect
    client.extra_on_close = extra_on_close
    client.extra_on_receive = extra_on_receive
    client.start()
    client.write(b'A0 A1 A2')
    while client.is_connected():
        print(client.read(100))
        time.sleep(1)


def test_serial_client():
    client = IOTTransportSerial(**{'port': 'com2'})
    client.extra_on_connect = extra_on_connect
    client.extra_on_close = extra_on_close
    client.extra_on_receive = extra_on_receive
    client.set_timeout(0.5)
    client.start()
    client.write(b'A0 A1 A2')
    while client.is_connected():
        print(client.read(100))
        time.sleep(1)


test_serial_client()
