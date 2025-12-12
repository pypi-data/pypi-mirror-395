import datetime
import json
import os
import re
import requests
from urllib.parse import urlparse


def json_parse_safe(obj):
    """安全的JSON处理"""
    try:
        if isinstance(obj, str):
            return json.loads(obj) if obj else {}
        elif isinstance(obj, (dict, list)):
            # 如果已经是 dict 或 list，直接返回
            return obj
        else:
            return {}
    except (json.JSONDecodeError, TypeError):
        return {}
def get_public_ip(ip="",source=10):

    """
    获取公网IP信息
    :param ip: IP地址
    :param source: 获取IP信息的源，默认为10 0-15
    :return: IP信息字典
    """
    if source==0:
        url = f"https://whois.pconline.com.cn/ipJson.jsp?ip={ip}&json=true"
        ret = requests.get(url)
        if ret is None:
            return ""
        print(ret.text)
        json_data = json.loads(ret.text)

        ip_info = {
            "ip": json_data.get("ip"),
            "country": json_data.get("country"),
            "province": json_data.get("pro"),
            "city": json_data.get("city"),
            "isp": json_data.get("company"),
            "cityCode": json_data.get("cityCode"),
            "type": json_data.get("type"),
        }
        return ip_info
    elif source==1:
        url = f"https://api.vore.top/api/IPdata?ip={ip}"
        ret = requests.get(url)
        if ret is None:
            return ""
        print(ret.text)
        json_data = json.loads(ret.text)
        ip_info = {
            "ip": json_data.get("ipinfo", {}).get("text", ""),
            "country": json_data.get("country"),
            "province": json_data.get("ipdata", {}).get("info1", ""),
            "city": json_data.get("ipdata", {}).get("info2", ""),
            "district": json_data.get("ipdata", {}).get("info3", ""),  # 添加区/县信息
            "isp":json_data.get("ipdata", {}).get("isp", ""),
            "cityCode": json_data.get("adcode", {}).get("a", ""),
            "type": json_data.get("ipinfo", {}).get("type", ""),
        }
        return ip_info
    elif source==2:
        url = f"http://demo.ip-api.com/json/?lang=zh-CN"
        ret = requests.get(url)
        if ret is None:
            return ""
        print(ret.text)
        json_data = json.loads(ret.text)
        #{"status":"success","country":"中国","countryCode":"CN","region":"HA","regionName":"河南","city":"濮阳县城关镇","zip":"","lat":35.7062,"lon":115.028,"timezone":"Asia/Shanghai","isp":"Chinanet","org":"","as":"AS4134 CHINANET-BACKBONE","query":"123.52.205.93"}
        ip_info={
            "ip": json_data.get("query", ""),
            "country": json_data.get("country", ""),
            "province": json_data.get("regionName", ""),
            "city": json_data.get("city", ""),
            "district": json_data.get("district", ""),  # 添加区/县信息
            "isp": json_data.get("isp", ""),
            "cityCode": json_data.get("cityCode", ""),
            "type": json_data.get("type", ""),
            "lat": json_data.get("lat", ""),
            "lon": json_data.get("lon", ""),
        }
        return ip_info
    elif source==3:
        url = f"http://httpbin.org/ip"
        ret = requests.get(url)
        if ret is None:
            return ""
        json_data = json.loads(ret.text)
        #{"origin": "123.52.205.93"}
        ip_info = {
            "ip": json_data.get("origin", ""),
        }
        return ip_info
    elif source==4:
        url = f"https://vv.video.qq.com/checktime?otype=ojson"
        ret = requests.get(url)
        if ret is None:
            return ""
        print(ret.text)
        json_data = json.loads(ret.text)
        #{"s":"o","t":1764669188,"ip":"123.52.205.93","pos":"---","rand":"Xkgh_260PzliI2E-amN0zA=="}
        ip_info = {
            "ip": json_data.get("ip", ""),
        }
        return ip_info
    elif source==5:
        url = f"https://ipv4.my.ipinfo.app/api/ipDetails.php"
        ret = requests.get(url)
        if ret is None:
            return ""
        print(ret.text)
        json_data = json.loads(ret.text)
        #{"ip":"123.52.205.93","asn":"AS4134 - CHINANET-BACKBONE No.31,Jin-rong Street","continent":"AS","continentLong":"Asia","flag":"https://my.ipinfo.app/imgs/flags/4x3/cn.svg","country":"China"}
        ip_info = {
            "ip": json_data.get("ip", ""),
            "country": json_data.get("country", ""),
        }
        return ip_info
    elif source==6:
        url = f"https://r.inews.qq.com/api/ip2city"
        ret = requests.get(url)
        if ret is None:
            return ""
        json_data = json.loads(ret.text)
        #{"ret":0,"errMsg":"","ip":"123.52.205.93","provcode":"18","citycode":"188","country":"中国","province":"河南省","city":"濮阳市","district":"","isp":"","districtCode":"410900","callback":""}
        ip_info = {
            "ip": json_data.get("ip", ""),
            "country": json_data.get("country", ""),
            "province": json_data.get("province", ""),
            "city": json_data.get("city", ""),
            "district": json_data.get("district", ""),
            "isp": json_data.get("isp", ""),
            "cityCode": json_data.get("districtCode", ""),
        }
        return ip_info
    elif source==7:
        url = f"https://myip.ipip.net/json"
        ret = requests.get(url)
        if ret is None:
            return ""
        json_data = json.loads(ret.text)
        #{"ret":"ok","data":{"ip":"123.52.205.93","location":["中国","河南","濮阳","","电信"]}}
        ip_info = {
            "ip": json_data.get("data", {}).get("ip", ""),
            "country": json_data.get("data", {}).get("location", [])[0],
            "province": json_data.get("data", {}).get("location", [])[1],
            "city": json_data.get("data", {}).get("location", [])[2],
            "district": json_data.get("data", {}).get("location", [])[3],
            "isp": json_data.get("data", {}).get("location", [])[4],
        }
        return ip_info
    elif source==8:
        url = f"https://iplark.com/ipstack"
        ret = requests.get(url)
        if ret is None:
            return ""
        json_data = json.loads(ret.text)
        #{"ip":"123.52.205.93","type":"ipv4","continent_code":"AS","continent_name":"亚洲","country_code":"CN","country_name":"中国","region_code":"HA","region_name":"Henan","city":"Puyang","zip":"457000","latitude":35.6966705322266,"longitude":115.013893127441,"msa":null,"dma":null,"radius":"0","ip_routing_type":"fixed","connection_type":"tx","location":{"geoname_id":1798422,"capital":"Beijing","languages":[{"code":"zh","name":"Chinese","native":"中文"}],"country_flag":"https://assets.ipstack.com/flags/cn.svg","country_flag_emoji":"🇨🇳","country_flag_emoji_unicode":"U+1F1E8 U+1F1F3","calling_code":"86","is_eu":false},"time_zone":{"id":"Asia/Shanghai","current_time":"2025-12-02T18:12:02+08:00","gmt_offset":28800,"code":"CST","is_daylight_saving":false},"currency":{"code":"CNY","name":"Chinese Yuan","plural":"Chinese yuan","symbol":"CN¥","symbol_native":"CN¥"},"connection":{"asn":4134,"isp":"Chinanet","sld":null,"tld":null,"carrier":"chinanet","home":false,"organization_type":"Telecommunications","isic_code":"J6100","naics_code":"000517"},"security":{"is_proxy":false,"proxy_type":null,"is_crawler":false,"crawler_name":null,"crawler_type":null,"is_tor":false,"threat_level":"low","threat_types":null,"proxy_last_detected":null,"proxy_level":null,"vpn_service":null,"anonymizer_status":null,"hosting_facility":false}}
        ip_info = {
            "ip": json_data.get("ip", ""),
            "country": json_data.get("country_name", ""),
            "province": json_data.get("region_name", ""),
            "city": json_data.get("city", ""),
            "district": json_data.get("district", ""),
            "isp": json_data.get("isp", ""),
            "cityCode": json_data.get("city_code", ""),
            "type": json_data.get("type", ""),
            "lat": json_data.get("latitude", ""),
            "lon": json_data.get("longitude", ""),
        }
        return ip_info
    elif source==9:
        url = f"https://ipservice.ws.126.net/locate/api/getLocByIp"
        ret = requests.get(url)
        if ret is None:
            return ""
        json_data = json.loads(ret.text)
        #{"message":"查询成功","status":200,"result":{"administrativeCode":"410900","areaCode":"86","areaLat":"35.747699","areaLng":"115.014198","city":"濮阳","company":"电信","continentCode":"AP","country":"中国","countrySymbol":"CN","ip":"123.52.205.93","network":"AP","operator":"","province":"河南","timezone":"Asia/Shanghai","utc":"UTC+8"}}
        ip_info = {
            "ip": json_data.get("result", {}).get("ip", ""),
            "country": json_data.get("result", {}).get("country", ""),
            "province": json_data.get("result", {}).get("province", ""),
            "city": json_data.get("result", {}).get("city", ""),
            "district": json_data.get("result", {}).get("district", ""),
            "isp": json_data.get("result", {}).get("operator", ""),
            "cityCode": json_data.get("result", {}).get("administrativeCode", ""),
            "type": json_data.get("result", {}).get("network", ""),
            "lat": json_data.get("result", {}).get("areaLat", ""),
            "lon": json_data.get("result", {}).get("areaLng", ""),
        }
        return ip_info
    elif source==10:
        url = f"https://126.com/fgw/mailsrv-ipdetail/detail"
        ret = requests.get(url)
        if ret is None:
            return ""
        json_data = json.loads(ret.text)
        #{"code":200,"desc":"DONE","success":"false","result":{"country":"中国","province":"河南省","provinceEn":"Henan","city":"濮阳市","org":"中国电信","isp":"电信","latitude":"35.7532978882","longitude":"115.026627441","timezone":"Asia/Shanghai","countryCode":"CN","continentCode":"AS","provinceCode":"41","continent":"亚洲","county":"UNKNOWN","ispId":"10000","ip":"123.52.205.93","zone":"gz"}}
        ip_info = {
            "ip": json_data.get("result", {}).get("ip", ""),
            "country": json_data.get("result", {}).get("country", ""),
            "province": json_data.get("result", {}).get("province", ""),
            "city": json_data.get("result", {}).get("city", ""),
            "district": json_data.get("result", {}).get("county", ""),
            "isp": json_data.get("result", {}).get("isp", ""),
            "cityCode": json_data.get("result", {}).get("cityCode", ""),
            "lat": json_data.get("result", {}).get("latitude", ""),
            "lon": json_data.get("result", {}).get("longitude", ""),

        }
        return ip_info
    elif source==11:
        url = f"http://only-162333-112-96-112-201.nstool.zhuanzfx.com/info.js"
        ret = requests.get(url)
        if ret is None:
            return ""
        #var ip = '123.52.205.93'; var dns = '171.15.161.125'; var ip_province = '河南省'; var ip_city = '濮阳市'; var ip_isp = '电信'; var dns_province = '河南省'; var dns_city = '郑州市'; var dns_isp = '电信'; var res = 'correct'; var msg = '您的DNS设置正确';
        ip_info = {
            "ip": ret.text.split("ip = '")[1].split("';")[0],
            "province": ret.text.split("ip_province = '")[1].split("';")[0],
            "city": ret.text.split("ip_city = '")[1].split("';")[0],
            "isp": ret.text.split("ip_isp = '")[1].split("';")[0],
        }
        return ip_info
    elif source==12:
        url = f"https://ipv4.gdt.qq.com/get_client_ip"
        ret = requests.get(url)
        if ret is None:
            return ""
        #123.52.205.93
        ip_info = {
            "ip": ret.text.strip(),

        }
        return ip_info
    elif source==13:
        url = f"http://fn.syyx.com/my_ip"
        ret = requests.get(url)
        if ret is None:
            return ""
        ip_info = {
            "ip": ret.text.strip(),

        }
        return ip_info
    elif source==14:
        url = f"https://www.uc.cn/ip"
        ret = requests.get(url)
        if ret is None:
            return ""
        #IP:33.50.238.112
        ip_info = {
            "ip": ret.text.split("IP:")[1].strip(),
        }
        return ip_info
    elif source==15:
        url = f"https://who.nie.163.com/"
        ret = requests.get(url)
        if ret is None:
            return ""
        #{"ip":"123.52.205.93","country":"CN"}
        json_data = json.loads(ret.text)
        ip_info = {
            "ip": json_data.get("ip", ""),
            "country": json_data.get("country", ""),
        }
        return ip_info
    #https://get.geojs.io/v1/ip/geo.json
    return None


