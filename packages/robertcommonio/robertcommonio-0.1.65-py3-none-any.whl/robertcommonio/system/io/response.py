import logging
import os
import json
import pandas as pd

from typing import Tuple, Type, Optional, Any
from decimal import Decimal
from enum import Enum
from bson import ObjectId
from datetime import datetime, date
from functools import wraps as func_wraps
from uuid import uuid4

from flask import Response, has_request_context, make_response, request, send_from_directory

from robertcommonbasic.basic.cls.utils import daemon_thread
from robertcommonbasic.basic.dt.utils import DATETIME_FMT_FULL, DATETIME_FMT_DATE, get_datetime
from robertcommonbasic.basic.error.utils import S_OK, E_INTERNAL, RobertError
from robertcommonbasic.basic.validation import input
from robertcommonbasic.basic.log import utils as logutils
from robertcommonbasic.basic.os.path import create_dir_if_not_exist, get_sys_path


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, bytes):
            for encoding in ['gbk', 'utf-8']:
                try:
                    return obj.decode(encoding=encoding, errors='ignore')
                except:
                    pass
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.strftime(DATETIME_FMT_FULL)
        elif isinstance(obj, date):
            return obj.strftime(DATETIME_FMT_DATE)
        elif str(obj).lower() == 'nan':
            return None
        elif isinstance(obj, pd.Series):
            return obj.to_json(orient='values')
        elif isinstance(obj, pd.DataFrame):
            return obj.to_json(orient='records')
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, Decimal):
            return float(obj)
        else:
            return obj


class RequestLogLevel:
    LOG_NULL = 0
    LOG_URL = 1
    LOG_URL_INPUT = 2
    LOG_URL_INPUT_AND_COST = 3
    LOG_ALL = 4


class WatchRequestOperation:
    """请求操作记录"""

    def __init__(self, url: str, **kwargs):
        self.url = url
        self.start = get_datetime()  # 启动时间
        self.kwargs = kwargs    # url post header params response cost

    @daemon_thread
    def record(self):
        try:
            self.handle_record(create_time_utc=self.start, info={'cost': self.cost(), 'url': self.url, 'params': self.kwargs})
        except Exception:
            pass

    def handle_record(self, **kwargs):
        pass

    def end(self, **kwargs):
        self.end = get_datetime()   # 结束时间
        self.kwargs.update(**kwargs)
        self.record().start()

    def cost(self):
        return '{:.3f}'.format((self.end - self.start).total_seconds())


def robert_response(is_success, data, code, msg='') -> Response:
    if not code:
        code = S_OK if is_success else E_INTERNAL
    return Response(
        json.dumps({
            'success': is_success,
            'code': code,
            'data': data,
            'msg': msg
        }, cls=Encoder, ensure_ascii=False),
        mimetype='application/json')


def robert_response_error(data=None, code='0', msg='') -> Response:
    if isinstance(data, Exception):
        logging.error(data)
        data = str(data)
    return robert_response(False, data, code, msg)


def robert_response_success(data=None, code='1') -> Response:
    return robert_response(True, data, code)


ErrorTypes = Tuple[Type[Exception], ...]


def _get_error_response(e: Exception, user_errors: ErrorTypes) -> Response:
    is_robert_error = isinstance(e, RobertError)
    is_user_error = user_errors and isinstance(e, user_errors) or is_robert_error

    msg = getattr(e, 'msg', e.__str__())
    data = dict(error_type=str(type(e)),
                detail=getattr(e, 'data', getattr(e, 'detail', None)))

    if is_user_error:
        code = getattr(e, 'code', E_INTERNAL)
        logging.error(e.__str__())
    else:
        code = E_INTERNAL
        data['inner_code'] = getattr(e, 'code', None)
        # noinspection PyUnusedLocal
        url = request.url or 'N/A'
        logutils.log_unhandled_error()
    return robert_response_error(code=code, msg=msg, data=data)


def response_wrapper(func, tolerable_errors: Optional[ErrorTypes] = None):
    tolerable_errors = input.ensure_tuple_of(
        'tolerable_errors', tolerable_errors, (input.ensure_not_none_of, Type))

    @func_wraps(func)
    def wrapper(*args, **kwargs) -> Response:
        try:
            if has_request_context() and 'doc' in request.args:
                rv = make_response(func.__doc__)
                rv.headers['Content-Type'] = 'plain/text'
                return rv
            else:
                rv = func(*args, **kwargs)
                return robert_response_success(data=rv)
        except Exception as e:
            return _get_error_response(e, tolerable_errors)

    return wrapper


