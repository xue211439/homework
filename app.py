import requests
import csv

# 基本参数配置
apiUrl = 'http://apis.juhe.cn/fapigw/air/provinces'
# 请替换为你自己的真实API Key
apiKey = 'dc49036741ab332e34be5e4b81629561'

# 接口请求入参配置
requestParams = {
    'key': apiKey,
    'city': '北京'
}

# 发起接口网络请求
try:
    response = requests.get(apiUrl, params=requestParams)
    # 解析响应结果
    if response.status_code == 200:
        responseResult = response.json()
        if responseResult['error_code'] == 0:
            result = responseResult['result']
            weather_data = []
            for item in result:
                city = item.get('city')
                weather = item.get('realtime', {}).get('weather')
                temperature = item.get('realtime', {}).get('temperature')
                weather_data.append([city, weather, temperature])

            # 将数据写入CSV文件
            with open('weather.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['城市', '天气状况', '温度'])
                writer.writerows(weather_data)
            print("天气数据已成功保存到 weather.csv 文件。")
        else:
            print(f"API请求错误，错误码: {responseResult['error_code']}，错误信息: {responseResult['reason']}")
    else:
        print(f'请求异常，状态码: {response.status_code}')
except requests.RequestException as e:
    print(f"网络请求出错: {e}")
