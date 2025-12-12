import json
import time
from robertcommonio.system.io.mqtt import MQTTConfig, MQTTAccessor
from datetime import datetime

HOST = 'mqtt.smartbeop.com'
PORT = 1884
client_id = '123456'
TOPIC = 'clp' #'SUBSTATION/MASTER/200120-1/S_SNT_DA' #'SUBSTATION/MASTER/200120-1/S_SNT_DAT'
USER = 'clp'
PSW = '9T3QV7hdjcHNIHpt'

all_values = {}


def call_back(topic: str, payload: bytes):
    try:
        values = json.loads(payload.decode())
        print(values)
        if isinstance(values, list):
            for value in values:
                if 'ID' in value.keys() and 'TS' in value.keys() and 'ST' in value.keys() and  'VR' in value.keys():
                    time = datetime.utcfromtimestamp(int(value.get('TS'))).replace(second=0).strftime("%Y-%m-%d %H:%M:%S")
                    if time not in all_values.keys():
                        all_values[time] = {}
                    all_values[time][f"{value.get('ID')}_{value.get('ST')}"] = eval(value.get('VR'))[0]

            print(f"{all_values}")
    except Exception as e:
        print(e.__str__())


def log_call_back(**kwargs):
    print(kwargs)


def test_pub():
    accessor = MQTTAccessor(MQTTConfig(HOST=HOST, PORT=PORT, USER=USER, PSW=PSW, TOPIC=TOPIC, CLIENT_ID=client_id, KEEP_ALIVE=60))
    while True:
        accessor.publish_topic(TOPIC, datetime.now().strftime('%H:%M:%S'), 0)
        time.sleep(2)

def test_sub():
    accessor = MQTTAccessor(MQTTConfig(HOST=HOST, PORT=PORT, USER=USER, PSW=PSW, TOPIC=TOPIC, CLIENT_ID=client_id, KEEP_ALIVE=60))
    accessor.subscribe_topics(['clp', 'clp/s1'], 0, 10, call_back)


def test_sub1():
    accessor = MQTTAccessor(MQTTConfig(HOST='mqtt.clpcluster.com', PORT=1883, USER='clp', PSW='JuMkBhMFqbfsPgymYNcC', CLIENT_ID=client_id, KEEP_ALIVE=60))
    accessor.subscribe_topics(['test/sub'], 0, 10, call_back)


def test_sub2():
    accessor = MQTTAccessor(MQTTConfig(HOST='121.37.104.218', PORT=1883, USER='admin', PSW='abc@123', CLIENT_ID='1212121111', KEEP_ALIVE=60))
    accessor.publish_topic("SUBSTATION/MASTER/050030-1/S_SNT_DAT", datetime.now().strftime('%H:%M:%S'), 0)
    print()


def test_sub3():
    accessor = MQTTAccessor(MQTTConfig(HOST='mqtt.clpcluster.com', PORT=8883, USER='clp', PSW='JuMkBhMFqbfsPgymYNcC', CLIENT_ID=client_id, KEEP_ALIVE=60))
    accessor.publish_topic('test/sub', '123456')
    accessor.subscribe_topics(['test/sub'], 0, 10, call_back)


def test_sub_and_pub():

    def call_back1(topic: str, payload: bytes):
        try:
            values = json.loads(payload.decode())
            print(values)
            accessor.publish_topic('test_sub2', '123456', wait=0)
        except Exception as e:
            print(e.__str__())

    accessor = MQTTAccessor(MQTTConfig(HOST='mqtt.clpcluster.com', PORT=1883, USER='clp', PSW='JuMkBhMFqbfsPgymYNcC', CLIENT_ID=client_id, KEEP_ALIVE=60))
    accessor.subscribe_topics(['test_sub1'], 0, 10, call_back1)


def test_pub_max():
    import json
    from robertcommonio.system.io.file import FileType, FileConfig, FileAccessor
    json_contents = FileAccessor(FileConfig(PATH=r"C:\Users\85101\Desktop\69132e0966f2b07698766e1e.zip", PSW="GateWayCore", MODE=FileType.AES_ZIP)).read()
    for file_name, file_content in json_contents.items():
        file_content1 = json.loads(file_content.decode())
        accessor = MQTTAccessor(MQTTConfig(HOST='mqtt.clpcluster.com', PORT=1883, USER='clp', PSW='JuMkBhMFqbfsPgymYNcC', CLIENT_ID=client_id, KEEP_ALIVE=60))
        accessor.enable_logging(log_call_back)
        accessor.publish_topic('tes123', file_content[0:1000000], 0)


test_pub_max()

