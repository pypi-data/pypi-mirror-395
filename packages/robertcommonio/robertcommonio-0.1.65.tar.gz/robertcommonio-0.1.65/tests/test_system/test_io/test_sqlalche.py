import time
from typing import Union
from robertcommonio.system.io.sqlalche import SQLAlCheAccessor, SQLQueryBuilder
from robertcommonbasic.basic.os.file import check_file_exist
from robertcommonbasic.basic.data.utils import chunk_list
from encodings.aliases import aliases as encodings_aliases
import sqlite3
import cx_Oracle
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


def test_sqlite():
    accessor = SQLAlCheAccessor()
    accessor.add_engine('sqlite0', 'sqlite+pysqlite:///:memory:')
    accessor.execute_sql('sqlite0', 'CREATE TABLE some_table (x int, y int)')
    accessor.execute_sql('sqlite0', 'INSERT INTO some_table (x,y) VALUES (:x, :y)', [{"x": 1, "y": 1}, {"x": 2, "y": 4}])
    print(accessor.read_sql('sqlite0', 'SELECT * FROM some_table'))


def test_sqlite1():
    accessor = SQLAlCheAccessor()
    accessor.add_engine('sqlite0', 'sqlite:///config.db')
    accessor.execute_sql('sqlite0', 'CREATE TABLE some_table (x int, y int)')
    accessor.execute_sql('sqlite0', 'INSERT INTO some_table (x,y) VALUES (:x, :y)', [{"x": 1, "y": 1}, {"x": 2, "y": 4}])
    print(accessor.read_sql('sqlite0', 'SELECT * FROM some_table'))


def test_sqlite2():
    db = '/data/config.db'
    print(check_file_exist(db))
    accessor = SQLAlCheAccessor()
    accessor.add_engine('sqlite0', f'sqlite:///{db}?check_same_thread=False')
    print(accessor.read_sql('sqlite0', 'SELECT * FROM task'))


def convert(content: Union[str, bytes]):
    print(f"{type(content)} {content}")
    if isinstance(content, str):
        return content
    try:
        return content.decode(encoding='gbk', errors='ignore')  # lambda x: unicode(x, 'utf-8', 'ignore')
    except:
        try:
            return content.decode(encoding='utf-8', errors='ignore')
        except:
            encodings = set(encodings_aliases.values())
            for encoding in encodings:
                if encoding not in ['gbk', 'utf-8']:
                    try:
                        return content.decode(encoding=encoding, errors='ignore')
                    except:
                        pass
    return str(content)


def test_sqlite3():
    db = 'E:/gzwjd.4db'
    print(check_file_exist(db))
    accessor = SQLAlCheAccessor()
    accessor.add_engine('sqlite0', f"sqlite:///{db}?check_same_thread=False", text_factory=lambda x: convert(x))
    rows = accessor.read_sql('sqlite0', 'SELECT distinct elementName FROM page_contain_elements')
    print(rows)


def test_mysql():
    accessor = SQLAlCheAccessor()
    accessor.add_engine('mysql0', 'mysql+pymysql://root:RNB.beop-2013@localhost/beopdata')

    print(accessor.read_sql('mysql0', 'SELECT * FROM some_table'))

    records = [{"A": 1, "B": 1, "C": 5.2, "D": "2021-07-23 00:00:00"}, {"A": 2, "B": 3, "C": 4.2, "D": "2021-07-25 00:00:00"}]
    cmds = accessor.generate_sql_cmds('some_table', records, 'replace', list(records[0].keys()))

    print(accessor.execute_multi_sql('mysql0', cmds))

    print(accessor.read_sql('mysql0', 'SELECT * FROM some_table'))

    record_update = [{"A": 1, "B": 1, "C": 5.2, "D": "2021-07-23 01:00:00"}, {"A": 2, "B": 3, "C": 4.2, "D": "2021-07-25 01:00:00"}]
    cmd_update = accessor.generate_sql_cmds('some_table', record_update, 'update', ["B", "C", "D"], ["A"])

    print(accessor.execute_multi_sql('mysql0', cmd_update))

    print(accessor.read_sql('mysql0', 'SELECT * FROM some_table'))

    print()


