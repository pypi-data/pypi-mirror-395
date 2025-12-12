import abc
import json
import logging
import time
import os

from typing import Callable, NamedTuple, Optional, Union, Sequence, Dict, Any
from threading import get_ident, Timer

from pika import PlainCredentials, BlockingConnection, ConnectionParameters, BasicProperties
from pika.exceptions import AMQPConnectionError, AMQPChannelError, ConnectionClosedByBroker

from robertcommonbasic.basic.data.utils import generate_object_id


class RabbitMQConfig(NamedTuple):
    HOST: str
    PORT: int = 5672
    USER: str = ''
    PSW: str = ''
    VIR_HOST: str = ''
    HEART_BEAT: Optional[int] = None
    SOCKET_TIMEOUT: Union[int, float] = 10
    BLOCKET_CONNECTION_TIMEOUT: Union[int, float] = None
    SHORT_CONNECT: bool = True  # 短连接模式
    FRAME_MAX: Optional[int] = None


class RabbitMQAccessor:

    def __init__(self, config: RabbitMQConfig):
        self.config = config
        self.client = None
        self.callbacks = {}

    def __del__(self):
        self.close()

    def close(self):
        try:
            if self.is_connected():
                self.client.close()
        finally:
            self.client = None

    def get_client(self):
        if self.client is None:
            if self.config.USER is not None and self.config.PSW is not None and len(self.config.USER) > 0:
                credentials = PlainCredentials(self.config.USER, self.config.PSW)
                self.client = BlockingConnection(ConnectionParameters(host=self.config.HOST, port=self.config.PORT, virtual_host=self.config.VIR_HOST, credentials=credentials, socket_timeout=self.config.SOCKET_TIMEOUT, heartbeat=self.config.HEART_BEAT, blocked_connection_timeout=self.config.BLOCKET_CONNECTION_TIMEOUT, frame_max=self.config.FRAME_MAX))
            else:
                self.client = BlockingConnection(ConnectionParameters(host=self.config.HOST, port=self.config.PORT, virtual_host=self.config.VIR_HOST, socket_timeout=self.config.SOCKET_TIMEOUT, heartbeat=self.config.HEART_BEAT, blocked_connection_timeout=self.config.BLOCKET_CONNECTION_TIMEOUT, frame_max=self.config.FRAME_MAX))
        return self.client

    def is_connected(self) -> bool:
        if self.client and self.client.is_open:
            return True
        return False

    def set_call_result(self, call_method: str, **kwargs):
        if isinstance(self.callbacks, dict):
            call_method = self.callbacks.get(call_method)
            if isinstance(call_method, Callable):
                call_method(**kwargs)

    def enable_logging(self, enable_log: bool, callback: Callable = None):
        if enable_log is True:
            self.callbacks['debug_log'] = callback
        else:
            self.callbacks['debug_log'] = None

    def publish_exchange(self, exchange: str, routing_key: str, message: str, exchange_type: str = 'topic', **kwargs):
        client = self.get_client()
        if client is not None:
            try:
                channel = client.channel()
                channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=kwargs.get('durable', True))
                channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message, properties=BasicProperties(delivery_mode=kwargs.get('delivery_mode', 2), ))
                channel.close()
                return True
            finally:
                if self.config.SHORT_CONNECT is True or self.is_connected() is False:
                    self.close()

    def _get_queue_arguments(self, **kwargs):
        """获取队列参数
            20251205
        """
        arguments = None
        x_queue_type = kwargs.get('x_queue_type')
        if x_queue_type not in ['', None]:
            arguments = {"x-queue-type": x_queue_type}
        return arguments

    def publish_queue(self, queue_name: str, message: str, exchange: str = '', **kwargs):
        client = self.get_client()
        if client is not None:
            try:
                channel = client.channel()
                channel.queue_declare(queue=queue_name, durable=kwargs.get('durable', True), arguments=self._get_queue_arguments(**kwargs))
                channel.basic_publish(exchange=exchange, routing_key=queue_name, body=message, properties=BasicProperties(delivery_mode=kwargs.get('delivery_mode', 2), ))
                channel.close()
                return True
            finally:
                if self.config.SHORT_CONNECT is True or self.is_connected() is False:
                    self.close()

    def consume_exchange(self, exchange: str, exchange_type: str = 'topic', routing_key: str = '#', retry_interval: int = 10, callback: Callable = None, consumer_tag: Optional[str] = None, **kwargs):
        self.callbacks['receive_data'] = callback

        def real_callback(c, method, properties, body):
            c.basic_ack(delivery_tag=method.delivery_tag)
            self.set_call_result('receive_data', body=body)

        while True:
            try:
                connection = self.get_client()
                channel = connection.channel()
                channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=kwargs.get('durable', True))  # 声明一个Exchange
                channel.queue_declare(queue=exchange, exclusive=kwargs.get('exclusive', True), arguments=self._get_queue_arguments(**kwargs))  # 声明一个队里
                channel.queue_bind(exchange=exchange, queue=exchange, routing_key=routing_key)  # 绑定一个队列
                channel.basic_consume(exchange, on_message_callback=real_callback, consumer_tag=consumer_tag)
                channel.start_consuming()
            except ConnectionClosedByBroker as e:
                logging.error(f'exchange={exchange} ConnectionClosedByBroker({e.__str__()})')
            except AMQPChannelError as e:
                logging.error(f'exchange={exchange} AMQPChannelError({e.__str__()})')
            except AMQPConnectionError as e:
                logging.error(f'exchange={exchange} AMQPConnectionError({e.__str__()})')
            except Exception as e:
                logging.error(f'exchange={exchange} exception({e.__str__()})')
            finally:
                self.close()
            time.sleep(retry_interval)

    def consume_queue(self, queue_name: str, retry_interval: int = 10, callback: Callable = None, consumer_tag: Optional[str] = None, **kwargs):
        self.callbacks['receive_data'] = callback

        def real_callback(c, method, properties, body):
            c.basic_ack(delivery_tag=method.delivery_tag)
            self.set_call_result('receive_data', body=body)

        while True:
            try:
                connection = self.get_client()
                channel = connection.channel()
                channel.queue_declare(queue=queue_name, durable=kwargs.get('durable', True), arguments=self._get_queue_arguments(**kwargs))
                channel.basic_qos(prefetch_count=kwargs.get('prefetch_count', 1))
                channel.basic_consume(queue=queue_name, consumer_tag=consumer_tag, on_message_callback=real_callback)
                channel.start_consuming()
            except ConnectionClosedByBroker as e:
                logging.error(f'queue_name={queue_name} ConnectionClosedByBroker({e.__str__()})')
            except AMQPChannelError as e:
                logging.error(f'queue_name={queue_name} AMQPChannelError({e.__str__()})')
            except AMQPConnectionError as e:
                logging.error(f'queue_name={queue_name} AMQPConnectionError({e.__str__()})')
            except Exception as e:
                logging.error(f'queue_name={queue_name} exception({e.__str__()})')
            finally:
                self.close()
            time.sleep(retry_interval)


