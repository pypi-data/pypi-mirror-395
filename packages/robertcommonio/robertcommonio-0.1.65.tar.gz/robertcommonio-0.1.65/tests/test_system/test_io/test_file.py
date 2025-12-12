from robertcommonio.system.io.file import FileType, FileConfig, FileAccessor
from robertcommonbasic.basic.dt.utils import parse_time
from robertcommonbasic.basic.os.file import scan_files
from robertcommonio.system.io.http import HttpTool
import base64
import json
import re
import pyzipper
import pandas as pd

from typing import Optional
from io import BytesIO


def test_csv():
    accessor = FileAccessor(FileConfig(PATH='E:/test.csv', MODE=FileType.CSV))
    accessor.save('ss1')


def test_zip_csv():
    accessor = FileAccessor(FileConfig(PATH=r'E:\Beop\Code\Git\datapushserver\file\real\testdtu\20220711\request_20220711081000.zip', PSW='123456', MODE=FileType.AES_ZIP))
    json_contents = accessor.read()
    for file_name, file_content in json_contents.items():
        if len(file_content) > 0:
            if file_name.endswith('.json'):
                body = json.loads(file_content.decode())
                body = body.get('body')
                file_type = body.get('type', '')
                file_psw = body.get('psw', '')
                file_path = body.get('path', '')
                file_name = body.get('name', '')
                file_content = body.get('content', '')
                accessor = FileAccessor(FileConfig(PATH=BytesIO(base64.b64decode(file_content.encode())), PSW='RNB.beop-2019', MODE=FileType.AES_ZIP))
                json_contents = accessor.read()
                for file_name, file_content in json_contents.items():
                    datas = [p.split(',') for p in file_content.decode('gbk').split(';')]
                    points = {}
                    for data in datas:
                        if len(data) >= 2 and len(data[0]) > 0:
                            points[data[0]] = data[1]

                    value = {'dtuName': 'test2020',
                    'dataType': 0,
                    'dataSource': '',
                    'serverCode': 6,
                    'updateTime': '2022-07-11 08:10:00',
                    'dataStruct': [{'time': '2022-07-11 08:10:00', 'type': 0, 'points': points}]}
                    body = json.dumps(value, ensure_ascii=False).encode("utf-8")
                    rt = HttpTool().send_request(url=f"http://beopservice.smartbeop.com/site/v1.0/update_raw_data_v2", method='POST', headers={'content-type': 'application/json'}, data=body, timeout=30)
                    print(rt)


def test_zip_csv1():
    content = b''
    with open(r'E:\DTU\real\atlanta\20210907\his_20210907095301.zip', 'rb') as f:
        content = f.read()

    accessor = FileAccessor(FileConfig(PATH=BytesIO(content), PSW=['aa', '123456', 'RNB.beop-2019', ''],
                                       MODE=FileType.AES_ZIP))
    results = accessor.read()
    for k, v in results.items():
        print(k)
    results = {}
    with pyzipper.AESZipFile(BytesIO(content)) as zip:
        zip.setpassword('RNB.beop-2019'.encode('utf-8'))
        for file in zip.namelist():
            results[file] = zip.read(file)
    print(results)


def test_excel():
    #import pandas as pd
    #df = pd.read_excel(r'E:\DTU\point\hongqiao_api\point202202221.xls', sheet_name=None)

    accessor = FileAccessor(FileConfig(PATH=r'E:\DTU\point\hongqiao_api\point20220224.xls', MODE=FileType.Excel, NAME=None))
    results = accessor.read()
    for k, v in results.items():
        print(k)
    del accessor

    accessor1 = FileAccessor(FileConfig(PATH=r'E:\DTU\point\hongqiao_api\point20220224_new.xls', MODE=FileType.Excel, NAME=None))
    accessor1.save(file_content=results)
    print()


def test_pcc():
    records = pd.read_csv('E:/PCC_AB_Davis_AirHandlers_Analog (3).csv', keep_default_na=False)
    for index, row in records.iterrows():
        row_value = row.to_dict()
        values = {}
        for k, v in row_value.items():
            if v is not None and len(str(v)) > 0:
                if isinstance(v, str) and v.find(',') > 0:
                    v = v.replace(',', '')
                print(v)


def test_csv_ansi():
    accessor = FileAccessor(FileConfig(PATH=r'C:\nginx\resource\point\iot_modbus/iot_modbus (1).csv', MODE=FileType.CSV))
    points = accessor.read()
    print(points)


def test_device_log_to_csv(file_folder: str):
    """"""
    LOG_LINE_RE = re.compile(
        r"^\s*['\"]?(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d{1,6})?)\s+[^\n]*?::\[(?P<method>[A-Za-z]+)\]\s+(?P<path>\S+)\s+\((?P<ip>[^)]+)\)\((?P<body>\{.*\})\)?",
        re.DOTALL,
    )
    records = []

    def parse_body_device(body_text: Optional[str]) -> Optional[str]:
        if not body_text:
            return None
        try:
            data = json.loads(body_text)
            value = data.get("modbusTag")
            if isinstance(value, str):
                return value
            return None
        except json.JSONDecodeError:
            # 有些日志可能出现单引号或非标准 JSON，尝试简单修正
            try:
                fixed = body_text.replace("'", '"')
                data = json.loads(fixed)
                value = data.get("modbusTag")
                return value if isinstance(value, str) else None
            except Exception:
                return None

    for file_path in scan_files(file_folder):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f.readlines():
                m = LOG_LINE_RE.match(line.strip())
                if not m:
                    continue
                ts_raw = m.group("ts")
                path = m.group("path")
                body = m.group("body")

                time_str = parse_time(ts_raw).strftime('%Y-%m-%d %H:%M:%S')
                action_type = 1 if "/remoteopen" in path.lower() else 0
                device = parse_body_device(body)
                if isinstance(device, str) and len(device) > 0:
                    records.append({
                        "TIME": time_str,
                        "DEVICE": device,
                        "TYPE": action_type,
                        "MODE": 0,
                        "VALUE": "",
                        "USER": "admin",
                        "RESULT": 1,
                        "REMARK": "",
                    })

    import csv
    fieldnames = ["TIME", "DEVICE", "TYPE", "MODE", "VALUE", "USER", "RESULT", "REMARK"]
    with open(r"ab.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=',', lineterminator='\n', extrasaction='ignore')
        writer.writeheader()
        for r in records:
            writer.writerow(r)
    print()

def test():
    import re
    line = '2024-07-29 07:52:00.049149 ::[POST] /api/remoteOpen (10.192.1.241)({"modbusTag":"SND001"})'
    LOG_LINE_RE = re.compile(
        r"^\s*['\"]?(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d{1,6})?)\s+[^\n]*?::\[(?P<method>[A-Za-z]+)\]\s+(?P<path>\S+)\s+\((?P<ip>[^)]+)\)\((?P<body>\{.*\})\)?",
        re.DOTALL,
    )
    m = LOG_LINE_RE.match(line)
    print('matched=', bool(m))
    if m:
        print(m.groupdict())
    else:
        print('no match')
    print()


#test()
test_device_log_to_csv(r"C:\Users\85101\Desktop\request\request_post_*.log")