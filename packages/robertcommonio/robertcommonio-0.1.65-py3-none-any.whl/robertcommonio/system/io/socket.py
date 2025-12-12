import asyncore
import logging
import sys
import socket
import time
from abc import abstractmethod
from typing import NamedTuple, Any, Optional, Union, List
from enum import Enum
from threading import Thread, Lock, Event, currentThread

from robertcommonbasic.basic.cls.utils import daemon_thread, function_thread, stop_thread
from robertcommonbasic.basic.data.frame import FRAMEFLAG, PACKAGETYPE, FRAMETYPE, TRANSFERTYPE, pack_frame, unpack_frame, get_pack_start_length, get_pack_header_length, convert_bytes_to_int
from robertcommonbasic.basic.data.conversion import format_bytes
from robertcommonbasic.basic.dt.utils import get_datetime


class CloseException(Exception):
    pass


class NormalException(Exception):
    pass


class SocketType(Enum):
    TCP_CLIENT = 'tcp_client'
    TCP_SERVER = 'tcp_server'
    UDP_CLIENT = 'udp_client'
    UDP_SERVER = 'udp_server'


class SocketConfig(NamedTuple):
    MODE: SocketType
    HOST: str
    PORT: int = 9500
    POOL: int = 0
    BUFFER: int = 1400
    LISTEN: int = 500
    TIME_OUT: int = 10
    RECV_TIMEOUT: Optional[int] = None
    IS_BROADCAST: bool = False
    CALL_BACK: dict = {}
    HANDLE_CLASS: Any = None
    PARAENT_CLASS: Any = None


class SocketHandler(asyncore.dispatcher_with_send):
    """定制应答式处理类"""

    def __init__(self, config: SocketConfig, sock=None, addr=None):
        asyncore.dispatcher_with_send.__init__(sock)

        self.config = config
        self.sock = sock
        self.addr = addr
        self.valid = True
        self.infos: dict = {'start': get_datetime(), 'recv': get_datetime(), 'send': get_datetime()}   # 存储信息

        self.start_length = get_pack_start_length()
        self.header_length = get_pack_header_length()

        if self.config.MODE == SocketType.TCP_CLIENT:
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect((self.config.HOST, self.config.PORT))
        elif self.config.MODE == SocketType.UDP_CLIENT:
            self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.connect((self.config.HOST, self.config.PORT))

    def __str__(self):
        if isinstance(self.addr, tuple) and len(self.addr) >= 2:
            return f"{self.addr[0]}:{self.addr[1]}"
        return str(self.addr)

    def __del__(self):
        self.exit()

    def exit(self):
        self.valid = False
        try:
            self.close()
        except:
            pass

    def format_bytes(self, data: bytes) -> str:
        return ' '.join(["%02X" % x for x in data]).strip()

    def recv_bytes(self, length: int) -> Optional[bytes]:
        data = self.recv(length)
        if isinstance(data, bytes) and len(data) > 0:
            self.infos['recv'] = get_datetime()
        return data

    def handle_read(self):
        try:
            data_start = self.recv_bytes(self.start_length)    # 包头
            if len(data_start) == self.start_length:
                if data_start == FRAMEFLAG.START_FLAG:    #
                    data_header = self.recv_bytes(self.header_length)    # 包头长度
                    if len(data_header) == self.header_length:
                        data_end_length = convert_bytes_to_int(data_header[-4:]) + self.start_length + 1
                        data_end = self.recv_bytes(data_end_length)  # 包内容
                        if len(data_end) == data_end_length:
                            if data_end[-2:] == FRAMEFLAG.END_FLAG:  # 包结尾
                                if 'analyze_data' in self.config.CALL_BACK.keys():
                                    self.config.CALL_BACK['analyze_data'](self, data_start + data_header + data_end)
        except Exception as e:
            logging.error(f"handle read({self}) fail ({e.__str__()})")

    def handle_error(self):
        self.valid = False
        t, e, trace = sys.exc_info()
        if 'handle_error' in self.config.CALL_BACK.keys():
            self.config.CALL_BACK['handle_error'](self, e)
        self.close()

    def handle_close(self):
        self.valid = False
        if 'handle_close' in self.config.CALL_BACK.keys():
            self.config.CALL_BACK['handle_close'](self)
        self.close()

    def handle_connect(self):
        if 'handle_connect' in self.config.CALL_BACK.keys():
            self.config.CALL_BACK['handle_connect'](self)

    def writable(self):
        return True

    def handle_write(self):
        pass

    def readable(self):
        return True

    def check_invalid(self) -> bool:
        recv_timeout = self.config.RECV_TIMEOUT
        if self.valid is True and (recv_timeout in [None, 0] or (get_datetime() - self.infos.get('recv')).total_seconds() <= recv_timeout):
            return True
        return False
        
    def info(self) -> dict:
        self.infos.update({'address': self.__str__(), 'valid': self.valid})
        return self.infos


