import streamlit as st
import pandas as pd
import sqlite3
import requests
from io import StringIO

# 使用MVC架構下就不用使用,取消只為了單程式debug
#database_name = '165.db3'
#csv_url2 = 'https://data.moi.gov.tw/MoiOD/System/DownloadFile.aspx?DATA=7F6BE616-8CE6-449E-8620-5F627C22AA0D'
#table_name2= 'line_table'

def check_165linedb(url2, database_name, table_name2):
    response = requests.get(url2)
    data = StringIO(response.text)
    df_new = pd.read_csv(data)

    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    table_exists = cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name2}'").fetchone()

    if table_exists:
        df_existing = pd.read_sql(f"SELECT * FROM {table_name2}", conn)

        if not df_existing.equals(df_new):
            df_new.to_sql(table_name2, conn, index=False, if_exists='replace')
            result = "【165-詐騙LINE ID】已更新最新資料了！"
        else:
            result = "【165-詐騙LINE ID】已經是最新資料！"
    else:
        df_new.to_sql(table_name2, conn, index=False)
        result = "【165-詐騙LINE ID】建立新資料庫，已更新完成！"

    conn.close()
    return result


if __name__ == "__main__":
   # 檢查並更新數據庫
   result_message = check_165linedb(csv_url2, database_name, table_name2)
   print("最後修改日期:", result_message )