def response_wrapper_with_log(log_level: RequestLogLevel = RequestLogLevel.LOG_NULL, folder: Optional[str] = None):

    def inner_response_wrapper(func, tolerable_errors: Optional[ErrorTypes] = None):
        tolerable_errors = input.ensure_tuple_of(
            'tolerable_errors', tolerable_errors, (input.ensure_not_none_of, Type))

        def _save_log(out_time, log: dict):
            if len(log) > 0:
                base_folder = folder if folder is not None else get_sys_path()
                log_folder = f"{base_folder}/file/log/request"
                create_dir_if_not_exist(log_folder)
                log_path = f"{log_folder}/request_{out_time.strftime('%Y_%m_%d')}.log"
                with open(log_path, 'a+') as f:
                    f.write(f"{out_time.strftime('%Y-%m-%d %H:%M:%S.%f')} :: {log}\n")

        def _output_log(id, request, response, time):
            request_log = {}
            out_time = get_datetime()
            if log_level >= RequestLogLevel.LOG_URL:
                request_log['id'] = id
                request_log['path'] = request.path
                request_log['method'] = request.method
                request_log['type'] = request.content_type
                request_log['ip'] = str(request.headers.get('X-Real-IP')) if 'X-Real-IP' in request.headers.keys() else request.remote_addr

            if log_level >= RequestLogLevel.LOG_URL_INPUT:
                request_log['input'] = str(request.data, encoding="utf-8")

            if log_level >= RequestLogLevel.LOG_URL_INPUT_AND_COST:
                request_log['cost'] = '{:.3f}'.format((out_time - time).total_seconds())

            if log_level >= RequestLogLevel.LOG_ALL:
                request_log['ouput'] = str(response.data, encoding="utf-8")

            _save_log(out_time, request_log)

        @func_wraps(func)
        def wrapper(*args, **kwargs) -> Response:
            try:
                if has_request_context() and 'doc' in request.args:
                    rv = make_response(func.__doc__)
                    rv.headers['Content-Type'] = 'plain/text'
                    return rv
                else:
                    #
                    request_start = get_datetime()

                    request_id_key = f"X-Request-ID"
                    request_id_value = str(uuid4())
                    rv = func(*args, **kwargs)
                    response = robert_response_success(data=rv)
                    response.headers.add(request_id_key, request_id_value)

                    _output_log(request_id_value, request, response, request_start)
                    return response
            except Exception as e:
                return _get_error_response(e, tolerable_errors)

        return wrapper

    return inner_response_wrapper


def response_wrapper_with_operation(op_handle: Optional[Any] = None, save_response: bool = False):

    def inner_response_wrapper(func, tolerable_errors: Optional[ErrorTypes] = None):
        tolerable_errors = input.ensure_tuple_of('tolerable_errors', tolerable_errors, (input.ensure_not_none_of, Type))

        @func_wraps(func)
        def wrapper(*args, **kwargs) -> Response:
            try:
                if has_request_context() and 'doc' in request.args:
                    rv = make_response(func.__doc__)
                    rv.headers['Content-Type'] = 'plain/text'
                    return rv
                else:
                    request_id_value = str(uuid4())
                    op_handle_class = op_handle if op_handle is not None else WatchRequestOperation
                    sw = op_handle_class(request.url, method=request.method, data=str(request.data, encoding="utf-8")[:200], id=request_id_value, ip=str(request.headers.get('X-Real-IP')) if 'X-Real-IP' in request.headers.keys() else request.remote_addr)
                    res = None
                    try:
                        res = func(*args, **kwargs)
                        response = robert_response_success(data=res)
                        response.headers.add(f"X-Request-ID", request_id_value)
                        return response
                    finally:
                        sw.end(respone=res if save_response else None)
            except Exception as e:
                return _get_error_response(e, tolerable_errors)

        return wrapper

    return inner_response_wrapper


def file_response_wrapper(func, tolerable_errors: Optional[ErrorTypes] = None):
    tolerable_errors = input.ensure_tuple_of(
        'tolerable_errors', tolerable_errors, (input.ensure_not_none_of, Type))

    @func_wraps(func)
    def wrapper(*args, **kwargs) -> Response:
        try:
            file_path = func(*args, **kwargs)
            rsp = send_from_directory(path=file_path, directory=os.path.dirname(file_path), filename=os.path.basename(file_path), as_attachment=True, attachment_filename=os.path.basename(file_path))
            rsp.headers['Content-Type'] = "application/octet-stream; charset=UTF-8"
            return rsp
        except Exception as e:
            return _get_error_response(e, tolerable_errors)

    return wrapper