class SocketServer(asyncore.dispatcher):

    def __init__(self, config: SocketConfig):
        asyncore.dispatcher.__init__(self)
        self.config = config
        self.sockets = {}

        if self.config.MODE == SocketType.TCP_SERVER:
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.set_reuse_addr()
        self.bind((self.config.HOST, self.config.PORT))

        if self.config.MODE == SocketType.TCP_SERVER:
            self.listen(self.config.LISTEN)

    def exit(self):
        for n, sock in self.sockets.items():
            try:
                if sock:
                    if hasattr(sock, 'exit'):
                        sock.exit()
            except Exception as e:
                pass
        self.sockets = {}
        self.close()

    def handle_close(self):
        self.close()

    def handle_accept(self):
        client = self.accept()
        if client is not None:
            sock, addr = client
            if self.verify_request(sock, addr) is True:
                if self.config.HANDLE_CLASS is not None:
                    self.sockets[f"{addr[0]}:{addr[1]}"] = self.config.HANDLE_CLASS(self.config, sock, addr, self)
                else:
                    self.sockets[f"{addr[0]}:{addr[1]}"] = SocketHandler(self.config, sock, addr)

    def verify_request(self, sock, address):
        return True

    def clear_invalid(self):
        sock_addrs = list(self.sockets.keys())
        for sock_addr in sock_addrs:
            if sock_addr in self.sockets.keys() and self.sockets[sock_addr].check_invalid() is False:
                try:
                    if hasattr(self.sockets[sock_addr], 'exit'):
                        self.sockets[sock_addr].exit()
                except:
                    pass
                del self.sockets[sock_addr]


class SocketAccessor:

    def __init__(self, config: SocketConfig):
        self.exit_thread = False
        self.config = config
        self.accessor = None
        self.threads: dict = {}

    def __del__(self):
        self.exit()

    def __str__(self):
        return f"{self.config.HOST}:{self.config.PORT}"

    def exit(self):
        self.exit_thread = True
        if self.accessor:
            self.accessor.exit()
        for name, thread in self.threads.items():
            thread.join(5)
            stop_thread(thread)
        self.threads = {}
        self.accessor = None

    def asyncore_loop(self, *args, **kwargs):
        while self.exit_thread is False:
            try:
                asyncore.loop(*args, **kwargs)
            except Exception as e:
                logging.error(f"asyncore loop fail({e.__str__()})")
            time.sleep(1)

    def start(self, thread: bool = True):
        if self.config.MODE in [SocketType.TCP_SERVER, SocketType.UDP_SERVER]:
            self.accessor = SocketServer(self.config)
        else:
            if self.config.HANDLE_CLASS is not None:
                self.accessor = self.config.HANDLE_CLASS(self.config)
            else:
                self.accessor = SocketHandler(self.config)

        if self.config.POOL == 0:
            if thread is True:
                self.threads['asyncore_loop'] = Thread(target=self.asyncore_loop, name=f"socket{self} loop", daemon=False)
            else:
                self.asyncore_loop()
        else:
            if thread is True:
                self.threads['asyncore_loop'] = Thread(target=self.asyncore_loop, name=f"socket({self}) loop", daemon=False, kwargs={'timeout': self.config.TIME_OUT})
            else:
                self.asyncore_loop(self.config.TIME_OUT)

        for name, thread in self.threads.items():
            thread.start()


class AsyncResult:

    def __init__(self, client, request_id: int, data: bytes, timeout: float, retries: int = 1):
        self.client = client
        self.request_id = request_id
        self.data = data
        self.retries = retries
        self.timeout = timeout
        self.wait_event = Event()
        self.error = None
        self.result = None

    def __del__(self):
        self.exit()

    def exit(self):
        self.close()

    def close(self):
        if self.wait_event:
            self.wait_event.clear()

    def send_request(self, wait_config: bool = True) -> dict:
        for r in range(self.retries):
            self.send()
            if wait_config is False:
                if self.error:
                    raise self.error
                return {}
            else:
                if self.wait(self.timeout) is True:
                    return self.result
        if self.error:
            raise self.error
        raise Exception(f"no config")

    def recv(self, package: dict):
        if package.get('package_index') == self.request_id:
            self.wait_event.set()
        self.result = package

    def format_bytes(self, data: bytes) -> str:
        return ' '.join(["%02X" % x for x in data]).strip()

    def send(self):
        self.error = None
        try:
            if self.client:
                if self.client.send(self.data) <= 0:
                    raise Exception(f"send fail")
            else:
                raise Exception(f"no connect")
        except Exception as e:
            self.error = Exception(f"send exception({e.__str__()})")

    def wait(self, timeout: float) -> bool:
        while True:
            if not self.wait_event.wait(timeout):
                return False
            return True


