import time
import socketserver
from typing import Union, Optional, Any
from robertcommonbasic.basic.re.utils import format_name
from robertcommonbasic.basic.data.utils import generate_object_id
from robertcommonbasic.basic.data.frame import PACKAGETYPE, FRAMETYPE, TRANSFERTYPE, pack_frame
from robertcommonbasic.basic.dt.utils import parse_time


from robertcommonio.system.io.socket import SocketType, SocketConfig, SocketAccessor, SocketIPAccssor, SocketHandler, IOTNetwork, IOTNetMessage, IOTNetResult, format_bytes, IOTSocketClient, IOTSocketServer


def call_back(data):
    print(data)


def test_tcp_client():
    config = SocketConfig(MODE=SocketType.TCP_CLIENT, HOST='0.0.0.0', PORT=1000, CALL_BACK={})
    accessor = SocketAccessor(config)
    accessor.start()


class TCPServer:

    def __init__(self):
        pass

    def handle_data(self, client, package: dict):
        try:
            frame_type = package['frame_type']
            package_type = package['package_type']
            package_index = package['package_index']
            data = package['data']
            if frame_type == FRAMETYPE.REQ:
                if package_type == PACKAGETYPE.REGISTER:
                    self.create_config(client, package_type, package_index, TRANSFERTYPE.JSON_COMPRESS_ENCRYPT, {'result': True, 'msg': ''})
                elif package_type == PACKAGETYPE.FILE:
                    self.analyze_file(client, data, package_type, package_index)
            elif frame_type == FRAMETYPE.ACK:
                pass
        except Exception as e:
            print(f"handle data fail ({e.__str__()})")

    def analyze_file(self, client, file: dict, package_type: int, package_index: int):
        file_name = file.get('file_name')
        task_name = file.get('task_name')
        file_content = file.get('file_content')
        file_type = file.get('file_type', 'real')
        ack_data = {'result': False, 'msg': 'UnKnown'}
        if file_name is not None and file_content is not None:
            try:
                file_time = parse_time(format_name(file_name, r'[^0-9]+', ''))
                print(f"recv {client.reg_tag} {file_type} file({file_name}) success({package_index})")
                time.sleep(11)
                ack_data = {'result': True, 'msg': ''}
            except Exception as e:
                print(f"send request({file_name}) fail({e.__str__()})")
                ack_data['msg'] = e.__str__()[:30]
        self.create_config(client, package_type, package_index, TRANSFERTYPE.JSON_COMPRESS_ENCRYPT, ack_data)

    def create_config(self, client, package_type: int, package_index: int, transfer_type: int, data: Any):
        answer = dict()
        answer['frame_type'] = FRAMETYPE.CONFIG
        answer['package_type'] = package_type
        answer['package_index'] = package_index
        answer['transfer_type'] = transfer_type
        answer['data'] = data
        return client.send(pack_frame(answer))


def test_tcp_server():
    tcp = TCPServer()
    config = SocketConfig(MODE=SocketType.TCP_SERVER, HOST='0.0.0.0', PORT=9504, BUFFER=8192, TIME_OUT=10, CALL_BACK={'handle_data': tcp.handle_data})
    accessor = SocketIPAccssor(config)
    accessor.start()

    while True:
        time.sleep(1)


def test_s7_client():
    config = SocketConfig(MODE=SocketType.TCP_CLIENT, HOST='0.0.0.0', PORT=1000, CALL_BACK={})
    accessor = SocketAccessor(config)
    accessor.start()


