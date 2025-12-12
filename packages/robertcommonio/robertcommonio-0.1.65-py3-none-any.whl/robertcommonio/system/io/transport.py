import socket
import time
from abc import abstractmethod
from typing import Optional
from uuid import uuid1
from serial import Serial


class IOTTransport:

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.transport = None
        self.timeout = None
        self.uuid = uuid1()
        self.events = {}    # events

    def __str__(self):
        return f"{self.__class__.__name__}({self.uuid})"

    def __del__(self):
        self.exit()

    def exit(self):
        pass

    def is_connected(self) -> bool:
        return True
    
    def get_timeout(self):
        return self.timeout

    def set_timeout(self, timeout: Optional[float] = None):
        self.timeout = timeout

    @abstractmethod
    def start(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def send(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def extra_on_connect(self, transport):
        """连接上服务器后需要进行的初始化操作"""
        raise NotImplementedError()

    @abstractmethod
    def extra_on_close(self, transport):
        """连接上服务器后需要进行的初始化操作"""
        raise NotImplementedError()

    @abstractmethod
    def extra_on_receive(self, transport, datas: bytes):
        raise NotImplementedError()


class IOTTransportSerial(IOTTransport):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transport = None

    def is_connected(self) -> bool:
        return self.transport and self.transport.isOpen()

    def start(self):
        if self.transport is None:
            self.transport = Serial(timeout=self.get_timeout(), **self.kwargs)
            if self.is_connected() is True:
                self.extra_on_connect(self.transport)

        if self.is_connected() is False:
            self.transport.open()
            if self.is_connected() is True:
                self.extra_on_connect(self.transport)
        return self.is_connected()
    
    def exit(self):
        if self.transport:
            if self.is_connected() is True:
                self.transport.close()
            self.extra_on_close(self.transport)
        self.transport = None

    def write(self, data: bytes):
        if self.is_connected() is True: 
            if self.transport.write(data) > 0:
                return True
        return False
    
    def read(self, length: int):
        data = bytearray()
        if self.is_connected() is True:
            try:
                start_time = time.time() if self.get_timeout() is not None else 0
                if isinstance(length, int):
                    while len(data) < length:
                        d = self.transport.read(1)
                        if self.get_timeout() is not None:
                            read_duration = time.time() - start_time
                        else:
                            read_duration = 0

                        if read_duration > self.get_timeout():
                            data.extend(d)
                            break

                        if not d:
                            raise Exception(f"close")
                        else:
                            data.extend(d)
            except Exception as e:
                self.exit()
                return None
        if data is not None and len(data) > 0:
            self.extra_on_receive(self.transport, data)
        return data


class IOTTransportSocket(IOTTransport):

    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs
        self.transport = None
        self.connected = False

    def is_connected(self) -> bool:
        return self.transport and self.connected

    def start(self):
        if self.transport is None:
            self.transport = socket.socket(socket.AF_INET, self.kwargs.get('type', 1))
            self.transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
        if self.transport:
            if self.is_connected() is False:
                self.transport.settimeout(10)
                self.transport.connect((self.kwargs.get('host'), self.kwargs.get('port')))
                self.transport.settimeout(None)
                self.connected = True
                self.extra_on_connect(self.transport)
                if self.get_timeout() is None:
                    self.transport.settimeout(self.get_timeout())
        return self.is_connected()

    def exit(self):
        if self.transport:
            if self.is_connected() is True:
                self.transport.close()
            self.extra_on_close(self.transport)
        self.connected = False
        self.transport = None

    def write(self, data: bytes):
        if self.is_connected() is True:
            if self.transport.send(data) > 0:
                return True
        return False

    def read(self, length: int, size: int = 1024):
        data = bytearray()
        if self.is_connected() is True:
            try:
                if isinstance(length, int):
                    while len(data) < length:
                        pack_size = size if length - len(data) > size else length - len(data)
                        d = self.transport.recv(pack_size)
                        if not d:
                            raise Exception(f"close")
                        elif len(d) < pack_size:
                            data.extend(d)
                            break
                        else:
                            data.extend(d)
                else:
                    data.extend(self.transport.recv(size))
            except socket.timeout as e:
                pass
            except Exception as e:
                self.exit()
                return None
        if data is not None and len(data) > 0:
            self.extra_on_receive(self.transport, data)
        return data


class IOTClient:

    def __init__(self, transport: IOTTransport, timeout: int = 1, retries: int = 3):
        self.uuid = uuid1()
        self.transport = transport
        self.timeout = timeout
        self.retries = max(1, retries)

    def __str__(self):
        return f"{self.__class__.__name__}({self.uuid})"

    def __del__(self):
        self.exit()

    def exit(self):
        if self.transport:
            self.transport.exit()
            del self.transport
        self.transport = None

    def start(self):
        if self.transport:
            self.transport.start()