class AsyncResultManage:
    
    def __init__(self, start_package_id: int, end_package_id: int, call_backs: dict):
        self.start_package_id = start_package_id
        self.end_package_id = end_package_id
        self.call_backs = call_backs
        
        self.package_id = start_package_id
        self.requests = {}
        
    def set_debug_log(self, content: str):
        if 'set_debug_log' in self.call_backs.keys():
            self.call_backs['set_debug_log'](content)

    def get_pack_id(self) -> int:
        if self.package_id >= self.end_package_id:
            self.package_id = self.start_package_id
        self.package_id = self.package_id + 1
        return self.package_id

    def config_request(self, request_id: int, result: dict = None):
        if request_id in self.requests.keys():
            if result is not None:
                self.set_debug_log(f"recv {request_id} (FRAMETYPE.CONFIG)")
                self.requests[request_id].recv(result)
            else:
                del self.requests[request_id] 
    
    def create_config(self, client, package_type: int, package_index: int, transfer_type: int, data: Any):
        self.set_debug_log(f"send {package_index}({FRAMETYPE(FRAMETYPE.CONFIG).__str__()}--{PACKAGETYPE(package_type).__str__()}--{TRANSFERTYPE(transfer_type).__str__()})")
        answer = dict()
        answer['frame_type'] = FRAMETYPE.CONFIG
        answer['package_type'] = package_type
        answer['package_index'] = package_index
        answer['transfer_type'] = transfer_type
        answer['data'] = data
        return client.send(pack_frame(answer))

    def create_request(self, client, package_index: Optional[int], frame_type: int, package_type: int, transfer_type: int, data, timeout: float, retries: int = 1, wait_config: bool = True):
        try:
            if package_index is None:
                package_index = self.get_pack_id()
            self.set_debug_log(f"send {package_index}({FRAMETYPE(frame_type).__str__()}--{PACKAGETYPE(package_type).__str__()}--{TRANSFERTYPE(transfer_type).__str__()})")
            self.requests[package_index] = AsyncResult(client, package_index, pack_frame({'frame_type': frame_type, 'package_type': package_type, 'package_index': package_index, 'transfer_type': transfer_type, 'data': data}), timeout, retries)
            return self.requests[package_index].send_request(wait_config)
        except Exception as e:
            raise Exception(f"create request {package_index}({client})({e.__str__()})")
        finally:
            self.config_request(package_index)


