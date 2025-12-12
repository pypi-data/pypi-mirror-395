from robertcommonio.system.io.license import gen_license_file, show_license_file, parse_license_file


def test_license():
    path = r'E:\license.xml'
    encodings = 'UTF-8'
    value = {'license': {'@vendor': 'Ari', '@expire': '2024-01-01', '@mac': '1DA8-E3F0-9E6A-493D', '@version': 'V1.0.2', '@author': '', '@generated': '2022-11-22', 'project': {'@name': '测试项目', '@id': '1', '@user': 'admin', '@psw': '123456', 'drivers': {'@support': '*', 'driver': [{'@type': 'opc', '@device.limit': '10', '@point.limit': '10000'}, {'@type': 'tcp_core', '@device.limit': '1', '@point.limit': 'none', 'devices': {'device': {'@name': 'TCP', 'property': [{'@name': 'enabled', '@value': 'true', '@type': 'str'}, {'@name': 'host', '@value': 'localhost', '@type': 'str'}, {'@name': 'port', '@value': '9500', '@type': 'int'}, {'@name': 'reg', '@value': 'test_dtu', '@type': 'str'}, {'@name': 'interval', '@value': '1m', '@type': 'str'}, {'@name': 'timeout', '@value': '5', '@type': 'int'}]}}}]}}}}
    gen_license_file(path, value, 1024, encodings)
    content1 = show_license_file(path, encodings)
    content2 = parse_license_file(path, encodings, '')
    print()


test_license()