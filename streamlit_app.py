import time,sys,os,time,sqlite3,requests
import streamlit as st
import numpy as np
import pandas as pd
import whois
from io import StringIO
from datetime import datetime
from bs4 import BeautifulSoup
from Model.m_database_data import * ##import 匯入子程式Model資料夾下的m_database_data.py 
from Model.m_check_update_db import * ##import 匯入子程式Model資料夾下更新165網站資料 
from Model.m_check_line_db import * ##import 匯入子程式Model資料夾下更新165 line資料
from Model.m_find165_url import * ##import 匯入子程式Model資料夾下查詢165網站資料
from Model.m_findlineID import * ##import 匯入子程式Model資料夾下查詢165lineID資料
from Model.m_Diff_ServerDay import * ##import 匯入子程式Model資料夾下查詢m_Diff_ServerDay
from Model.m_checkIP import * ##import 匯入子程式Model資料夾下查詢查ip來源

def main():
    st.image("PIC/165logo.png", width=300)
    st.title('使用165內政部警政署官方資料庫')

    data = database_data()
    st.write(f'資料庫更新時間:{data}')

    global csv_url,csv_url2,database_name,table_name,table_name2,column_name,column_name2,url
    csv_url = 'https://data.moi.gov.tw/MoiOD/System/DownloadFile.aspx?DATA=3BB8E3CE-8223-43AF-B1AB-5824FA889883'
    database_name = 'Model/165.db3'
    table_name = 'url_table'
    column_name = 'WEBURL'

    csv_url2 = 'https://data.moi.gov.tw/MoiOD/System/DownloadFile.aspx?DATA=7F6BE616-8CE6-449E-8620-5F627C22AA0D'
    table_name2= 'line_table'
    column_name2 = '帳號'

    #當按下再次查詢時
    button_clicked = st.button('再次查詢資料更新時間!')
    # 下按後的動作
    if button_clicked:
        data = database_data()
        st.info(f'資料庫更新時間: {data}')
        #st.write(f'目前資料庫更新時間: {data}') write改用.info提示較為明顯

    #當按下時
    button_clicked = st.button('step1.更新公告【165假詐騙及博奕網站】資料庫')
    # 下按後的動作
    if button_clicked:
        progress_text = "更新中，請稍後..." #加入進度條代碼
        my_bar = st.progress(0, text=progress_text) #加入進度條代碼

        #在顯示進度條前先run更新程式跑完後,再顯示進度條1-100%動畫
        result_message = check_and_update_database(csv_url, database_name, table_name)        

        #加入進度條代碼,跑1-100%進度
        for percent_complete in range(100):
            time.sleep(0.05)
            my_bar.progress(percent_complete + 1, text=progress_text)
        
        #加入進度條代碼
        my_bar.progress(100, text="更新完成！")
        #write改用.success顯示較為明顯
        st.success(result_message)
        # st.write("最後修改日期:", result_message) 

    #當按下165 line查詢時
    button_clicked = st.button('step2.更新公告【165-詐騙LINE ID】資料庫')
    # 下按後的動作
    if button_clicked:
        progress_text = "更新中，請稍後..." #加入進度條代碼
        my_bar = st.progress(0, text=progress_text) #加入進度條代碼

        #在顯示進度條前先run更新程式跑完後,再顯示進度條1-100%動畫        
        result_message = check_165linedb(csv_url2, database_name, table_name2)
        #加入進度條代碼,跑1-100%進度
        for percent_complete in range(100):
            time.sleep(0.05)
            my_bar.progress(percent_complete + 1, text=progress_text)     
 
        #加入進度條代碼
        my_bar.progress(100, text="更新完成！")
        st.success(result_message)
        #st.write("最後修改日期:", result_message) write改用.success顯示較為明顯


    with st.form(key='165url_form'):
        form_name = st.text_input(label='step3.查詢已公告【165假詐騙及博奕網站】', placeholder='請輸入網站,勿輸入http://')
        submit_button = st.form_submit_button(label='查詢')

    #當按下enter後自動查詢165url是否有詐騙
    if submit_button:
        # 使用者輸入欲查詢網址的字串
        input_string = form_name

        # 使用 search_database 函數執行查詢
        results = search_database(input_string, database_name, table_name, column_name)

        # 顯示結果
        if results:
            st.write("是詐騙！請立刻與165警方聯絡！資料庫中存在包含 '{}' 字串的相關資料：".format(input_string))
            st.write("內政部警政署165報案資料如下")
            st.write("網站名稱 網址 件數 統計 起始日期 統計結束日期")
            # 輸出所有查詢到的整行資料
            for row in results:
                st.write(row)
        else:
            st.write("資料庫中沒有包含 '{}' 字串的相關資料。".format(input_string))

    with st.form(key='165line_form'):
        form_name2 = st.text_input(label='step4.查詢已公告【165詐騙LineID】', placeholder='請輸入LineID')
        submit_button = st.form_submit_button(label='查詢')

    #當按下enter後自動查詢165 lineID是否有詐騙
    if submit_button:
        # 使用者輸入欲查詢網址的字串
        input_string = form_name2

        # 使用 search_lineID_DB 函數執行查詢
        results = search_lineID_DB(input_string, database_name, table_name2, column_name2)

        # 顯示結果
        if results:
            st.write("是詐騙！請立刻與165警方聯絡！資料庫中存在包含 '{}' 字串的相關資料：".format(input_string))
            st.write("內政部警政署165報案資料如下")
            st.write("編號 詐騙LINEID 通報日期")
            # 輸出所有查詢到的整行資料
            for row in results:
                st.write(row)
        else:
            st.write("資料庫中沒有包含 '{}' 字串的相關資料。".format(input_string))

    # 使用 Streamlit 构建表单和提交按钮
    with st.form(key='ip_form'):
        form_name3 = st.text_input(label='step5.查詢此網址電腦來源', placeholder='請輸入完整網址，包含http://..../')
        submit_button = st.form_submit_button(label='查詢')

    
    # 当按下提交按钮后查找 IP 地址和表格信息
    if submit_button:
        # 使用者輸入欲查詢網址的字串
        url3  = form_name3

        # 获取 Creation Date
        creation_date = get_creation_date(url3)        
        if creation_date:
            st.info(f"對方伺服器whois建立日期: {creation_date}")            
            # 只提取天數，計算和伺服器日期的時間差（只提取天数）
            days_difference = calculate_time_difference(creation_date)
            
            if days_difference is not None:
                
                st.error(f"此伺服器建立至今已成立: {days_difference} days，100%詐騙網站都建立更新日期1年內 ！詐騙極高！")
            else:
                print("Failed to calculate time difference.")
        else:
            print("Failed to retrieve Creation Date.")

        ip_address = get_ip_address(url3)
        table_data = get_table_data(ip_address)
        st.info(f'對方電腦IP位置: {ip_address}')
        st.write("1.國家 2.對方所在城市 3.郵地區號 4.經度 5.ISP供應者 6.域名")
        st.write(table_data)



if __name__ == "__main__":
    main()