class SocketIPHandler:

    def __init__(self, config: SocketConfig, sock=None, addr=None, msg: Optional[bytes]=None):
        self.config = config
        self.sock = sock
        self.addr = addr
        self.reg_tag = ''
        self.valid = True
        self.threads: dict = {}
        self.lock = Lock()

        self.start_length = get_pack_start_length()
        self.header_length = get_pack_header_length()
        self.exit_flag = False
        self.rec_buffer = b''
        self.infos: dict = {'start': get_datetime(), 'recv': get_datetime(), 'send': get_datetime()}   # 存储信息

        # 触发连接事件
        if self.is_udp_server():
            if 'handle_read' in self.config.CALL_BACK.keys():
                self.config.CALL_BACK['handle_read'](self, msg)
        else:
            self.threads['receive'] = self.receive()
            for name, thread in self.threads.items():
                thread.start()
            self.handle_connect()

    def __str__(self):
        if isinstance(self.addr, tuple) and len(self.addr) >= 2:
            return f"{self.addr[0]}:{self.addr[1]}"
        if self.config is not None:
            return f"{self.config.HOST}:{self.config.PORT}"
        return str(self.addr)

    def __del__(self):
        self.exit()

    def exit(self):
        self.valid = False
        self.close()

    def is_udp_server(self) -> bool:
        return self.config.MODE == SocketType.UDP_SERVER

    def format_bytes(self, data: bytes) -> str:
        return ' '.join(["%02X" % x for x in data]).strip()

    def close(self):
        self.valid = False
        self.exit_flag = True
        if self.is_udp_server() is False:
            if self.sock:
                try:
                    self.sock.close()
                except:
                    pass
            del self.sock
            self.sock = None
        for name, thread in self.threads.items():
            if thread is not currentThread():
                thread.join(5)
            stop_thread(thread)
        self.threads = {}

    def handle_connect(self):
        if 'handle_connect' in self.config.CALL_BACK.keys():
            self.config.CALL_BACK['handle_connect'](self)

    def handle_close(self, reason: str = ''):
        self.close()
        if 'handle_close' in self.config.CALL_BACK.keys():
            self.config.CALL_BACK['handle_close'](self, reason)

    def handle_error(self, e: Exception):
        self.close()
        if 'handle_error' in self.config.CALL_BACK.keys():
            self.config.CALL_BACK['handle_error'](self, e)
        else:
            logging.error(f"handle_error({self})({e.__str__()})")
            
    def recv_bytes(self, length: int) -> Optional[bytes]:
        data = b''
        while len(data) < length:
            if self.check_invalid() is True:
                rec_data = self.sock.recv(length - len(data))  # 加快接收速度
                if rec_data is None or len(rec_data) == 0:
                    raise CloseException(f"remote close")
                self.infos['recv'] = get_datetime()
                data += rec_data
            else:
                raise CloseException(f"invalid")
        if len(data) != length:
            raise NormalException(f"recv length fail({len(data)}/{length})")
        return data

    def recv_default(self):       
        if self.recv_bytes(1) == FRAMEFLAG.START_FLAG[:1]:
            t1 = time.time()
            if self.recv_bytes(1) == FRAMEFLAG.START_FLAG[1:]:
                data_header = self.recv_bytes(self.header_length)  # 包头长度为9
                t_h = time.time()
                if data_header is not None:
                    data_end_length = convert_bytes_to_int(data_header[-4:]) + self.start_length + 1
                    data_end = self.recv_bytes(data_end_length)  # 包内容
                    t_d = time.time()
                    if data_end is not None:
                        if data_end[-2:] == FRAMEFLAG.END_FLAG:  # 包结尾
                            try:
                                package = unpack_frame(FRAMEFLAG.START_FLAG + data_header + data_end)
                                t_p = time.time()
                                if 'handle_data' in self.config.CALL_BACK.keys():
                                    package['cost'] = {'s': data_end_length, 'h': '{:.2f}'.format(t_h - t1), 'd': '{:.2f}'.format(t_d - t_h), 'p': '{:.2f}'.format(t_p - t_d)}
                                    self.config.CALL_BACK['handle_data'](self, package)
                            except Exception as e:
                                logging.error(f"unpack frame fail({e.__str__()})")

    @daemon_thread
    def receive(self):
        while self.exit_flag is False:
            try:
                name = f"{self.reg_tag}({self}) receive"
                if currentThread().getName() != name:
                    currentThread().setName(name)
                if 'handle_read' in self.config.CALL_BACK.keys():
                    data = self.sock.recv(self.config.BUFFER)
                    if data is None or len(data) == 0:
                        raise CloseException(f"remote close")
                    elif data is not None and len(data) > 0:
                        self.infos['recv'] = get_datetime()
                        self.config.CALL_BACK['handle_read'](self, data)
                else:
                    self.recv_default()
            except socket.timeout as e:
                if self.config.RECV_TIMEOUT > 0:
                    pass
                else:
                    self.handle_error(e)
            except NormalException as e:
                logging.error(e.__str__())
            except CloseException as e:
                self.handle_close(e.__str__())
            except Exception as e:
                self.handle_error(e)

    def send(self, data: bytes, is_broadcast: bool = False):
        with self.lock:
            if self.sock:
                length = len(data)
                buffer = self.config.BUFFER
                group = int(length/buffer)
                for i in range(group):
                    if self.is_udp_server():
                        self.sock.sendto(data[i*buffer: (i+1)*buffer], self.addr if is_broadcast is False else ('<broadcast>', self.config.PORT))
                    else:
                        self.sock.send(data[i*buffer: (i+1)*buffer])
                if group*buffer < length:
                    if self.is_udp_server():
                        self.sock.sendto(data[group*buffer:], self.addr if is_broadcast is False else ('<broadcast>', self.config.PORT))
                    else:
                        self.sock.send(data[group*buffer:])
                self.infos['send'] = get_datetime()
                return length
            raise Exception(f"no connect")
    
    def check_invalid(self) -> bool:
        recv_timeout = self.config.RECV_TIMEOUT
        if self.valid is True and (recv_timeout in [None, 0] or (get_datetime() - self.infos.get('recv')).total_seconds() <= recv_timeout):
            return True
        return False
    
    def info(self) -> dict:
        self.infos.update({'address': self.__str__(), 'reg': self.reg_tag, 'valid': self.valid})
        return self.infos