def test_oracle():
    accessor = SQLAlCheAccessor()
    accessor.add_engine('oracle0', 'oracle://cy2003:goen_cy2003@10.192.1.216:1521/gc', engine_pool_recycle=300)

    r = accessor.read_sql('oracle0', 'SELECT * FROM ACT')
    time.sleep(60)
    print(accessor.read_sql('oracle0', 'SELECT * FROM ACT'))

    records = [{"ID": '1512005962', "CNTR_NO": "123"}, {"ID": '1512005970', "CNTR_NO": "234"}]
    cmds = accessor.generate_sql_cmds('action_syn1', records, 'replace', list(records[0].keys()), ['ID'])

    # print(accessor.execute_multi_sql('oracle0', cmds))

    print()


def test_syn_oracle():
    from robertcommonio.system.io.sqlalche import SQLAlCheAccessor
    accessor = SQLAlCheAccessor()
    accessor.add_engine('oracle0', 'oracle://cy2003:goen_cy2003@10.192.1.250:1521/gc')
    r = accessor.read_sql('oracle0', 'SELECT count(*) FROM ACTION where data_out is null')
    print(r)


    records = [{"ID": '1512005962', "CNTR_NO": "123"}, {"ID": '1512005970', "CNTR_NO": "234"}]
    cmds = accessor.generate_sql_cmds('action_syn1', records, 'replace', list(records[0].keys()), ['ID'])

    print(accessor.execute_multi_sql('oracle0', cmds))

    print(accessor.read_sql('mysql0', 'SELECT * FROM some_table'))

    accessor = SQLAlCheAccessor()
    accessor.add_engine('oracle0', 'oracle://XX:XX@10.192.1.250:1521/gc')
    accessor.add_engine('oracle1', 'oracle://XX:XX@10.192.1.216:1521/gc')

    r = accessor.read_sql('oracle0', 'SELECT * FROM action_syn1 where date_out is null')

    records = [{"ID": '1512005962', "CNTR_NO": "123"}, {"ID": '1512005970', "CNTR_NO": "234"}]
    cmds = accessor.generate_sql_cmds('action_syn1', records, 'replace', list(records[0].keys()), ['ID'])

    print(accessor.execute_multi_sql('oracle0', cmds))

    print(accessor.read_sql('mysql0', 'SELECT * FROM some_table'))


def test_sqlite4():
    db = 'C:/nginx/resource/1/best.4db'
    db = '1.4db'

    accessor = SQLAlCheAccessor()
    #accessor.add_engine('sqlite0', f"sqlite:///{db}?check_same_thread=False")
    #accessor.add_engine('sqlite0', f"sqlite:///{db}?check_same_thread=False", text_factory=lambda x: convert(x))
    accessor.add_engine('sqlite0', f"sqlite:///{db}?check_same_thread=False", text_factory= lambda x: str(x, 'gbk', 'ignore'))
    rows = accessor.read_sql('sqlite0', 'select * from template_files where id=7')
    rows = accessor.read_sql('sqlite0', 'select id, name, unitproperty01 as group_order from list_pagegroup  where id=19 order by cast(group_order as int)')
    print(rows)


def test_create():
    aa = SQLQueryBuilder().select(f"id, order").from_table({'l': 'gcxl_dictinfo'}).order_by('id').build_query()
    bb = SQLQueryBuilder().insert_into('gcxl_dictinfo').values({'order': 123}).build_query()
    cc = SQLQueryBuilder().update('gcxl_dictinfo').set({'order': 123}).where({'order': 123}).build_query()
    print()


