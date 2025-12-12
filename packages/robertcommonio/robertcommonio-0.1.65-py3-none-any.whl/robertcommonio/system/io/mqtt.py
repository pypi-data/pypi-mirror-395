import logging
import time
from datetime import datetime
from typing import Callable, NamedTuple, Union

import paho.mqtt.client as mqtt

'''
    pip install paho-mqtt==1.6.1
'''


class MQTTConfig(NamedTuple):
    HOST: str
    PORT: int = 1883    # 使用SSL/TLS的默认端口是 8883
    USER: str = None
    PSW: str = None
    TOPIC: str = ''
    CLIENT_ID: str = ''
    KEEP_ALIVE: int = 60
    SHORT_CONNECT: bool = False  # 短连接模式
    MIN_RECONNECT_DELAY: int = 1
    MAX_RECONNECT_DELAY: int = 120


class MQTTAccessor:

    def __init__(self, config: MQTTConfig):
        self.config = config
        self.client = None
        self.thread_exit = False
        self.callbacks = {}
        self.last_pub_mid = None    # 上一个发布ID

    def __del__(self):
        self.close()

    def __str__(self):
        client_id = self.client._client_id if self.client is not None else ''
        if isinstance(client_id, bytes):
            client_id = client_id.decode()
        return f"mqtt({client_id})" if len(client_id) > 0 else 'mqtt'
    
    def exit(self):
        self.thread_exit = True
        self.close()

    def connack_string(self, connack_code: int):
        """Return the string associated with a CONNACK result."""
        if connack_code == 0:
            return "success"
        elif connack_code == 1:
            return "unacceptable protocol version."
        elif connack_code == 2:
            return "identifier rejected."
        elif connack_code == 3:
            return "broker unavailable."
        elif connack_code == 4:
            return "bad user name or password."
        elif connack_code == 5:
            return "not authorised."
        else:
            return f"unknown reason({connack_code})."

    def on_connect(self, client, userdata, flags, rc):
        self.set_call_result('debug_log', content=f"{self} connect success({flags})" if int(str(rc)) == 0 else f"fail({self.connack_string(rc)})({flags})")

    def on_message(self, client, userdata, message):
        self.set_call_result('receive_data', topic=message.topic, payload=message.payload)
        self.set_call_result('debug_log', content=f"{self} recv message({message.topic} {message.payload})")

    def on_log(self, client, userdata, level, messages):
        self.set_call_result('debug_log', content=f"{self} recv log ({level} {messages})")

    def on_subscribe(self, client, userdata, mid, granted_qos):
        self.set_call_result('debug_log', content=f"{self} subscribe(mid: {mid}) success")

    def on_disconnect(self, client, userdata, rc):
        self.set_call_result('debug_log', content=f"{self} disconect({self.connack_string(rc)})")

    def on_publish(self, client, userdata, mid):
        self.last_pub_mid = mid
        self.set_call_result('debug_log', content=f"{self} publish(mid: {mid}) success")

    def close(self):
        try:
            if self.client:
                self.client.disconnect()
            if self.client:
                self.client.loop_stop()
        except Exception as e:
            logging.error(f"{self} close fail({e.__str__()}")
        finally:
            self.client = None

    def get_client(self, client_mode='sub'):
        if self.client is None:
            try:
                clean_session = self.config.SHORT_CONNECT  # False表示要建立一个持久性会话
                if self.config.CLIENT_ID is None or len(self.config.CLIENT_ID) == 0:
                    client = mqtt.Client(client_id='', clean_session=True)
                else:
                    client = mqtt.Client(self.config.CLIENT_ID, clean_session=clean_session)
                if self.config.USER is not None and self.config.PSW is not None and len(self.config.USER) > 0:
                    client.username_pw_set(self.config.USER, self.config.PSW)
                client.on_connect = self.on_connect
                client.on_message = self.on_message
                client.on_subscribe = self.on_subscribe
                client.on_disconnect = self.on_disconnect
                client.on_publish = self.on_publish
                client.on_log = self.on_log
                client.connect(self.config.HOST, self.config.PORT, self.config.KEEP_ALIVE)
                client.reconnect_delay_set(self.config.MIN_RECONNECT_DELAY, self.config.MAX_RECONNECT_DELAY)
                if client_mode == 'pub':
                    client.loop_start()

                    wait = 5
                    while not client.is_connected() and wait > 0:    # 等待连接
                        time.sleep(1)
                        wait = wait - 1

                    if client.is_connected() is False:
                        client.disconnect()
                        client.loop_stop()
                        raise Exception(f"{self} not connected")
                self.client = client
            except Exception as e:
                raise Exception(f"{self} connect fail({e.__str__()})")
        return self.client

    def publish_topic(self, topic: str, message: str, qos: int = 0, wait: float = 3) -> bool:
        client = self.get_client('pub')
        if client is not None:
            connect_status = False
            if client._state != 2:
                connect_status = True
            else:
                self.set_call_result('debug_log', content=f"{self} client status({client._state}) fail")

            try:
                if connect_status is True:
                    info = client.publish(topic, payload=message, qos=qos)
                    now = datetime.now()
                    while info.mid != self.last_pub_mid:
                        if (datetime.now() - now).total_seconds() >= wait:    # 超时3s
                            self.set_call_result('debug_log', content=f"{self} client publish({info.mid}) timeout")
                            break
                        time.sleep(0.1)
                    info.wait_for_publish(wait)
                    if info.rc == mqtt.MQTT_ERR_SUCCESS:
                        return True
                    elif info.rc == mqtt.MQTT_ERR_NO_CONN:
                        connect_status = False
                    raise Exception(f"publish fail({info})")
                else:
                    raise Exception(f"invalid state({client._state})")
            finally:
                if self.config.SHORT_CONNECT is True or connect_status is False or self.is_connected() is False:
                    self.close()
        else:
            raise Exception(f"no client")

    def subscribe_topics(self, topics: Union[str, list], qos: int = 0, retry_interval: int = 10, callback: Callable = None):
        self.callbacks['receive_data'] = callback
        while self.thread_exit is False:
            try:
                client = self.get_client()
                if client:
                    if isinstance(topics, str):
                        client.subscribe(topics, qos=qos)
                    elif isinstance(topics, list):
                        for topic in topics:
                            client.subscribe(topic, qos=qos)
                    self.set_call_result('debug_log', content=f"{self} subscribe({topics})")
                    client.loop_forever()
            except Exception as e:
                logging.error(f'subscribe topics={topics} fail({e.__str__()})', exc_info=True)
            finally:
                self.close()
                self.set_call_result('debug_log', content=f"{self} close subscribe")
            time.sleep(retry_interval)

    def is_connected(self) -> bool:
        if self.client and self.client.is_connected():
            return True
        return False

    def enable_logging(self, callback: Callable = None):
        self.callbacks['debug_log'] = callback

    def set_call_result(self, call_method: str, **kwargs):
        if isinstance(self.callbacks, dict):
            call_method = self.callbacks.get(call_method)
            if call_method is not None and isinstance(call_method, Callable):
                call_method(**kwargs)