class SocketIPAccssor:

    def __init__(self, config: SocketConfig):
        self.config = config
        self.accessor = None
        self.exit_flag = False
        self.threads: dict = {}
        self.sockets = {}
        self.lock = Lock()
        self.lock_sock= Lock()
        self.handle = self.config.HANDLE_CLASS if self.config.HANDLE_CLASS is not None else SocketIPHandler

    def __del__(self):
        self.exit()

    def exit(self):
        self.exit_flag = True
        for k, v in self.sockets.items():
            try:
                v.close()
            except:
                pass
        if self.accessor:
            self.accessor.close()
        self.accessor = None
        for name, thread in self.threads.items():
            stop_thread(thread)
        self.threads = {}
        self.sockets = {}

    def create_client(self):
        with self.lock:
            if self.config.MODE == SocketType.TCP_CLIENT:
                self.accessor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            elif self.config.MODE == SocketType.UDP_CLIENT:
                self.accessor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            self.accessor.settimeout(self.config.TIME_OUT)  # 设置连接超时
            self.accessor.connect((self.config.HOST, self.config.PORT))
            self.accessor.settimeout(None)

            self.sockets[f"{self.config.HOST}:{self.config.PORT}"] = self.handle(self.config, self.accessor)
        
    def create_server(self):
        with self.lock:
            if self.config.MODE == SocketType.TCP_SERVER:
                self.accessor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.accessor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            elif self.config.MODE == SocketType.UDP_SERVER:
                self.accessor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            if self.config.IS_BROADCAST is True:
                self.accessor.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

            self.accessor.bind((self.config.HOST, self.config.PORT))

            if self.config.MODE == SocketType.TCP_SERVER:
                self.accessor.listen(self.config.LISTEN)

        while self.exit_flag is False:
            try:
                if self.config.MODE == SocketType.TCP_SERVER:
                    sock, addr = self.accessor.accept()  # 接收连接
                    if self.verify_request(sock, addr) is True:
                        if isinstance(self.config.RECV_TIMEOUT, int) and self.config.RECV_TIMEOUT > 0:
                            sock.settimeout(self.config.RECV_TIMEOUT)  # 设置连接超时
                        with self.lock_sock:
                            self.sockets[f"{addr[0]}:{addr[1]}"] = self.handle(self.config, sock, addr)
                elif self.config.MODE == SocketType.UDP_SERVER:
                    msg, addr = self.accessor.recvfrom(self.config.BUFFER)
                    if self.verify_request(self.accessor, addr) is True:
                        with self.lock_sock:
                            self.sockets[f"{addr[0]}:{addr[1]}"] = self.handle(self.config, self.accessor, addr, msg)
            except Exception as e:
                pass

    def verify_request(self, sock, address):
        return True

    def clear_invalid(self):
        with self.lock_sock:
            sock_addrs = list(self.sockets.keys())
            for sock_addr in sock_addrs:
                if sock_addr in self.sockets.keys() and self.sockets[sock_addr].check_invalid() is False:
                    self.sockets[sock_addr].exit()
                    del self.sockets[sock_addr]

    def clear_invalid_thread(self):
        while self.exit_flag is False:
            try:
                self.clear_invalid()
            except Exception as e:
                pass
            time.sleep(1)

    def start(self, thread: bool = True):
        if self.config.MODE in [SocketType.TCP_SERVER, SocketType.UDP_SERVER]:
            if thread is True:
                self.threads['create_server'] = Thread(target=self.create_server, name=f"create_server")
            else:
                self.create_server()
        else:
            if thread is True:
                self.threads['create_client'] = Thread(target=self.create_client, name=f"create_client")
            else:
                self.create_client()

        if self.config.RECV_TIMEOUT is not None and self.config.RECV_TIMEOUT > 0:
            self.threads['clear_invalid'] = Thread(target=self.clear_invalid_thread, name=f"clear_invalid")

        for name, thread in self.threads.items():
            thread.start()

    def send_broadcast(self, data: Union[str, bytes], address: str = '<broadcast>'):
        if self.accessor:
            self.accessor.sendto(data if isinstance(data, bytes) else data.encode('utf-8'), (address, self.config.PORT))

    def info(self):
        with self.lock_sock:
            return {address: sock.info() for address, sock in self.sockets.items() if hasattr(sock, 'info')}
        return {}


# IOT 重构
class IOTNetMessage:

    def __init__(self):
        self.heads: Optional[bytearray] = None
        self.contents: Optional[bytearray] = None
        self.sends: Optional[bytearray] = None

    def __str__(self):
        return f"IOTNetMessage"

    def get_head_length(self) -> int:
        """
            协议头数据长度，也即是第一次接收的数据长度
        """
        return 0

    def get_content_length(self) -> int:
        """二次接收的数据长度"""
        return 0

    def get_frame_length(self) -> int:
        """帧大小"""
        return 1024

    def check_response(self) -> bool:
        """回复报文校验"""
        return True

    def check_head(self) -> bool:
        """回复报文校验"""
        return True
    

class IOTNetResult:

    is_success: bool = False    # 是否成功的标志
    msg: str = 'Unknown'    # 操作返回的错误消息
    code: int = 10000   # 错误码
    contents: list = [None] * 20    # 结果数组

    '''结果对象类，可以携带额外的数据信息'''
    def __init__(self, code: int = 0, msg: str = ""):
        self.code = code
        self.msg = msg
        self.is_success = False
        self.contents: list = [None] * 20  # 结果数组

    def __str__(self):
        return f"code: {self.code} msg: {self.msg}"

    def copy(self, result):
        if result is not None and isinstance(result, IOTNetResult):
            self.code = result.code
            self.msg = result.msg

    @staticmethod
    def create_fail(result=None):
        failed = IOTNetResult()
        if result is not None:
            failed.code = result.code
            failed.msg = result.msg
        return failed

    @staticmethod
    def create_success(contents: Optional[list] = None):
        success = IOTNetResult()
        success.is_success = True
        success.msg = 'Success'
        if contents is not None and not isinstance(contents, list):
            contents = [contents]
        if isinstance(contents, list):
            for i, content in enumerate(contents):
                success.contents[i] = content
        return success


