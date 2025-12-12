from robertcommonio.system.io.data_storage import DataStorage, MongoAccessor, MySqlAccessor, MongoConfig, DateRange, datetime, TimeInterval


def test_real():
    access = MySqlAccessor('localhost', 3306, 'root', 'RNB.beop-2013', 'iot_engine')
    write_result = DataStorage().save_data([access], [['2021-5-1 00:00:01', 'name1', 'test2'], ['2022-5-1 00:00:02', 'name2', '2.9']])
    read_result = DataStorage().load_realtime_data(access, [f'@0|name1', "@0|name2", "@0|name3"])
    print(read_result)


def test_history():
    access = MongoAccessor(config=MongoConfig('localhost', 27017, 'gateway', 'gateway@123456', 'iot_engine', None, None, None))
    #write_result = DataStorage().save_data([access], [['2022-5-1 00:02:00', 'name1', 'test2'], ['2022-5-1 00:03:00', 'name2', '2.9'], ['2022-5-1 00:01:00', 'name3', '2.9']])
    read_result = DataStorage().load_history_data(access, DateRange(datetime(2022, 5, 1, 0, 0), datetime(2022, 5, 1, 2, 0), TimeInterval.m1), [f'@0|name1', "@0|name2", "@0|name3"])
    print(read_result)


def test_log():
    access = MongoAccessor(config=MongoConfig('localhost', 27017, 'gateway', 'gateway@123456', 'iot_engine', None, None, None))
    #write_result = DataStorage().save_log([access], [{'user_id': 1, 'content': '测试数据', 'source': 'ss', 'type': 'communication'}, {'user_id': -1, 'content': '读取错误', 'source': 'name1', 'type': 'point'}, ])
    read_result = DataStorage().read_log(access, datetime(2022, 5, 1, 0, 0), datetime(2023, 5, 1, 2, 0), 1, 1)
    print(read_result)


test_history()