def url_get_domain(url):
    """
    获取URL的域名

    Args:
        url (str): URL字符串

    Returns:
        str: 域名
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc
def get_jsonp(text):
    """
    解析JSONP字符串并返回JSON对象

    Args:
        text (str): JSONP字符串

    Returns:
        dict: 解析后的JSON对象
    """
    jsonp_str = re.search(r"\((.*)\)", text, re.S).group(1)
    return json.loads(jsonp_str)
def save_log(filename, log_content):
    """
    保存日志到指定文件

    :param filename: 日志文件名
    :param log_content: 需要保存的日志内容
    """
    # 定义日志文件夹路径
    log_dir = "logs"
    # 检查log文件夹是否存在，不存在则创建
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 构建完整的文件路径
    file_path = os.path.join(log_dir, filename)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 以追加模式打开文件，如果文件不存在会自动创建
    with open(file_path+".txt", 'a', encoding='utf-8') as file:
        file.write(f"[{current_time}] {log_content}\n")

def cookie_dict_to_string(cookie_dict):
    """
    将字典格式的cookie转换为字符串格式(key=value; key=value)

    Args:
        cookie_dict (dict): cookie字典

    Returns:
        str: 字符串格式的cookie
    """
    if not isinstance(cookie_dict, dict):
        raise ValueError("输入必须是字典类型")

    cookie_items = []
    for key, value in cookie_dict.items():
        cookie_items.append(f"{key}={value}")

    return "; ".join(cookie_items)
def cookie_string_to_dict(cookie_string):
    """
    将字符串格式的cookie转换为字典格式

    Args:
        cookie_string (str): 字符串格式的cookie (key=value; key=value)

    Returns:
        dict: cookie字典
    """
    if not isinstance(cookie_string, str):
        raise ValueError("输入必须是字符串类型")

    cookie_dict = {}
    if not cookie_string.strip():
        return cookie_dict

    # 按分号分割cookie项
    items = cookie_string.split(";")
    for item in items:
        item = item.strip()  # 去除前后空格
        if "=" in item:
            key, value = item.split("=", 1)  # 只分割第一个等号
            cookie_dict[key.strip()] = value.strip()

    return cookie_dict
def cookie_merge(old_cookie, new_cookie):
    """
    合并更新cookie，支持字典和字符串两种格式

    Args:
        old_cookie (dict or str): 旧cookie
        new_cookie (dict or str): 新cookie

    Returns:
        dict or str: 合并后的cookie，格式与old_cookie保持一致
    """
    # 判断输入类型
    old_is_dict = isinstance(old_cookie, dict)
    new_is_dict = isinstance(new_cookie, dict)

    # 统一转换为字典格式进行处理
    if old_is_dict:
        old_dict = old_cookie.copy()
    else:
        old_dict = cookie_string_to_dict(old_cookie)

    if new_is_dict:
        new_dict = new_cookie
    else:
        new_dict = cookie_string_to_dict(new_cookie)

    # 合并cookie，新cookie覆盖旧cookie
    merged_dict = {**old_dict, **new_dict}

    # 根据原始格式返回结果
    if old_is_dict:
        return merged_dict
    else:
        return cookie_dict_to_string(merged_dict)



if __name__ == '__main__':
    print(get_public_ip(source=10))

    pass