class IOTNetworkBase:

    def __init__(self):
        self.iot_socket = None
        self.socket_error = False
        self.callbacks = {}

    def __str__(self):
        return f"IOTNetworkBase"

    def __del__(self):
        self.exit()

    @abstractmethod
    def extra_on_close(self, sock: socket):
        """连接上服务器后需要进行的初始化操作"""
        raise NotImplementedError()

    def logging(self, **kwargs):
        if 'call_logging' in kwargs.keys():
            self.callbacks['call_logging'] = kwargs.get('call_logging')

        if 'content' in kwargs.keys():
            call_logging = self.callbacks.get('call_logging')
            if call_logging:
                call_logging(**kwargs)

    def exit(self):
        if self.iot_socket is not None:
            self.iot_socket.close()
        self.iot_socket = None

    def close_socket(self, sock: socket):
        if sock is not None:
            sock.close()
            self.extra_on_close(sock)

    def receive(self, sock: socket, length: Optional[int] = None, size: Optional[int] = 1024):
        """接收固定长度的字节数组"""
        if length == 0:
            return IOTNetResult.create_success([bytearray(0)])

        data = bytearray()
        try:
            if isinstance(length, int):
                while len(data) < length:
                    pack_size = size if length - len(data) > size else length - len(data)
                    d = sock.recv(pack_size)
                    if not d:
                        raise CloseException(f"close")
                    elif len(d) < pack_size:
                        data.extend(d)
                        break
                    else:
                        data.extend(d)
            else:
                data.extend(sock.recv(size))
            return IOTNetResult.create_success([data])
        except socket.timeout as e:
            return IOTNetResult(msg=f"receive fail({e.__str__()})")
        except (CloseException, Exception) as e:
            self.close_socket(sock)
            return IOTNetResult(msg=f"receive fail({e.__str__()})")

    def send(self, sock: socket, data: Optional[bytes]):
        """发送消息给套接字，直到完成的时候返回"""
        try:
            if data is not None:
                self.logging(content=f"send {len(data)}: [{format_bytes(data)}]")
                sock.send(data)
            return IOTNetResult.create_success()
        except Exception as e:
            self.close_socket(sock)
            return IOTNetResult(msg=f"send fail({e.__str__()})")

    def send_udp_broadcast(self, sock: socket, port: int, data: Optional[bytes]):
        try:
            if data is not None:
                self.logging(content=f"send broadcast {len(data)}: [{format_bytes(data)}]")
                sock.sendto(data, ('<broadcast>', port))
            return IOTNetResult.create_success()
        except Exception as e:
            self.close_socket(sock)
            return IOTNetResult(msg=f"send broadcast fail({e.__str__()})")

    def connection(self, host: str, port: int, timeout: Optional[Union[int, float]] = None, sock_type: int = 1):
        sock = socket.socket(socket.AF_INET, sock_type)
        try:
            sock.settimeout(10 if timeout is None else timeout)
            sock.connect((host, port))
            if timeout is None:
                sock.settimeout(None)
            return IOTNetResult.create_success([sock])
        except Exception as e:
            return IOTNetResult(msg=f"connect fail({e.__str__()})")

    def listen(self, host: str, port: int, size: int = 500, sock_type: int = 1, is_broad_cast: bool = False):
        sock = socket.socket(socket.AF_INET, sock_type)
        try:
            if is_broad_cast is True:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            else:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            if is_broad_cast is False:
                sock.listen(size)
            return IOTNetResult.create_success([sock])
        except Exception as e:
            return IOTNetResult(msg=f"bind fail({e.__str__()})")

    def receive_msg(self, sock: socket, net_msg):
        """接收一条完整的数据，使用异步接收完成，包含了指令头信息"""
        if net_msg is None:
            return self.receive(sock)

        if isinstance(net_msg, IOTNetMessage):
            result = IOTNetResult()
            head = self.receive(sock, net_msg.get_head_length(), net_msg.get_frame_length())
            if head.is_success is False:
                result.copy(head)
                return result

            net_msg.heads = head.contents[0]
            if net_msg.check_head() is False:
                result.msg = f"Receive Invalid Head"
                return result

            content_length = net_msg.get_content_length()
            if content_length == 0:
                net_msg.contents = bytearray(0)
            else:
                content_result = self.receive(sock, content_length, net_msg.get_frame_length())
                if content_result.is_success is False:
                    result.copy(content_result)
                    return result
                net_msg.contents = content_result.contents[0]

            if net_msg.contents is None:
                net_msg.contents = bytearray(0)

            if net_msg.check_response() is False:
                result.msg = f"Receive Invald package"
                return result
            return IOTNetResult.create_success([self.cat_bytes(net_msg.heads, net_msg.contents)])

    def cat_bytes(self, data1: bytes, data2: bytes):
        if data1 is None and data2 is None:
            return None
        if data1 is None:
            return data2
        if data2 is None:
            return data1
        return data1 + data2

    def get_connected(self, sock: socket) -> bool:
        if sock is not None:
            if getattr(sock, '_closed') is False:
                return True
        return False


