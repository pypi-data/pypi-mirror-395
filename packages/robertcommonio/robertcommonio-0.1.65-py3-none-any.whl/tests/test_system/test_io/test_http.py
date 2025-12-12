import json
from robertcommonio.system.io.http import HttpTool


response = HttpTool().send_request(url='http://app.dtuip.com/api/device/getDeviceSensorDatas', method='GET', timeout=30)
print(json.loads(response.data))


response = HttpTool().send_request(url='http://106.15.207.63/resource/basic/version/info.json', method='GET', timeout=120, retry=2)
print(json.loads(response.data))


response = HttpTool().send_request(url='https://stage.ari-smart.com/history/get_proj_data_start_time', method='POST', data=json.dumps({'proj_id': '1361'}, ensure_ascii=False), headers={'content-type': 'application/json', 'Accept-Encoding': 'gzip', 'token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MT'}, timeout=120, retry=2)
print(response)