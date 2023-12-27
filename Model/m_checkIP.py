import socket
import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_ip_address(url3):
    try:
        # 提取主机名（hostname）部分
        parts = url3.split("//")
        if len(parts) > 1:
            hostname = parts[1].split("/")[0]
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        else:
            return f"URL格式無效: {url3}"
    except socket.error as e:
        return f"Unable to resolve {url3}: {e}"

def get_table_data(ip_address):
    ur4 = f"https://www.geolocation.com/zh_tw?ip={ip_address}#ipresult"

    response = requests.get(ur4)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        country = soup.find('div', string='國家').find_next('a').text.strip()
        area = soup.find('div', string='區域').find_next('td').text.strip()
        city = soup.find('div', string='市').find_next('td').text.strip()
        latitude = soup.find('div', string='緯度').find_next('td').text.strip()
        longitude = soup.find('div', string='經度').find_next('td').text.strip()
        isp = soup.find('div', string='ISP').find_next('td').text.strip()
        domain = soup.find('div', string='域名').find_next('td').text.strip()

        # 將所有信息組合成一個字符串
        result_string = f"{country}, {area}, {city}, {latitude}, {longitude}, {isp}, {domain}"

        return result_string
    else:
        return f"请求失败，状态码：{response.status_code}"

# 用户输入网址
#單程式測試用
#url3 = input("請輸入完整網址:.... ")
# 获取 IP 地址
#單程式測試用
#ip_address = get_ip_address(url3)

# 获取表格信息
#單程式測試用
#table_data = get_table_data(ip_address)

if __name__ == "__main__":
    # 檢查並更新數據庫
    print("IP 地址:", ip_address)
    print("國家:", table_data)  # 在這裡打印 country 的值