class IOTNetwork(IOTNetworkBase):
    
    def __init__(self, host: str, port: int, timeout: Optional[Union[int, float]] = None, size: int = 500, is_broad_cast: bool = False):
        super().__init__()
        self.host = host
        self.port = port
        self.timeout = timeout
        self.size = size
        self.lock = Lock()
        self.is_persistent: bool = True  # 是否长连接模式
        self.is_broad_cast = is_broad_cast  # 是否广播模式

    @abstractmethod
    def get_net_msg(self):
        """获取一个新的消息对象的方法"""
        raise NotImplementedError()

    @abstractmethod
    def extra_on_connect(self, sock: socket):
        """连接上服务器后需要进行的初始化操作"""
        raise NotImplementedError()

    @abstractmethod
    def extra_on_disconnect(self, sock: socket):
        """在将要和服务器进行断开的情况下额外的操作"""
        raise NotImplementedError()

    @abstractmethod
    def extra_on_receive(self, sock: socket, datas: bytes):
        raise NotImplementedError()

    def pack_command_with_header(self, command: bytearray):
        """对当前的命令进行打包处理，通常是携带命令头内容，标记当前的命令的长度信息，需要进行重写，否则默认不打包"""
        return command

    def unpack_response(self, send: bytearray, response: bytearray):
        """根据对方返回的报文命令，对命令进行基本的拆包，例如各种Modbus协议拆包为统一的核心报文，还支持对报文的验证"""
        return IOTNetResult.create_success([response])

    # Client
    def create_and_initialication(self):
        """连接并初始化网络套接字"""
        result = self.connection(self.host, self.port, self.timeout)
        if result.is_success:
            # 初始化
            initi = self.extra_on_connect(result.contents[0])
            if initi.is_success is False:
                if result.contents[0] is not None:
                    self.close_socket(result.contents[0])
                result.is_success = initi.is_success
                result.copy(initi)
        return result

    def connect(self):
        result = IOTNetResult()
        self.exit()
        con_result = self.create_and_initialication()
        if con_result.is_success is False:
            self.socket_error = True
            con_result.contents[0] = None
            result.msg = con_result.msg
        else:
            self.iot_socket = con_result.contents[0]
            result.is_success = True
        return result

    def disconnect(self):
        result = IOTNetResult()
        with self.lock:
            result = self.extra_on_disconnect(self.iot_socket)
            self.exit()
            return result

    # Server
    def start_server(self):
        result = IOTNetResult()
        self.exit()
        server_result = self.listen(self.host, self.port, self.size, self.is_broad_cast)
        if server_result.is_success is False:
            server_result.contents[0] = None
            result.msg = server_result.msg
        else:
            self.iot_socket = server_result.contents[0]
            function_thread(self.accept, True, self.iot_socket, name=f"accept").start()
            result.is_success = True
        return result

    def accept(self, s: socket):
        while self.iot_socket is not None:
            sock, addr = s.accept()  # 接收连接
            function_thread(self.receive_client, True, sock, name=f"receive_client").start()

    def stop_server(self):
        result = IOTNetResult()
        with self.lock:
            result = self.extra_on_disconnect(self.iot_socket)
            self.exit()
            return result

    def get_socket(self):
        """获取本次操作的可用的网络套接字"""
        if self.is_persistent:
            # 长连接模式
            if self.socket_error or self.iot_socket is None or self.get_connected(self.iot_socket) is False:
                connect = self.connect()
                if connect.is_success is False:
                    self.socket_error = True
                    return IOTNetResult(msg=connect.msg)
                else:
                    self.socket_error = False
                    return IOTNetResult.create_success([self.iot_socket])
            else:
                return IOTNetResult.create_success([self.iot_socket])
        else:
            # 短连接模式
            return self.create_and_initialication()

    def read_from_socket(self, s: socket, send: Optional[bytearray], has_response: bool = True, pack_unpack: bool = True):
        """在其他指定的套接字上，使用报文来通讯，传入需要发送的消息，返回一条完整的数据指令"""
        send_value = self.pack_command_with_header(send) if pack_unpack else send

        net_msg = self.get_net_msg()
        if net_msg is not None:
            net_msg.sends = send_value

        send_result = self.send(s, send_value)
        if send_result.is_success is False:
            return IOTNetResult.create_fail(send_result)

        if has_response is False:
            return IOTNetResult.create_success([bytearray(0)])

        # 接收数据信息
        result_receive = self.receive_msg(s, net_msg)
        if result_receive.is_success is False:
            return IOTNetResult(code=result_receive.code, msg=result_receive.msg)

        # 拼接结果数据
        return self.unpack_response(send_value, result_receive.contents[0]) if pack_unpack else result_receive

    def read_server(self, send: Optional[bytearray] = None):
        """使用底层的数据报文来通讯，传入需要发送的消息，返回一条完整的数据指令"""
        result = IOTNetResult()
        with self.lock:
            # 获取有用的网络通道，如果没有，就建立新的连接
            result_socket = self.get_socket()
            if result_socket.is_success is False:
                self.socket_error = True
                result.copy(result_socket)
                return result

            read = self.read_from_socket(result_socket.contents[0], send)
            if read.is_success:
                self.socket_error = False
                result.is_success = read.is_success
                result.contents[0] = read.contents[0]
                result.msg = f"Success"
                self.logging(content=f"recv {len(read.contents[0])}: [{format_bytes(read.contents[0])}]")
            else:
                result.copy(read)

        if self.is_persistent is False:
            self.close_socket(result_socket.contents[0])
        return result

    def receive_client(self, s: socket):
        """在其他指定的套接字上，使用报文来通讯，传入需要发送的消息，返回一条完整的数据指令"""
        initi = self.extra_on_connect(s)
        if initi.is_success is False:
            if s is not None:
                self.close_socket(s)
            return initi

        while self.iot_socket is not None:
            net_msg = self.get_net_msg()

            # 接收数据信息
            result_receive = self.receive_msg(s, net_msg)
            if result_receive.is_success is False:
                return IOTNetResult(code=result_receive.code, msg=result_receive.msg)

            # 拼接结果数据
            self.logging(content=f"recv {len(result_receive.contents[0])}: [{format_bytes(result_receive.contents[0])}]")
            self.extra_on_receive(s, result_receive.contents[0])