class IOTClientMessage(IOTNetMessage):

    def get_head_length(self) -> int:
        '''协议头数据长度，也即是第一次接收的数据长度'''
        return 2

    def get_content_length(self) -> int:
        '''二次接收的数据长度'''
        if self.heads is not None:
            return self.heads[1]
        else:
            return 0

    def check_head(self) -> bool:
        '''回复报文校验'''
        if self.heads is not None:
            if self.heads[0] == 0xA0:
                return True
            else:
                return False
        else:
            return False

    def check_response(self) -> bool:
        '''回复报文校验'''
        if self.heads is not None:
            if self.heads[0] == 0xA0 and self.create_sum((self.heads + self.contents)[0:-1]) == self.contents[-1]:
                return True
            else:
                return False
        else:
            return False

    def create_sum(self, datas: bytes):
        data = sum(datas) & 0xFF
        data = 255 - data if data > 0 else 255 + data
        return data + 1


class IOTServerMessage(IOTNetMessage):

    def get_head_length(self) -> int:
        '''协议头数据长度，也即是第一次接收的数据长度'''
        return 1024


class IOTClient(IOTNetwork):

    '''timeout为None 不超时'''
    def __init__(self, host: str, port: int, timeout: Optional[int] = 5):
        super().__init__(host, port, timeout)

    def get_net_msg(self):
        return IOTClientMessage()

    def extra_on_connect(self, socket):
        '''连接上服务器后需要进行的二次握手操作'''
        # 返回成功的信号
        return IOTNetResult.create_success()

    def extra_on_disconnect(self, socket):
        return IOTNetResult.create_success()

    def ping(self):
        return self.get_socket().is_success

    def read(self):
        read = self.read_server(None)
        return read


class IOTServer(IOTNetwork):
    '''timeout为None 不超时'''

    def __init__(self, host: str, port: int, timeout: Optional[int] = 5, size: int = 500):
        super().__init__(host, port, timeout, size)

    def get_net_msg(self):
        return IOTServerMessage()

    def extra_on_connect(self, socket):
        '''连接上服务器后需要进行的二次握手操作'''
        # 返回成功的信号
        print(f"connect({socket})")
        return IOTNetResult.create_success()

    def extra_on_close(self, socket):
        print(f"close({socket})")
        return IOTNetResult.create_success()

    def extra_on_disconnect(self, socket):
        print(f"disconnect({socket})")
        return IOTNetResult.create_success()

    def extra_on_receive(self, socket, datas: bytes):
        print(f"recv({format_bytes(datas)})")

    def read(self):
        read = self.read_server(None)
        return read


def test_iot_client():
    client = IOTClient('127.0.0.1', 4001, None)
    while True:
        rt = client.read()
        if rt.is_success is True:
            print(format_bytes(rt.contents[0]))
        else:
            print(rt.msg)


def test_iot_server():
    server = IOTServer('0.0.0.0', 4001, None)
    server.start_server()
    while True:
        time.sleep(1)


def test_iot_socket_client():

    def handle_message(msg: bytes):
        print(msg.decode())

    def server_shutdown():
        print("Server shutdown.")

    try:
        smtp_client = IOTSocketClient('127.0.0.1', 2404)
    except ConnectionRefusedError:
        print("Connection refused.")
        return
    print("Connected.")
    smtp_client.on_msg_received = handle_message
    smtp_client.on_shutdown = server_shutdown
    smtp_client.start_receiving()


def test_iot_socket_server():

    def handle_client_connect(client: IOTSocketClient):
        client_address = client.socket.getpeername()
        print(f"{client_address} connected.")

    def handle_message_received(client: IOTSocketClient, msg: bytes):
        msg_str = msg.decode()
        client_address = client.socket.getpeername()
        print(f"{client_address}: {msg_str}")

    def handle_shutdown(client: IOTSocketClient):
        client_address = client.socket.getpeername()
        print(f"{client_address} disconnected.")

    try:
        server = IOTSocketServer('127.0.0.1', 2404)
    except Exception as e:
        print("Connection refused.")
        return

    server.on_client_connect = handle_client_connect
    server.on_msg_received = handle_message_received
    server.on_shutdown = handle_shutdown
    server.start_listening()
    while True:
        input("> ")


test_tcp_server()