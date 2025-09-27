import requests

#设定基础的请求内容
API_Key = '6b56a879b1b34c9297d6f1c488eb339c'
City_LookUp_URL = "https://nc78kyefbq.re.qweatherapi.com/geo/v2/city/lookup"
Weather_URL = "https://nc78kyefbq.re.qweatherapi.com/v7/weather/now"
#定义主要请求函数
def get_weather(city_name):
    #请求参数
    lookup_params = {'location' : city_name,
                     'key' : API_Key,
                     'range':'cn'}
    try:
        city_respones = requests.get(City_LookUp_URL,params=lookup_params)
        city_data = city_respones.json()
    #防止请求错误
    except requests.exceptions.RequestException as e:
        return f'请求错误咯：{e}'
    #检查是否能找到
    if city_data.get('code') != '200':
        return f'没有找到对应的城市{city_name},请检查拼写'
    city_list = city_data.get('location',[])
    if not city_list:
        return f'没有找到对应的城市列表'
    #默认选择第一个搜索到的城市
    city_id = city_list[0]['id']
    city_name = city_list[0]['name']

    #用求到的城市id来请求对应城市的天气
    weather_params= {
        'location':city_id,
        'key':API_Key,
    }
    try:
        city_weather = requests.get(Weather_URL,params=weather_params)
        weather_data = city_weather.json()

    except requests.exceptions.RequestException as e:
        return f'请求错误咯：{e}'
    if weather_data.get('code') != '200':
        return f'没有找到对应的天气{city_name}'
    weather_deatil_list = weather_data['now']
    #返回结果
    time = weather_deatil_list['obsTime']
    temp = weather_deatil_list['temp']+'°c'
    fellsLike = weather_deatil_list['feelsLike']+'°c'
    weather_condition = weather_deatil_list['text']
    humidity = weather_deatil_list['humidity']+'%'
    vis = weather_deatil_list['vis']+'公里'
    result = f"""数据时间:{time}
                 温度:{temp}               
                 体感温度:{fellsLike}               
                 天气状况:{weather_condition}
                 空气湿度:{humidity}                  
                 能见度:{vis}                   
                            """
    return result
if __name__ == '__main__':
    while True:
        print('请任意时刻输入退出来关闭循环')
        name=input('请输入你要查询天气的城市:')
        if name =='退出':
            break
        print(get_weather(name))