class IOTSocketClient:
    """IOT TCP Client"""

    def __init__(self, ip: Optional[str] = None, port: Optional[int] = None, sock=None, **kwargs):
        if sock is not None:
            self._socket = sock
        elif isinstance(ip, str) and isinstance(port, int):
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((ip, port))
        else:
            raise ValueError("Either the socket should be passed in the parameters or the ip/port of the server.")
        self.on_msg_received = None
        self.on_shutdown = None
        self._receive_msg_thread = None

    @property
    def socket(self):
        return self._socket

    @property
    def buffer_size(self):
        return self._buffer_size

    @buffer_size.setter
    def buffer_size(self, buffer_size):
        self._buffer_size = buffer_size

    # Events
    @property
    def on_msg_received(self):
        return self._on_msg_received

    @on_msg_received.setter
    def on_msg_received(self, on_msg_received):
        self._on_msg_received = on_msg_received

    @property
    def on_shutdown(self):
        return self._on_shutdown

    @on_shutdown.setter
    def on_shutdown(self, on_shutdown):
        self._on_shutdown = on_shutdown

    # Event triggers
    def _trigger_msg_received(self, msg: bytes):
        if self._on_msg_received is not None:
            self._on_msg_received(msg)

    def _trigger_shutdown(self):
        if self._on_shutdown is not None:
            self._on_shutdown()

    # Private methods
    def _handle_receive_msg(self):
        while True:
            try:
                buffer = self._socket.recv(self._buffer_size)
            except OSError:
                self._trigger_shutdown()
                break

            # Server shutdown
            if len(buffer) == 0:
                self._trigger_shutdown()
                break

            self._trigger_msg_received(buffer)

    @staticmethod
    def _parse_header(header_bytes: bytes):
        return {"length": int(header_bytes.decode("utf-8"))}

    # Public methods
    def start_receiving(self):
        self._receive_msg_thread = function_thread(self._handle_receive_msg, True, name=f"receiving")
        self._receive_msg_thread.start()

    def send(self, msg: bytes):
        self._socket.send(msg)

    def close(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()


class IOTSocketServer:

    def __init__(self, ip: str, port: int):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._socket.bind((ip, port))

        self._clients = list()
        self.on_client_connect = None
        self.on_msg_received = None
        self.on_shutdown = None
        self._listening_thread = None
        self._buffer_size = 1024

    @property
    def socket(self):
        return self._socket

    @property
    def clients(self) -> List[IOTSocketClient]:
        return self._clients

    @property
    def buffer_size(self):
        return self._buffer_size

    @buffer_size.setter
    def buffer_size(self, buffer_size):
        self._buffer_size = buffer_size

    # Events
    @property
    def on_msg_received(self):
        return self._on_msg_received

    @on_msg_received.setter
    def on_msg_received(self, on_msg_received):
        self._on_msg_received = on_msg_received

    @property
    def on_shutdown(self):
        return self._on_shutdown

    @on_shutdown.setter
    def on_shutdown(self, on_shutdown):
        self._on_shutdown = on_shutdown

    @property
    def on_client_connect(self):
        return self._on_client_connect

    @on_client_connect.setter
    def on_client_connect(self, on_client_connect):
        self._on_client_connect = on_client_connect

    # Event triggers
    def _trigger_msg_received(self, client: IOTSocketClient, msg: bytes):
        if self._on_msg_received is not None:
            self._on_msg_received(client, msg)

    def _trigger_shutdown(self, client: IOTSocketClient):
        self.clients.remove(client)
        if self._on_shutdown is not None:
            self._on_shutdown(client)

    def _trigger_client_connect(self, client: IOTSocketClient):
        if self._on_client_connect is not None:
            self._on_client_connect(client)

    def _handle_listening(self):
        self.socket.listen(500)
        while True:
            accepted_socket, accepted_addr = self.socket.accept()
            client = IOTSocketClient(sock=accepted_socket)
            client.on_msg_received = lambda msg: self._trigger_msg_received(client, msg)
            client.on_shutdown = lambda: self._trigger_shutdown(client)
            client.buffer_size = self.buffer_size
            self.clients.append(client)
            client.start_receiving()
            self._trigger_client_connect(client)

    def start_listening(self):
        self._listening_thread = function_thread(self._handle_listening, True, name=f"listening")
        self._listening_thread.start()