class MessageData(abc.ABC):

    def __init__(self):
        self.msg_id: Optional[str] = None

    def validate(self):
        pass

    def __str__(self):
        return f'msg_id: {self.msg_id}'


class RetryMessage(MessageData):
    def __init__(self):
        super().__init__()
        self.routing_key: Optional[str] = None
        self.message = {}
        self.exchange: Optional[str] = None
        self.retry_count: Optional[int] = None

    def __str__(self) -> str:
        return f'msg_id: {self.msg_id}, retry_count: {self.retry_count}, routing_key: {self.routing_key}, exchange: {self.exchange}'

    def to_dict(self) -> Dict:
        return {'msg_id': self.msg_id, 'routing_key': self.routing_key, 'exchange': self.exchange, 'retry_count': self.retry_count, 'message': self.message}

    @staticmethod
    def from_dict(data: Dict):
        message = RetryMessage()
        message.msg_id = data['msg_id']
        message.routing_key = data['routing_key']
        message.exchange = data['exchange'] or ''
        message.retry_count = data['retry_count']
        message.message = data['message']
        return message


class RabbitMQWorker(abc.ABC):
    config: RabbitMQConfig = None

    @classmethod
    def init(cls, config: RabbitMQConfig):
        cls.config = config

    def __init__(self,
                 queue_name: str,
                 exchange: str = None,
                 routing_keys: Sequence[str] = None,
                 heartbeat_interval: int = None,
                 busy_interval_minutes: int = None,
                 idle_interval_minutes: int = None,
                 test_mode: bool = False) -> None:
        """initialize a mq worker

        Args:
            queue_name (str): queue name
            exchange (str, optional): exchange name. Defaults to None.
            routing_keys (Sequence[str], optional): mq message routing keys. Defaults to None.
            heartbeat_interval (int, optional): MQ heartbeat interval in seconds. Defaults to None.
            busy_interval_minutes (int, optional): worker busy state max interval in minutes. Defaults to None.
            idle_interval_minutes (int, optional): worker idle state max interval in minutes. Defaults to None.
            test_mode (bool, optional): whether to init the worker in test mode. Defaults to False.
        """
        super().__init__()
        self._test_mode = test_mode
        self._queue_name = queue_name
        self._exchange = exchange or ''
        self._routing_keys = list(routing_keys or [])
        self._heartbeat_interval = heartbeat_interval or 300
        self._busy_interval_seconds = (busy_interval_minutes or 0) * 60
        self._idle_interval_seconds = (idle_interval_minutes or 10) * 60
        self._timer = None
        self._ident = get_ident()

        # if timeout interval is not properly set, choose a reasonable value
        max_idle_interval = self._heartbeat_interval * 2 + 1
        if self._busy_interval_seconds > max_idle_interval:
            self._busy_interval_seconds = max_idle_interval
        if self._idle_interval_seconds > max_idle_interval:
            self._idle_interval_seconds = max_idle_interval

    def _timeout_exit(self, is_idle: bool):
        os._exit(1)

    def _busy_timeout_callback(self):
        self._timeout_exit(is_idle=False)

    def _idle_timeout_callback(self):
        with self.new_connection() as connection:
            channel = connection.channel()
            queue = channel.queue_declare(queue=self._queue_name, durable=True)
            if queue.method.message_count:
                self._timeout_exit(is_idle=True)
            else:
                self.report_idle_state(is_idle=True)

    def report_idle_state(self, is_idle: bool = True):
        if self._timer:
            self._timer.cancel()
        if is_idle and self._idle_interval_seconds > 0:
            self._timer = Timer(self._idle_interval_seconds, self._idle_timeout_callback)
            self._timer.start()
        elif not is_idle and self._busy_interval_seconds > 0:
            self._timer = Timer(self._busy_interval_seconds, self._busy_timeout_callback)
            self._timer.start()

    @abc.abstractmethod
    def parse_data(self, message) -> MessageData:
        pass

    @abc.abstractmethod
    def process_data(self, data: MessageData) -> bool:
        pass

    def _process_data(self, message: MessageData) -> bool:
        return self.process_data(message)

    def _start_consuming(self):
        self.report_idle_state(is_idle=True)

        if self._exchange and self._routing_keys:
            for routing_key in self._routing_keys:
                self.channel.queue_bind(self._queue_name, self._exchange, routing_key)
        self.channel.basic_consume(self._queue_name, on_message_callback=self.callback)
        self.channel.start_consuming()

    def send_heartbeat(self):
        if self.connection:
            self.connection.sleep(0)
            self.report_idle_state(is_idle=False)

    def run(self):
        while True:
            try:
                self.report_idle_state(is_idle=True)
                with self.new_connection() as connection:
                    channel = connection.channel()
                    try:
                        channel.queue_declare(queue=self._queue_name, durable=True)
                    except:
                        channel = connection.channel()

                    channel.basic_qos(prefetch_count=1)
                    self.channel = channel
                    self.connection = connection
                    self._start_consuming()
            except Exception:
                self.channel = None
                self.connection = None
                sleep_seconds = 5
                logging.error(f'CONSUMER ABORTED, Retry after {sleep_seconds} seconds.')
                time.sleep(sleep_seconds)

    def new_connection(self) -> BlockingConnection:
        if self.config.USER is not None and self.config.PSW is not None and len(self.config.USER) > 0:
            credentials = PlainCredentials(self.config.USER, self.config.PSW)
            return BlockingConnection(ConnectionParameters(host=self.config.HOST, port=self.config.PORT, virtual_host=self.config.VIR_HOST, credentials=credentials, socket_timeout=self.config.SOCKET_TIMEOUT, heartbeat=self.config.HEART_BEAT, blocked_connection_timeout=self.config.BLOCKET_CONNECTION_TIMEOUT, frame_max=self.config.FRAME_MAX))
        else:
            return BlockingConnection(ConnectionParameters(host=self.config.HOST, port=self.config.PORT, virtual_host=self.config.VIR_HOST, socket_timeout=self.config.SOCKET_TIMEOUT, heartbeat=self.config.HEART_BEAT, blocked_connection_timeout=self.config.BLOCKET_CONNECTION_TIMEOUT, frame_max=self.config.FRAME_MAX))

    def translate_retry_message(self, retry_message: RetryMessage) -> RetryMessage:
        return retry_message

    def process_error_message(self, message: Dict[str, Any], method) -> bool:
        retry_message = RetryMessage()
        # When msg_id is empty, set the uuid value
        retry_message.msg_id = message.pop("msg_id", None) or generate_object_id()
        retry_message.retry_count = message.pop("retry_count", 0) + 1
        retry_message.exchange = self._exchange
        retry_message.routing_key = method.routing_key
        retry_message.message = message
        retry_message = self.translate_retry_message(retry_message)

        done = self.send_message_to_error_queue(retry_message)
        return done

    def _parse_body(self, body: bytes) -> Dict[str, Any]:
        data = None
        try:
            body_str = body.decode(encoding='utf-8')
            data = json.loads(body_str)
        except:
            try:
                data = eval(body)
            except:
                pass
        return data

    def _parse_message(self, data: Dict[str, Any]) -> MessageData:
        try:
            message = self.parse_data(data)
            if not message.msg_id:
                message.msg_id = data.get('msg_id')
                if not message.msg_id:
                    message.msg_id = generate_object_id()
                    data['msg_id'] = message.msg_id
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError('Invalid message', e)
        message.validate()
        return message

    def _handle_callback(self, method, body: bytes) -> bool:
        result = False
        data = self._parse_body(body)
        if not data or not isinstance(data, dict):
            try:
                body_str = body.decode(encoding='utf-8')
            except:
                body_str = str(body)
            result = self.process_dead_message(body_str, method.routing_key, invalid=True)
        else:
            try:
                message = self._parse_message(data)
                result = self.handle_parsed_message(message, method)
            except Exception as e:
                logging.error(f"Process message failed, routing key: {method.routing_key}, error: {e}")
            if not result:
                result = self.process_error_message(data, method)
        return result

    def callback(self, channel, method, property, body: bytes) -> bool:
        self.report_idle_state(is_idle=False)
        result = False
        try:
            result = self._handle_callback(method, body)
        except Exception as e:
            time.sleep(5)
        if result:
            channel.basic_ack(delivery_tag=method.delivery_tag)
        else:
            channel.basic_nack(delivery_tag=method.delivery_tag)
        self.report_idle_state(is_idle=True)
        return True

    def handle_parsed_message(self, message: MessageData, method) -> bool:
        result = False
        try:
            result = self._process_data(message)
        except Exception:
            logging.error(f"callback error, routing key: {method.routing_key}, message: {str(message)[:200]}")
        return result

    def process_dead_message(self, body: str, routing_key: str, invalid: bool = False) -> bool:
        queue_prefix = 'Invalid' if invalid else 'Dead'
        queue_name = f'{queue_prefix}.{self._queue_name}'
        done = self.rabbitmq_dynamic_send(queue_name, '', body)
        return done

    def send_message_to_error_queue(self, retry_message: RetryMessage):
        body = json.dumps(retry_message.to_dict())
        if retry_message.retry_count <= len([60, 300, 1800, 7200]):
            queue_name, queue_args = self.get_retry_queue(retry_message.retry_count)
            result = self.rabbitmq_dynamic_send(queue_name, '', body, queueArgs=queue_args)
        else:
            result = self.process_dead_message(body, retry_message.routing_key)
        return result

    @classmethod
    def get_retry_queue(cls, retry):
        queue_prefix = 'ErrorRetry'
        ttl = [60, 300, 1800, 7200][retry-1]
        arguments = {"x-dead-letter-exchange": '', "x-dead-letter-routing-key": 'ErrorRetryWorker', "x-message-ttl": ttl*1000}
        queue = f"{queue_prefix}_{retry}_{ttl}"
        return queue, arguments

    def rabbitmq_dynamic_send(self, queueName, exchange, sendValStr, queueArgs=None, sendToTestMQ=None) -> bool:
        sendValStr = str(sendValStr)
        MAX_RETRY = 4
        for i in range(1, MAX_RETRY + 1):
            try:
                channel = self.channel
                if queueArgs:
                    channel.queue_declare(queue=queueArgs["x-dead-letter-routing-key"], durable=True)
                    channel.queue_declare(queue=queueName, durable=True, arguments=queueArgs)
                elif not exchange:
                    channel.queue_declare(queue=queueName, durable=True)
                channel.basic_publish(exchange=exchange or '', routing_key=queueName, body=sendValStr, properties=BasicProperties(delivery_mode=2))
                return True
            except Exception as e:
                if i == MAX_RETRY:
                    logging.error(f'Failed to send message to {queueName} after all retries! message={sendValStr[:1000]}, sendToTestMQ={sendToTestMQ}')
                else:
                    logging.error(f'Failed to send message to {queueName}, body={sendValStr}. {e.__str__()}, Retrying for {i}th time...')
                    time.sleep(1)
        return False