def test_oracle_bgein():
    accessor = SQLAlCheAccessor()
    accessor.add_engine('oracle0', f"oracle://DB3D:SMU_DB3D@{cx_Oracle.makedsn('10.192.1.247', 1521, service_name='gc')}")
    r = accessor.execute_sql('oracle0', f"begin update cntr_temp_t set DEVICE_INDEX='31 F0 F2',SCM_INDEX='F0 F2 1F FF FF FF FF FF FF FF FF FF',BAUD=38400, AIR_BRAND='TK4000',A2='1B 02 64 00 FE 7F 6E 00 71 00 8E 01 8F 02 FF 7F 1D 01 FE 7F FE 7F FE 7F FE 7F FE 7F FE 7F E3 00',A3='1B 02 64 00 FE 7F 6E 00 71 00 90 01 8F 02 FF',STATUS=0 where CNTR_NO='OERU4103855'; IF SQL%NOTFOUND THEN insert into cntr_temp_t values ('F0 F2 1F FF FF FF FF FF FF FF FF FF','31 F0 F2',38400,'TK4000','OERU4103855','1B 02 64 00 FE 7F 6E 00 71 00 8E 01 8F 02 FF 7F 1D 01 FE 7F FE 7F FE 7F FE 7F FE 7F FE 7F E3 00','1B 02 64 00 FE 7F 6E 00 71 00 90 01 8F 02 FF',NULL,NULL,NULL,NULL,0);END IF;end;")

    print(r)


def test_mysql1():
    accessor = SQLAlCheAccessor()
    accessor.add_engine('mysql0', 'mysql+pymysql://root:RNB.beop-2013@localhost/beopdata')

    print(accessor.read_sql('mysql0', 'SELECT * FROM data1'))
    accessor.add_engine('mysql1', 'mysql+pymysql://root:RNB.beop-2013@localhost1/beopdata')
    print(accessor.read_sql('mysql1', 'SELECT * FROM unit01'))
    accessor.add_engine('mysql1', 'mysql+pymysql://root:RNB.beop-2013@localhost1/beopdata')
    accessor.add_engine('mysql0', 'mysql+pymysql://root:RNB.beop-2013@localhost1/beopdata')
    print()


def test_syn_hgcy():
    from urllib.parse import quote_plus

    accessor = SQLAlCheAccessor()
    accessor.add_engine('mysql_nei', f"mysql+pymysql://root:{quote_plus('Gcxl#186@smu6')}@10.192.1.186:3306/jn_hgcy")

    cmds = []
    for record in accessor.read_sql('mysql_nei', f"SELECT * FROM hgcy_app_check_plan_2025 where id <= 4082321 and id >= 4081889"):
        id = int(record.get('ID'))
        cmds.append((f"update hgcy_app_check_plan_2025 set id={id + 1000000} where id = {id}", None))

    for record in accessor.read_sql('mysql_nei', f"SELECT * FROM hgcy_app_operation_v2 where CHECK_PLAN_ID <= 4082321 and CHECK_PLAN_ID >= 4081889 and TIME>='2025-01-01 00:00:00'"):
        cmds.append((f"update hgcy_app_operation_v2 set CHECK_PLAN_ID={int(record.get('CHECK_PLAN_ID')) + 1000000} where id={record.get('ID')}", None))

    if len(cmds) > 0:
        accessor.execute_multi_sql('mysql_nei', cmds)
    print()


def test_syn_sn():
    from urllib.parse import quote_plus
    from robertcommonio.system.io.sqlalche import SQLAlCheAccessor
    accessor = SQLAlCheAccessor()
    accessor.add_engine('mysql_nei', f"mysql+pymysql://nfzj:{quote_plus('Nfzj152@@!')}@171.32.2.250:3306/opc_runtime")

    records = accessor.read_sql('mysql_nei', f"SELECT * FROM opc_realtime_value")
    for i, record in enumerate(records):
        print(record)
    print()


def test_syn_sn1():
    from robertcommonio.system.io.sqlalche import SQLAlCheAccessor
    accessor = SQLAlCheAccessor()
    accessor.add_engine('mysql_nei', "mysql+pymysql://nfzj:Nfzj152%40%40%21@171.32.2.250:3306/opc_runtime")
    print(accessor.read_sql('mysql_nei', "SELECT count(*) FROM eFactoryData"))
    records = accessor.read_sql('mysql_nei', "SELECT count(*) FROM eFactoryData")
    for i, record in enumerate(records):
        print(record)
    print()


test_syn_sn1()